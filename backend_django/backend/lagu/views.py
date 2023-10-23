import re
from datetime import timedelta
from django.db.models import Sum, Count
import locale

from django.db.models.functions import ExtractMonth
from django.forms import FloatField
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import action
from .models import *

from .serializers import BanSerializer, MenuSerializer, DSDatBanSerialier, KhachHangSerializer, DsOrderSerialier, \
    HoaDonThanhToanSerializer, GiamGiaSerializer, HoaDonCocTienSerializer, ChiTietHoaDonSerializer

ACCEPTANCE_TIME = 5  # phút | KHOẢNG THỜI GIAN CHẤP NHẬN ĐƯỢC
TIME_CHECK = 2
COUNT_BOOK = 6
TIME_BOOK_FEW = 120  # phút | khoảng thời gian trước khi nhận bàn (few)
TIME_BOOK_MANY = 7  # ngày | khoảng thời gian trước khi nhận bàn (many)
ORDER_MANY = 4  # MÓN | order tối thiểu (many)
ORDER_FEW = 2  # MÓN | order tối thiểu (few)
COUNT_TABLE_FEW = 2  # BÀN | số bàn tối thiểu (few)
COUNT_TABLE_MANY = 6  # BÀN | số bàn tối thiểu (many)
LAST_TIME_RECEIVE_BOOK_MANY = 120  # phút | khoảng thời gian cho phép nhận bàn (many)
LAST_TIME_RECEIVE_BOOK_FEW = 45  # phút | khoảng thời gian cho phép nhận bàn (few)
CANCEL_BOOK_FEW = 60  # phút | trước khoảng thời gian cho phép hủy (few)
CANCEL_BOOK_MANY = 1  # ngày | trước khoảng thời gian cho phép hủy (many)
UPDATE_TIME_BOOK_MANY = 7  # ngày | khoảng thời gian tối đa cho phép thay đổi thời gian nhận bàn sớm hơn (many)
LAST_UPDATE_TIME_BOOK_MANY = 30  # ngày | khoảng thời gian tối đa cho phép thay đổi thời gian nhận bàn trễ hơn (many)
UPDATE_TIME_BOOK_FEW = 60  # phút | khoảng thời gian tối đa cho phép thay đổi thời gian nhận bàn sớm hơn (few)
LAST_UPDATE_TIME_BOOK_FEW = 60  # phút | khoảng thời gian tối đa cho phép thay đổi thời gian nhận bàn trễ hơn (few)
TIME_UPDATE_ORDER_MANY = 1  # ngày | trước khoảng thời gian cho phép thay đổi order (many)
TIME_UPDATE_ORDER_FEW = 60  # phút | trước khoảng thời gian cho phép thay đổi order (few)
TIME_UPDATE_COUNT_TABLE_MANY = 1  # ngày | trước khoảng thời gian cho phép thay đổi số lượng bàn (many)
TIME_UPDATE_COUNT_TABLE_FEW = 45  # phút | trước khoảng thời gian cho phép thay đổi số lượng bàn (few)
PERCENT_TOTAL_BILL = 40  # Phần trăm | khoảng thanh toán đặt cọc


# Create your views here.


class TestView(viewsets.ViewSet, generics.ListAPIView):
    def test(self, request):
        return Response('hello world!!')


class BanViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Ban.objects.all()
    serializer_class = BanSerializer

    @action(methods=['get'], detail=False, url_path="get-ds-ban")
    def get_ds_ban(self, request):
        try:
            ban = Ban.objects.all()
            data = BanSerializer(ban, many=True).data
            return Response(data, status.HTTP_200_OK)
        except Exception as e:
            return Response("Message: " + str(e), status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], detail=True, url_path="change-active")
    def change_active(self, request, pk):
        try:
            ban = Ban.objects.get(id=pk)
            if ban.is_trang_thai:
                ban.is_trang_thai = False
                ban.save()
            else:
                ban.is_trang_thai = True
                ban.save()
            return Response(dict(message="update success"), status.HTTP_200_OK)
        except Exception as e:
            return Response("Message: " + str(e), status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path="create-table")
    def create_table(self, request, pk=None):
        try:
            so_luong = request.data.get('so_luong')
            suc_chua = request.data.get('suc_chua')
            loai_ban = request.data.get('loai_ban')
            ban = Ban.objects.filter(loai_ban=loai_ban)
            if not ban:
                new_ban = Ban(so_luong=so_luong, suc_chua=suc_chua, loai_ban=loai_ban)
                new_ban.save()
                return Response(dict(message="create success"), status.HTTP_200_OK)
            else:
                raise Exception("Loại bàn đã tồn tại")
        except Exception as e:
            return Response("Message: " + str(e), status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], detail=True, url_path="update-info")
    def update_info(self, request, pk):
        try:
            ban = Ban.objects.get(id=pk)
            if request.data.get('so_luong'):
                ban.so_luong = request.data.get('so_luong')
            if request.data.get('suc_chua'):
                ban.suc_chua = request.data.get('suc_chua')
            if request.data.get('loai_ban'):
                loai_ban = request.data.get('loai_ban')
                check = Ban.objects.filter(loai_ban=loai_ban)
                if not check:
                    ban.loai_ban = loai_ban
            ban.save()
            return Response(dict(message="update success"), status.HTTP_200_OK)
        except Exception as e:
            return Response("Message: " + str(e), status.HTTP_400_BAD_REQUEST)


class MenuViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    parser_classes = [MultiPartParser, ]

    @action(methods=['get'], detail=False, url_path="get-active-menu")
    def active_menu(self, request):
        menus = Menu.objects.filter(is_trang_thai=True).all()
        serializer_data = MenuSerializer(menus, many=True).data
        return Response(serializer_data, status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path="create-menu")
    def create_menu(self, request, pk=None):
        try:
            ten = request.data.get('ten_san_pham')
            don_gia = request.data.get('don_gia')
            don_gia_str = don_gia.replace('"', '')
            don_gia = float(don_gia_str)
            loai = request.data.get('loai')
            anh = request.FILES['link_anh']
            mon = Menu(ten_san_pham=ten, don_gia=don_gia, loai=loai, link_anh=anh)
            mon.save()
            return Response("Message: Create success", status.HTTP_200_OK)
        except Exception as e:
            return Response("Message: " + str(e), status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True, url_path="up-hinh")
    def up(self, request, pk):
        try:
            mon = Menu.objects.get(id=pk)
            uploaded_file = request.FILES['link_anh']
            mon.link_anh = uploaded_file
            if uploaded_file is None:
                raise Exception('file null')
            mon.save()
            return Response("Message: Upload success", status.HTTP_200_OK)
        except Exception as e:
            return Response("Message: " + str(e), status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path="update-trang-thai")
    def update_trang_thai(self, request, pk=None):
        try:
            id = request.data.get('id')
            mon = Menu.objects.get(id=id)
            if mon:
                if mon.is_trang_thai:
                    mon.is_trang_thai = False
                    mon.save()
                else:
                    mon.is_trang_thai = True
                    mon.save()
                return Response("Message: update success", status.HTTP_200_OK)
        except Exception as e:
            return Response("Message: " + str(e), status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], detail=True, url_path="update-menu")
    def update_menu(self, request, pk):
        try:
            mon = Menu.objects.get(id=pk)
            if mon:
                if request.data.get('ten_san_pham'):
                    ten = request.data.get('ten_san_pham')
                    mon.ten_san_pham = ten
                    mon.save()
                if request.data.get('don_gia'):
                    don_gia = request.data.get('don_gia')
                    don_gia_str = don_gia.replace('"', '')
                    don_gia = float(don_gia_str)
                    mon.don_gia = don_gia
                    mon.save()
                if request.FILES.get('link_anh'):
                    link_anh = request.FILES['link_anh']
                    mon.link_anh = link_anh
                if request.data.get('loai'):
                    loai = request.data.get('loai')
                    mon.loai = loai
                    mon.save()
                if request.data.get('is_trang_thai'):
                    trang_thai = request.data.get('is_trang_thai')
                    if trang_thai == 'true':
                        mon.is_trang_thai = True
                        mon.save()
                    else:
                        mon.is_trang_thai = False
                        mon.save()
                mon.save()
                return Response("Message: update success", status.HTTP_200_OK)
            else:
                raise Exception('khong tim duoc mon')

        except Exception as e:
            return Response("Message: " + str(e), status.HTTP_400_BAD_REQUEST)


class KhachHangViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = KhachHangSerializer

    @action(methods=['get'], detail=False, url_path="check-khach-hang")
    def get_khach_hang_by_sdt(self, request, pk=None):
        try:
            sdt = request.data.get('so_dien_thoai')
            khach_hang = KhachHang.objects.get(so_dien_thoai=sdt)
            if khach_hang:
                json_khach_hang = KhachHangSerializer(khach_hang).data
                return Response(json_khach_hang, status.HTTP_200_OK)
        except Exception as e:
            return Response("Message: " + str(e), status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path="create-khach-hang")
    def create_info(self, request, pk=None):
        try:
            so_dien_thoai = request.data.get('sdt')
            if not re.match("^[0-9]+$", so_dien_thoai) or len(so_dien_thoai) != 10:
                raise Exception('số điện thoại không hợp lệ')
            ho_ten = request.data.get('ho_ten')
            dia_chi = request.data.get('dia_chi')
            new_khach_hang = KhachHang(so_dien_thoai=so_dien_thoai, ho_ten=ho_ten, dia_chi=dia_chi)
            new_khach_hang.save()
            return Response(dict(message="create success"), status.HTTP_200_OK)
        except Exception as e:
            return Response("Message: " + str(e), status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path="khach-hang-info")
    def get_info(self, request, pk=None):
        try:
            key = request.data.get('key')
            query = Q()
            query |= Q(id__icontains=key)
            query |= Q(so_dien_thoai__icontains=key)
            query |= Q(ho_ten__icontains=key)
            query |= Q(dia_chi__icontains=key)
            result = KhachHang.objects.filter(query)
            data_result = KhachHangSerializer(result, many=True).data
            if not data_result:
                raise Exception("không tìm được dữ liệu khách hàng")
            data = KhachHangSerializer(data_result, many=True).data
            return Response(data, status.HTTP_200_OK)
        except Exception as e:
            return Response("Message: " + str(e), status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], detail=True, url_path='update-info')
    def update_info(self, request, pk):
        try:
            khach_hang = KhachHang.objects.get(id=pk)
            if not khach_hang:
                raise Exception('khách hàng không tồn tại')
            if request.data.get('so_dien_thoai'):
                so_dien_thoai = request.data.get('so_dien_thoai')
                if not re.match("^[0-9]+$", so_dien_thoai) or len(so_dien_thoai) != 10:
                    raise Exception('số điện thoại không hợp lệ')
                khach_hang.so_dien_thoai = so_dien_thoai
            if request.data.get('ho_ten'):
                khach_hang.ho_ten = request.data.get('ho_ten')
            if request.data.get('dia_chi'):
                khach_hang.dia_chi = request.data.get('dia_chi')
            if request.data.get('rank'):
                khach_hang.rank = request.data.get('rank')
            khach_hang.save()
            return Response(dict(message="update success"), status.HTTP_200_OK)
        except Exception as e:
            return Response("Message: " + str(e), status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], detail=True, url_path='delete-info')
    def delete_info(self, request, pk):
        try:
            khach_hang = KhachHang.objects.get(id=pk)
            if not khach_hang:
                raise Exception('khách hàng không tồn tại')
            khach_hang.delete()
            return Response(dict(message="delete success"), status.HTTP_200_OK)
        except Exception as e:
            return Response("Message: " + str(e), status.HTTP_400_BAD_REQUEST)


class DsDatBanViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = DsDatBan.objects.all()
    serializer_class = DSDatBanSerialier

    def Check_data(data):
        processed_result = {}
        for item in data:
            ban_id = item['ban_id']
            total_so_luong = item['total_so_luong']
            loai = Ban.objects.get(id=ban_id).loai_ban
            ban_so_luong = Ban.objects.get(id=ban_id).so_luong
            processed_so_luong = ban_so_luong - total_so_luong
            processed_result[ban_id] = ban_id
            processed_result = {'loai': loai, 'total_so_luong': processed_so_luong}
        return processed_result

    @action(methods=['get'], detail=True, url_path="get-by-id")
    def get_by_id(self, request, pk):
        try:
            ban = DsDatBan.objects.get(id=pk)
            serialier_data = DSDatBanSerialier(ban).data
            return Response(serialier_data, status.HTTP_200_OK)
        except Exception as e:
            return Response({"message:" + str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_path="get-ds-dat-ban")
    def get_ds_dat_ban(self, request, pk=None):
        try:
            so_dien_thoai = request.data.get('so_dien_thoai')
            ngay_dat_ban = request.data.get('ngay_dat_ban')
            data = DsDatBan.objects.filter(
                Q(so_dien_thoai=so_dien_thoai) & Q(thoi_gian_dat_ban__date=ngay_dat_ban)).all()
            json_res = DSDatBanSerialier(data, many=True).data
            return Response(json_res, status.HTTP_200_OK)
        except Exception as e:
            return Response({"message: " + str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_path='check-ds-dat-ban-today')
    def ds_dat_ban_today(self, request, pk=None):
        try:
            check_time = datetime.now().date()
            ds_ban = DsDatBan.objects.filter(thoi_gian_nhan_ban__date=check_time).order_by('thoi_gian_nhan_ban')
            serialier_data = DSDatBanSerialier(ds_ban, many=True).data
            return Response(serialier_data, status.HTTP_200_OK)
        except Exception as e:
            return Response({"message:" + str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_path='check-today')
    def Check_today(self, request, pk=None):
        date = datetime.now()
        if date:
            result = []
            time_star = date - timedelta(hours=TIME_CHECK)
            time_end = date
            ban = Ban.objects.filter(is_trang_thai=True).all()
            if not ban:
                return Response({"message": "khong con ban trong"}, status.HTTP_200_OK)
            for item in ban:
                item_date_data = DsDatBan.objects.filter(Q(ban_id=item.id) &
                                                         Q(thoi_gian_nhan_ban__range=(time_star, time_end)) &
                                                         Q(is_trang_thai=False)).all()
                temp = item_date_data.values('ban_id').annotate(total_so_luong=Sum('so_luong_ban'))
                checked = DsDatBanViewSet.Check_data(temp)
                if checked:
                    if checked['total_so_luong'] > 0:
                        result.append(checked)
                else:
                    result.append({'loai': item.loai_ban, 'total_so_luong': item.so_luong})
            return Response(result, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='ngay-nhan')
    def Check_day(self, request, pk=None):
        try:
            ngay_nhan_ban = request.data.get('ngay')
            date = datetime.strptime(ngay_nhan_ban, "%Y-%m-%d %H:%M:%S")

            if ngay_nhan_ban:
                result = []
                time_star = date - timedelta(hours=TIME_CHECK)
                time_end = date
                ban = Ban.objects.filter(is_trang_thai=True).all()
                if not ban:
                    return Response({"message": "khong con ban trong"}, status.HTTP_200_OK)
                for item in ban:
                    item_date_data = DsDatBan.objects.filter(Q(ban_id=item.id) &
                                                             Q(thoi_gian_nhan_ban__range=(time_star, time_end)) &
                                                             Q(is_trang_thai=False)).all()

                    temp = item_date_data.values('ban_id').annotate(total_so_luong=Sum('so_luong_ban'))

                    checked = DsDatBanViewSet.Check_data(temp)
                    if checked:
                        if checked['total_so_luong'] > 0:
                            result.append(checked)
                    else:
                        result.append({'loai': item.loai_ban, 'total_so_luong': item.so_luong})
                return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message:" + str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='them-dat-ban')
    def create_dat_ban(self, request, pk=None):
        try:
            form_data = request.data
            so_dien_thoai = form_data.get('so_dien_thoai')
            ten = form_data.get('ten_nguoi_dat')
            ngay_dat_ban = datetime.now()
            ngay_nhan_ban = form_data.get('ngay_nhan_ban')
            loai_ban = form_data.get('loai_ban')
            so_luong = int(form_data.get('so_luong'))
            mon_an_data = form_data.get('mon_an', [])
            id_ban = Ban.objects.get(loai_ban=loai_ban).id
            ban_active = Ban.objects.get(loai_ban=loai_ban).is_trang_thai
            if not ban_active:
                raise Exception("bàn ngưng hoạt động")
            id_khach_hang = None
            time_allow = None
            if form_data.get('khach_hang'):
                khach_hang = form_data.get('khach_hang')
                id_khach_hang = KhachHang.objects.get(so_dien_thoai=khach_hang).id
            # set start_time để kiểm tra điều kiện
            if so_luong >= COUNT_TABLE_MANY:
                time_allow = ngay_dat_ban + timedelta(days=TIME_BOOK_MANY)
            elif 0 < so_luong < COUNT_TABLE_MANY:
                time_allow = ngay_dat_ban + timedelta(minutes=TIME_BOOK_FEW)
            else:
                raise Exception("Lỗi số lượng bàn")

            # kiểu tra ngày nhận bàn và số lượng bàn
            end_time = ngay_nhan_ban = datetime.strptime(ngay_nhan_ban, "%Y-%m-%d %H:%M:%S")
            if so_luong >= COUNT_TABLE_MANY and time_allow > ngay_nhan_ban:
                raise Exception("Nhận bàn tối thiểu sau {} ngày".format(TIME_BOOK_MANY))
            elif 0 < so_luong < COUNT_TABLE_MANY and time_allow > ngay_nhan_ban:
                raise Exception("Nhận bàn tối thiểu sau {} phút".format(TIME_BOOK_FEW))

            # kiểm tra số lượng order món ăn
            if so_luong >= COUNT_TABLE_MANY and len(mon_an_data) < ORDER_MANY:
                raise Exception("Chưa order đủ số lượng món")
            elif COUNT_TABLE_FEW < so_luong < COUNT_TABLE_MANY and len(mon_an_data) < ORDER_FEW:
                raise Exception("Chưa order đủ số lượng món")
            # add id khách hàng nếu có
            if id_khach_hang:
                new_ds_dat_ban = DsDatBan(so_dien_thoai=so_dien_thoai,
                                          thoi_gian_nhan_ban=ngay_nhan_ban,
                                          thoi_gian_dat_ban=ngay_dat_ban,
                                          so_luong_ban=so_luong,
                                          khach_hang_id=id_khach_hang,
                                          ten_nguoi_dat=ten,
                                          ban_id=id_ban)
            else:
                new_ds_dat_ban = DsDatBan(so_dien_thoai=so_dien_thoai,
                                          thoi_gian_nhan_ban=ngay_nhan_ban,
                                          thoi_gian_dat_ban=ngay_dat_ban,
                                          so_luong_ban=so_luong,
                                          ten_nguoi_dat=ten,
                                          ban_id=id_ban)
            try:
                new_ds_dat_ban.save()
                tong_tien = 0
                dat_ban_id = DsDatBan.objects.get(thoi_gian_dat_ban=ngay_dat_ban).id
                if mon_an_data:
                    for item in mon_an_data:
                        mon = Menu.objects.get(id=item["id"])
                        mon_an_id = mon.id
                        tong_tien += mon.don_gia
                        so_luong = item["so_luong"]
                        new_order = DsOrder(ds_dat_ban_id=dat_ban_id, menu_id=mon_an_id, so_luong=so_luong)
                        new_order.save()
                tong_tien = (tong_tien * PERCENT_TOTAL_BILL) / 100
                hoa_don = HoaDonCocTien(ngay_thanh_toan=ngay_dat_ban, tong_tien=tong_tien, ds_dat_ban_id=dat_ban_id)
                hoa_don.save()
                # serializer_data = HoaDonCocTienSerializer(HoaDonCocTien.objects.get(ngay_thanh_toan=ngay_dat_ban)).data
                return Response({"message": " Created"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"message": "1 = " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "2 = " + str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], detail=True, url_path='nhan-ban')
    def nhan_ban(self, request, pk, *args):
        try:
            ban = DsDatBan.objects.get(id=pk)
            time_request = datetime.now().replace(tzinfo=None)
            time_accept = ban.thoi_gian_nhan_ban.replace(tzinfo=None)
            min_time_accept = None
            max_time_accept = None
            if ban.so_luong_ban >= COUNT_TABLE_MANY:
                min_time_accept = time_accept - timedelta(minutes=LAST_TIME_RECEIVE_BOOK_MANY)
                max_time_accept = time_accept + timedelta(minutes=LAST_TIME_RECEIVE_BOOK_MANY)
            elif 0 < ban.so_luong_ban <= COUNT_TABLE_MANY:
                min_time_accept = time_accept - timedelta(minutes=LAST_TIME_RECEIVE_BOOK_FEW)
                max_time_accept = time_accept + timedelta(minutes=LAST_TIME_RECEIVE_BOOK_FEW)
            if min_time_accept and max_time_accept and min_time_accept <= time_request <= max_time_accept:
                if not ban.is_trang_thai:
                    ban.is_trang_thai = True
                ban.save()
                json_result = DSDatBanSerialier(ban).data
                return Response(json_result, status.HTTP_200_OK)
            else:
                err = f"Không thể nhận bàn sớm hơn {min_time_accept}, trễ hơn {max_time_accept}"
                raise Exception(err)
        except Exception as e:
            return Response("message: " + str(e), status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], detail=True, url_path='update-time-nhan-ban')
    def update_time_accept(self, request, pk):
        try:
            time_request = datetime.strptime(request.data.get('time_update'), "%Y-%m-%d %H:%M:%S")
            time_update = datetime.now().replace(tzinfo=None)
            max_time_allow = None
            min_time_allow = None
            ban = DsDatBan.objects.get(id=pk)
            check = False
            thoi_gian_nhan_ban = ban.thoi_gian_nhan_ban.replace(tzinfo=None)
            if ban.so_luong_ban >= COUNT_TABLE_MANY:
                max_time_allow = thoi_gian_nhan_ban + timedelta(days=LAST_UPDATE_TIME_BOOK_MANY)
                min_time_allow = thoi_gian_nhan_ban - timedelta(days=UPDATE_TIME_BOOK_MANY)
                if time_update <= thoi_gian_nhan_ban - timedelta(days=UPDATE_TIME_BOOK_MANY):
                    check = True
            elif 0 < ban.so_luong_ban <= COUNT_TABLE_MANY:
                max_time_allow = thoi_gian_nhan_ban + timedelta(minutes=LAST_UPDATE_TIME_BOOK_FEW)
                min_time_allow = thoi_gian_nhan_ban - timedelta(minutes=UPDATE_TIME_BOOK_FEW)
                if time_update <= thoi_gian_nhan_ban - timedelta(minutes=UPDATE_TIME_BOOK_FEW):
                    check = True
                # raise Exception(f"dữ liệu so_luong_ban: {ban.so_luong_ban}, time_update = {time_update}")
            # if max_time_allow is None and min_time_allow is None:
            #     raise Exception("dữ liệu None")
            if not check:
                raise Exception("quá thời gian cho phép cập nhật")
            if check and min_time_allow <= time_request <= max_time_allow:
                ban.thoi_gian_nhan_ban = time_request
                ban.save()
                return Response({"message": "update success"}, status.HTTP_200_OK)
            else:
                err = f"Không thể nhận bàn sớm hơn {min_time_allow}, trễ hơn {max_time_allow}"
                raise Exception(err)
        except Exception as e:
            return Response("message: " + str(e), status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], detail=True, url_path='update-ten')
    def update_ten(self, request, pk):
        try:
            ten = request.data.get('ten')
            real_time = datetime.now().replace(tzinfo=None)
            ban = DsDatBan.objects.get(id=pk)
            time = ban.thoi_gian_nhan_ban.replace(tzinfo=None)
            if real_time > time:
                return Response({"message": "đổi tên thất bại"}, status.HTTP_400_BAD_REQUEST)
            if ban:
                ban.ten_nguoi_dat = ten
                ban.save()
                return Response({"message": "update successfull"}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"message:" + str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], detail=True, url_path='update-sdt')
    def update_sdt(self, request, pk):
        try:
            sdt = request.data.get('sdt')
            real_time = datetime.now().replace(tzinfo=None)
            if len(sdt) != 10:
                raise Exception("Số điện thoại không hợp lệ")
            ban = DsDatBan.objects.get(id=pk)
            time = ban.thoi_gian_nhan_ban.replace(tzinfo=None)
            if real_time > time:
                return Response({"message": "đổi số điện thoại thất bại"}, status.HTTP_400_BAD_REQUEST)
            if ban:
                ban.so_dien_thoai = sdt
                ban.save()
                return Response({"message": "update successfull"}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"message:" + str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], detail=True, url_path='update-so-luong-ban')
    def update_so_luong_ban(self, request, pk):
        try:
            new_so_luong = request.data.get('so_luong')
            ban = DsDatBan.objects.get(id=pk)
            time_update = datetime.now().replace(tzinfo=None)
            time_allow = None
            order_allow = 0
            data_request = request.data.get('order', [])
            ds_order = []
            for item in data_request:
                id = Menu.objects.get(ten_san_pham=item["mon"]).id
                ds_order.append({"id": id, "so_luong": item["so_luong"]})
            tong_tien = 0
            thoi_gian_nhan_ban = ban.thoi_gian_nhan_ban.replace(tzinfo=None)
            if 0 < ban.so_luong_ban <= COUNT_TABLE_MANY:
                time_allow = thoi_gian_nhan_ban - timedelta(minutes=TIME_UPDATE_COUNT_TABLE_FEW)
            elif ban.so_luong_ban >= COUNT_TABLE_MANY:
                time_allow = thoi_gian_nhan_ban - timedelta(days=TIME_UPDATE_COUNT_TABLE_MANY)
            if time_update <= time_allow:
                if COUNT_TABLE_FEW < new_so_luong < COUNT_TABLE_MANY:
                    order_allow = ORDER_FEW
                elif new_so_luong >= COUNT_TABLE_MANY:
                    order_allow = ORDER_MANY
                DsDatBanViewSet.update_mon(ds_order, ban, order_allow, new_so_luong, pk=None)
                ban.so_luong_ban = new_so_luong
                ban.save()
            return Response({"message": "Update success"}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"message: " + str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, url_path='load-bill-order')
    def load_bill(self, request, pk):
        try:
            hoa_don = HoaDonCocTien.objects.get(ds_dat_ban_id=pk)
            data = {"tong_tien": hoa_don.tong_tien}
            return Response(data, status.HTTP_200_OK)
        except Exception as e:
            return Response({"message: " + str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], detail=True, url_path='update-order')
    def update_order(self, request, pk):
        try:
            ban = DsDatBan.objects.get(id=pk)
            data_request = request.data.get('order', [])
            ds_order = []
            for item in data_request:
                id = Menu.objects.get(ten_san_pham=item["mon"]).id
                ds_order.append({"id": id, "so_luong": item["so_luong"]})
            order_allow = 0
            thoi_gian_nhan_ban = ban.thoi_gian_nhan_ban.replace(tzinfo=None)
            time_update = datetime.now().replace(tzinfo=None)
            if ban.so_luong_ban < COUNT_TABLE_MANY:
                time_allow = thoi_gian_nhan_ban.replace(tzinfo=None) - timedelta(minutes=TIME_UPDATE_ORDER_FEW)
            else:
                time_allow = thoi_gian_nhan_ban.replace(tzinfo=None) - timedelta(days=TIME_UPDATE_ORDER_MANY)
            if time_update <= time_allow:
                if COUNT_TABLE_FEW < ban.so_luong_ban < COUNT_TABLE_MANY:
                    order_allow = ORDER_FEW
                elif ban.so_luong_ban >= COUNT_TABLE_MANY:
                    order_allow = ORDER_MANY

                DsDatBanViewSet.update_mon(ds_order, ban, order_allow, ban.so_luong_ban)
                return Response({"message": "Update success"}, status.HTTP_200_OK)
            else:
                raise Exception(f"cập nhật không được trễ hơn {time_allow}")
        except Exception as e:
            return Response({"message: " + str(e)}, status.HTTP_400_BAD_REQUEST)

    def update_mon(ds_order, ban, order_allow, new_so_luong, pk=None):
        if ds_order and len(ds_order) >= order_allow:
            try:
                data_ds_order = DsOrder.objects.filter(ds_dat_ban_id=ban.id).all()
                if data_ds_order:
                    for item in ds_order:
                        menu_id = item["id"]
                        so_luong = item["so_luong"]

                        # Kiểm tra xem order đã tồn tại trong old_ds_order hay chưa
                        order_exists = data_ds_order.filter(menu_id=menu_id).first()

                        if order_exists:
                            # Nếu order đã tồn tại, cập nhật số lượng
                            order_exists.so_luong = so_luong
                            order_exists.save()
                        else:
                            # Nếu order chưa tồn tại, tạo mới
                            mon = Menu.objects.get(id=menu_id)
                            new_order = DsOrder(ds_dat_ban_id=ban.id, menu=mon, so_luong=so_luong)
                            new_order.save()
                    # xóa đi order không có trong request
                    old_order = DsOrder.objects.filter(ds_dat_ban_id=ban.id).all()
                    new_order = old_order.exclude(menu_id__in=[item["id"] for item in ds_order])
                    new_order.delete()
                    # Tính tổng tiền
                    tong_tien = 0
                    for item in ds_order:
                        menu_id = item["id"]
                        don_gia = Menu.objects.get(id=menu_id).don_gia
                        so_luong = item["so_luong"]
                        tong_tien += (don_gia * so_luong)
                    # tong_tien = data_ds_order.aggregate(Sum('menu__so_luong'))['menu__don_gia__sum']
                    hoa_don = HoaDonCocTien.objects.get(ds_dat_ban_id=ban.id)
                    if tong_tien != 0:
                        tong_tien = (tong_tien * PERCENT_TOTAL_BILL) / 100

                    if hoa_don:
                        hoa_don = HoaDonCocTien.objects.get(ds_dat_ban_id=ban.id)
                        hoa_don.tong_tien = tong_tien
                        hoa_don.save()
                    else:
                        hoa_don = HoaDonCocTien(ngay_thanh_toan=datetime.now().replace(tzinfo=None),
                                                tong_tien=tong_tien,
                                                ds_dat_ban_id=ban.id)
                        hoa_don.save()

                elif not data_ds_order:
                    if ds_order and len(ds_order) >= order_allow:
                        tong_tien = 0
                        for item in ds_order:
                            mon = Menu.objects.get(id=item["id"])
                            mon_an_id = mon.id
                            tong_tien += mon.don_gia
                            so_luong = item["so_luong"]
                            new_order = DsOrder(ds_dat_ban_id=ban.id, menu_id=mon_an_id, so_luong=so_luong)
                            new_order.save()
                        tong_tien = (tong_tien * PERCENT_TOTAL_BILL) / 100
                        hoa_don = HoaDonCocTien.objects.get(ds_dat_ban_id=ban.id)
                        if hoa_don:
                            hoa_don = HoaDonCocTien.objects.get(ds_dat_ban_id=ban.id)
                            # hoa_don.tong_tien = tong_tien
                            hoa_don.save()
                        else:
                            hoa_don = HoaDonCocTien(ngay_thanh_toan=datetime.now().replace(tzinfo=None),
                                                    tong_tien=tong_tien,
                                                    ds_dat_ban_id=ban.id)
                            hoa_don.save()
                    elif not ds_order and order_allow > 0:
                        raise Exception("order tối thiểu trên {} món".format(order_allow))
            except Exception as e:
                raise Exception("Lỗi: " + str(e))
        elif 0 < new_so_luong <= COUNT_TABLE_FEW:
            old_order = DsOrder.objects.filter(ds_dat_ban_id=ban.id).all()
            old_order.delete()
            hoa_don = HoaDonCocTien.objects.get(ds_dat_ban_id=ban.id)
            hoa_don.tong_tien = 0
            hoa_don.save()
        elif new_so_luong > COUNT_TABLE_FEW:
            raise Exception("order tối thiểu trên {} món".format(order_allow))
        else:
            raise Exception("Lỗi số lượng bàn hoặc danh sách order")

    @action(methods=['put'], detail=True, url_path='huy-dat-ban')
    def huy_dat_ban(self, request, pk):
        try:
            locale.setlocale(locale.LC_ALL, 'vi_VN')
            time_delete = datetime.now().replace(tzinfo=None)
            ban = DsDatBan.objects.get(id=pk)
            time_allow = ban.thoi_gian_nhan_ban.replace(tzinfo=None)
            thoi_gian_nhan_ban = ban.thoi_gian_nhan_ban.replace(tzinfo=None)
            if 0 < ban.so_luong_ban <= COUNT_TABLE_MANY:
                time_allow = thoi_gian_nhan_ban - timedelta(minutes=CANCEL_BOOK_FEW)
            if ban.so_luong_ban >= COUNT_TABLE_MANY:
                time_allow = thoi_gian_nhan_ban - timedelta(days=CANCEL_BOOK_MANY)
            if time_delete <= time_allow:
                # xử lý hoàn cọc
                ban.is_trang_thai = True
                hoa_don = HoaDonCocTien.objects.get(ds_dat_ban_id=ban.id)
                hoa_don.trang_thai = TrangThaiCocTien.HOAN_COC
                tong_tien = locale.currency(hoa_don.tong_tien, grouping=True)
                ban.save()
                hoa_don.save()
                return Response({"message": f"Hoàn lại cọc: {tong_tien}"}, status.HTTP_200_OK)
            else:
                # xử lý hủy cọc
                ban.is_trang_thai = True
                hoa_don = HoaDonCocTien.objects.get(ds_dat_ban_id=ban.id)
                hoa_don.trang_thai = TrangThaiCocTien.HUY_COC
                ban.save()
                hoa_don.save()
                return Response({"message": f"không hoàn cọc do thời gian hoàn cọc trước {time_allow}"},
                                status.HTTP_200_OK)
        except Exception as e:
            return Response({"message: " + str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='get-ds-dat-ban')
    def get_ds_dat_ban(self, request, pk=None):
        try:
            key = request.data.get('key')
            query = Q()
            query |= Q(so_dien_thoai__icontains=key)
            query |= Q(ten_nguoi_dat__icontains=key)
            query |= Q(ma_dat_ban__icontains=key)
            query |= Q(id__icontains=key)
            result = DsDatBan.objects.filter(query)
            if not result:
                raise Exception("Không tồn tại mẫu đặt bàn")
            data_result = DSDatBanSerialier(result, many=True).data
            return Response(data_result, status.HTTP_200_OK)
        except Exception as e:
            return Response({"message: " + str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_path='tim-dat-ban')
    def search_ds_dat_ban(self, request, pk=None):
        data = request.data.get('so_dien_thoai')
        if data:
            result = DsDatBan.objects.filter(so_dien_thoai=data).all()
            serializer = DSDatBanSerialier(result, many=True)
            json_data = serializer.data
            return Response(json_data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_path='ds_dat_ban_theo_ngay')
    def date_ds_dat_ban(self, request, pk=None):
        data = datetime.now().date()
        result = DsDatBan.objects.filter(thoi_gian_nhan_ban__date=data)
        serializer = DSDatBanSerialier(result, many=True)
        json_data = serializer.data
        return Response(json_data, status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=True)
    def del_ds_dat_ban(self, request, pk):
        try:
            ds_dat_ban_id = pk
            temp = DsDatBan.objects.get(id=ds_dat_ban_id)
            temp.delete()
            return Response({"message": "Deleted"}, status=status.HTTP_200_OK)
        except DsDatBan.DoesNotExist:
            return Response({"message": "DsDatBan not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DsOrderViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = DsOrder.objects.all()
    serializer_class = DsOrderSerialier

    @action(methods=['get'], detail=True, url_path='get-order-by-DsDatBan')
    def get_order_by_DsDatBan(self, request, pk=None):
        data_res = []
        try:
            order = DsOrder.objects.filter(ds_dat_ban_id=pk)
            if not order:
                return Response(status=status.HTTP_200_OK)
            for item in order:
                mon = Menu.objects.get(id=item.menu_id)
                if not mon:
                    raise Exception("không tồn tại món ăn")
                data_res.append({"mon": mon.ten_san_pham, "so_luong": item.so_luong})
            return Response(data_res, status.HTTP_200_OK)

        except Exception as e:
            return Response({"message:" + str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='update-order')
    def update_order(self, request, pk=None):
        try:
            tong_tien = 0
            so_dien_thoai = request.data.get('so_dien_thoai')
            order = request.data.get('ds_order', [])
            time_update = datetime.now().replace(tzinfo=None)
            ngay_dat_ban = datetime.strptime(request.data.get('ngay_dat_ban'), "%Y-%m-%d")
            ban = DsDatBan.objects.filter(
                Q(so_dien_thoai=so_dien_thoai) and Q(thoi_gian_dat_ban__date=ngay_dat_ban)).first()
            # Xác định giá trị delta_time dựa trên số lượng bàn
            if ban.so_luong_ban < COUNT_TABLE_MANY:
                delta_time = timedelta(minutes=TIME_UPDATE_ORDER_FEW)
            else:
                delta_time = timedelta(days=TIME_UPDATE_ORDER_MANY)
            time_allow = ban.thoi_gian_nhan_ban.replace(tzinfo=None) - delta_time
            if time_update <= time_allow:
                tong_tien = 0
                ds_order = DsOrder.objects.filter(ds_dat_ban_id=ban.id)
                for item in order:
                    menu_id = item["id"]
                    so_luong = item["so_luong"]

                    # Kiểm tra xem DsOrder đã tồn tại trong ds_order hay chưa
                    order_exists = ds_order.filter(menu_id=menu_id).first()

                    if order_exists:
                        # Nếu DsOrder đã tồn tại, cập nhật số lượng
                        order_exists.so_luong = so_luong
                        order_exists.save()
                    else:
                        # Nếu DsOrder chưa tồn tại, tạo mới
                        mon = Menu.objects.get(id=menu_id)
                        new_order = DsOrder(ds_dat_ban_id=ban.id, menu=mon, so_luong=so_luong)
                        new_order.save()
                # xóa đi order không có trong request
                ds_order.exclude(menu_id__in=[item["id"] for item in order]).delete()
                # Tính tổng tiền
                tong_tien = ds_order.aggregate(Sum('menu__don_gia'))['menu__don_gia__sum']
                if tong_tien != 0:
                    tong_tien = (tong_tien * PERCENT_TOTAL_BILL) / 100
                hoa_don = HoaDonCocTien.objects.get(ds_dat_ban_id=ban.id)
                hoa_don.tong_tien = tong_tien
                hoa_don.save()
                return Response("message: Updated", status=status.HTTP_200_OK)
            else:
                return Response("message: cannot update", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_path='thong-ke-order-today')
    def today(self, request, pk=None):
        try:
            current_time = datetime.now().replace(tzinfo=None).date()
            thong_ke = HoaDonCocTien.objects.filter(ngay_thanh_toan__date=current_time) \
                .values('trang_thai') \
                .annotate(total_tong_tien=Sum('tong_tien'), so_luong=Count('id'))
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='thong-ke-order')
    def thong_ke(self, request, pk=None):
        try:
            ngay_bat_dau = datetime.strptime(request.data.get('ngay_bat_dau'), "%Y-%m-%d").replace(tzinfo=None)
            if request.data.get('ngay_ket_thuc'):
                ngay_ket_thuc = datetime.strptime(request.data.get('ngay_ket_thuc'), "%Y-%m-%d").replace(
                    tzinfo=None)
                if ngay_ket_thuc < ngay_bat_dau:
                    raise Exception("Lỗi thời gian")
                thong_ke = HoaDonCocTien.objects.filter(ngay_thanh_toan__range=(ngay_bat_dau, ngay_ket_thuc)) \
                    .values('trang_thai') \
                    .annotate(total_tong_tien=Sum('tong_tien'), so_luong=Count('id'))
                return Response(thong_ke, status.HTTP_200_OK)
            else:
                thong_ke = HoaDonCocTien.objects.filter(ngay_thanh_toan__date=ngay_bat_dau) \
                    .values('trang_thai') \
                    .annotate(total_tong_tien=Sum('tong_tien'), so_luong=Count('id'))
                return Response(thong_ke, status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class HoaDonThanhToanViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = HoaDonThanhToan.objects.all()
    serializer_class = HoaDonThanhToanSerializer

    @action(methods=['post'], detail=False, url_path='thong-ke-bill')
    def thong_ke_bill(self, request, pk=None):
        try:
            ngay_bat_dau = datetime.strptime(request.data.get('ngay_bat_dau'), "%Y-%m-%d").replace(tzinfo=None)
            if request.data.get('ngay_ket_thuc'):
                ngay_ket_thuc = datetime.strptime(request.data.get('ngay_ket_thuc'), "%Y-%m-%d").replace(tzinfo=None)
                if ngay_ket_thuc < ngay_bat_dau:
                    raise Exception("Lỗi thời gian")
                thong_ke = HoaDonThanhToan.objects.filter(thoi_gian_thanh_toan__range=(ngay_bat_dau, ngay_ket_thuc)) \
                    .aggregate(total_tong_tien=Sum('tong_tien'), total_so_luong=Count('id'))
                return Response(thong_ke, status.HTTP_200_OK)
            else:
                thong_ke = HoaDonThanhToan.objects.filter(thoi_gian_thanh_toan__date=ngay_bat_dau) \
                    .aggregate(total_tong_tien=Sum('tong_tien'), total_so_luong=Count('id'))
                return Response(thong_ke, status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='create-bill')
    def create_bill(self, request, pk=None):
        try:
            real_time = datetime.now().replace(tzinfo=None)
            tong_tien = 0
            ds_mon_an = request.data.get("ds_mon_an", [])
            if request.data.get('voucher'):
                voucher = GiamGia.objects.get(ma_giam_gia=request.data.get('voucher'))
                if not voucher:
                    raise Exception('Mã giảm giá không tồn tại')
            if request.data.get('so_dien_thoai'):
                khach_hang = KhachHang.objects.get(so_dien_thoai=request.data.get('so_dien_thoai'))
                if not khach_hang:
                    raise Exception('Số điện thoại chưa đăng kí thành viên')
            new_bill = HoaDonThanhToan(thoi_gian_thanh_toan=real_time, tong_tien=tong_tien)
            new_bill.save()
            new_bill_id = HoaDonThanhToan.objects.get(thoi_gian_thanh_toan=real_time).id
            for item in ds_mon_an:
                mon = Menu.objects.get(id=int(item["id"]))
                mon_an_id = mon.id
                so_luong = int(item["so_luong"])
                tong_tien += mon.don_gia * so_luong
                new_bill_detail = ChiTietHoaDon(so_luong=so_luong, hoa_don_id=new_bill_id, menu_id=mon_an_id)
                new_bill_detail.save()
            if request.data.get('so_dien_thoai'):
                khach_hang = KhachHang.objects.get(so_dien_thoai=request.data.get('so_dien_thoai'))
                if not khach_hang:
                    raise Exception('Số điện thoại chưa đăng kí thành viên')
                new_bill.khach_hang_id = khach_hang.id
                new_bill.save()
            if request.data.get('voucher'):
                voucher = GiamGia.objects.get(ma_giam_gia=request.data.get('voucher'))
                real_time = datetime.now().date()
                so_luong = voucher.so_luong
                if so_luong is None: so_luong = 1
                max_time_allow = voucher.ngay_bat_dau.date()
                min_time_allow = voucher.ngay_ket_thuc.date()
                if max_time_allow <= real_time <= min_time_allow and so_luong > 0:
                    if voucher.so_tien_giam:
                        tong_tien -= voucher.so_tien_giam
                    elif voucher.ty_le_giam:
                        float_value = float(voucher.ty_le_giam)
                        tong_tien -= tong_tien * float_value
                    new_bill.giam_gia_id = voucher.id
                    if voucher.so_luong is not None:
                        voucher.so_luong = so_luong - 1
                        voucher.save()
                new_bill.tong_tien = tong_tien
                new_bill.save()
            new_bill.tong_tien = tong_tien
            new_bill.save()
            serializer = HoaDonThanhToanSerializer(new_bill)
            data_serialier = serializer.data
            return Response(data_serialier, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
    @action(methods=['get'], detail=False, url_path='thong-ke-doanh-thu-today')
    def today(self, request,pk=None):
        try:
            current_time = datetime.now().replace(tzinfo=None).date()
            thong_ke = HoaDonCocTien.objects.filter(ngay_thanh_toan__date=current_time) \
                .values('trang_thai') \
                .annotate(total_tong_tien=Sum('tong_tien'), so_luong=Count('id'))
            return Response(thong_ke, status.HTTP_200_OK)
        except Exception as e:
            return Response({"message: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['get'], detail=False, url_path='thong-ke-doanh-thu-theo-thang')
    def thong_ke(self, request, pk=None):
        try:
            current_year = datetime.now().replace(tzinfo=None).year
            hoa_don_theo_thang = (
                HoaDonThanhToan.objects
                .filter(thoi_gian_thanh_toan__year=current_year)
                .annotate(thang=ExtractMonth('thoi_gian_thanh_toan'))
                .values('thang')
                .annotate(so_luong=Count('id'))
                .annotate(doanh_thu=Sum('tong_tien'))
                .order_by('thang')
            )
            return Response(hoa_don_theo_thang, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GiamGiaViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = GiamGia.objects.all()
    serializer_class = GiamGiaSerializer

    @action(methods=['post'], detail=False, url_path='create-voucher')
    def create_voucher(self, request, pk=None):
        try:
            time_start = datetime.strptime(request.data.get('time_start'), "%Y-%m-%d %H:%M:%S")
            time_end = datetime.strptime(request.data.get('time_end'), "%Y-%m-%d %H:%M:%S")
            voucher_res = None
            if time_start >= time_end:
                raise Exception("thời gian không hợp lệ")
            if request.data.get('so_tien_giam'):
                tien = request.data.get('so_tien_giam')
                check_voucher = GiamGia.objects.filter(Q(ngay_bat_dau=time_start) &
                                                       Q(ngay_ket_thuc=time_end) &
                                                       Q(so_tien_giam=tien)).first()
                if check_voucher:
                    raise Exception("Voucher đã tồn tại")
                else:
                    new_voucher = GiamGia(ngay_bat_dau=time_start, ngay_ket_thuc=time_end, so_tien_giam=tien)
                if request.data.get('so_luong'):
                    new_voucher.so_luong = int(request.data.get('so_luong'))
                new_voucher.save()
                voucher_res = GiamGia.objects.filter(Q(ngay_bat_dau=time_start) &
                                                     Q(ngay_ket_thuc=time_end) &
                                                     Q(so_tien_giam=tien)).first()
            if request.data.get('ty_le_giam'):
                ty_le = int(request.data.get('ty_le_giam'))
                ty_le /= 100
                check_voucher = GiamGia.objects.filter(Q(ngay_bat_dau=time_start) &
                                                       Q(ngay_ket_thuc=time_end) &
                                                       Q(ty_le_giam=ty_le)).first()
                if check_voucher:
                    raise Exception("Voucher đã tồn tại")
                else:
                    new_voucher = GiamGia(ngay_bat_dau=time_start, ngay_ket_thuc=time_end, ty_le_giam=ty_le)
                if request.data.get('so_luong'):
                    new_voucher.so_luong = int(request.data.get('so_luong'))
                new_voucher.save()
                voucher_res = GiamGia.objects.filter(Q(ngay_bat_dau=time_start) &
                                                     Q(ngay_ket_thuc=time_end) &
                                                     Q(ty_le_giam=ty_le)).first()
            if voucher_res is not None:
                data = GiamGiaSerializer(voucher_res).data
                return Response(data, status=status.HTTP_200_OK)
            else:
                voucher_res = GiamGia.objects.filter(Q(ngay_bat_dau=time_start) &
                                                     Q(ngay_ket_thuc=time_end)).all()
                data = GiamGiaSerializer(voucher_res, many=True).data
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message: " + str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], detail=True, url_path='change-active')
    def change_active(self, request, pk):
        try:
            voucher = GiamGia.objects.get(id=pk)
            if voucher.active:
                voucher.active = False
                voucher.save()
            else:
                voucher.active = True
                voucher.save()
            return Response(dict(message="Update success"), status.HTTP_200_OK)

        except Exception as e:
            return Response({"message: " + str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='search-voucher')
    def search_voucher(self, request, pk=None):
        try:
            key = request.data.get('key')
            query = Q()
            query |= Q(ma_giam_gia__icontains=key)
            query |= Q(ty_le_giam__icontains=key)
            query |= Q(so_tien_giam__icontains=key)
            query |= Q(id__icontains=key)
            result = GiamGia.objects.filter(query).order_by('ngay_ket_thuc')
            data = GiamGiaSerializer(result, many=True).data
            return Response(data, status.HTTP_200_OK)
        except Exception as e:
            return Response({"message: " + str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='check-ma-giam-gia')
    def check_code(self, request, pk=None):
        try:
            code = request.data.get('code')
            voucher = GiamGia.objects.get(ma_giam_gia=code)
            if voucher:
                real_time = datetime.now().date()
                start_date = voucher.ngay_bat_dau.date()
                end_date = voucher.ngay_ket_thuc.date()
                is_active = voucher.active
                so_luong = voucher.so_luong
                if so_luong is None: so_luong = 1
                if start_date <= real_time <= end_date and is_active is True and so_luong > 0:
                    return Response({"message: Mã giảm giá còn sử dụng được"}, status.HTTP_200_OK)
                else:
                    return Response({"message: Mã giảm giá hết hiệu lực"}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"message: " + str(e)}, status.HTTP_400_BAD_REQUEST)


class ChiTietHoaDonViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = ChiTietHoaDon.objects.all()
    serializer_class = ChiTietHoaDonSerializer

    @action(methods=['post'], detail=False, url_path='thong-ke-mon-an-today')
    def today(self, request, pk=None):
        try:
            current_time = datetime.now().replace(tzinfo=None).date()
            thong_ke_mon_an = (
                ChiTietHoaDon.objects
                .filter(hoa_don__thoi_gian_thanh_toan__date=current_time)
                .values('menu__ten_san_pham')
                .annotate(tong_so_luong=Sum('so_luong'))
            )
        except Exception as e:
            return Response({"message: " + str(e)}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='thong-ke-mon-an-theo-thang')
    def thong_ke_theo_thang(self, request, pk=None):
        try:
            thang = request.data.get('thang')
            current_year = datetime.now().replace(tzinfo=None).year
            thong_ke_mon_an = (
                ChiTietHoaDon.objects
                .filter(hoa_don__thoi_gian_thanh_toan__year=current_year,
                        hoa_don__thoi_gian_thanh_toan__month=thang)
                .values('menu__ten_san_pham')
                .annotate(tong_so_luong=Sum('so_luong'))
            )
            # Tính toán tổng doanh thu bên ngoài truy vấn
            for item in thong_ke_mon_an:
                menu = Menu.objects.get(ten_san_pham=item['menu__ten_san_pham'])
                doanh_thu = menu.don_gia * item['tong_so_luong']
                item['doanh_thu'] = doanh_thu
            return Response(thong_ke_mon_an, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_path='thong-ke-mon-an-theo-nam')
    def thong_ke_theo_nam(self, request, pk=None):
        try:
            current_year = datetime.now().replace(tzinfo=None).year
            thong_ke_mon_an = (
                ChiTietHoaDon.objects
                .filter(hoa_don__thoi_gian_thanh_toan__year=current_year)
                .values('menu__ten_san_pham')
                .annotate(tong_so_luong=Sum('so_luong'))
            )
            # Tính toán tổng doanh thu bên ngoài truy vấn
            for item in thong_ke_mon_an:
                menu = Menu.objects.get(ten_san_pham=item['menu__ten_san_pham'])
                doanh_thu = menu.don_gia * item['tong_so_luong']
                item['doanh_thu'] = doanh_thu
            thong_ke_mon_an = sorted(thong_ke_mon_an, key=lambda x: x['tong_so_luong'], reverse=True)
            return Response(thong_ke_mon_an, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
