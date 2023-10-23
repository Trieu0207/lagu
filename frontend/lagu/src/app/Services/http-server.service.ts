import { HttpClient, HttpParams, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, catchError, pipe, throwError } from 'rxjs';
import { HttpHeaders } from '@angular/common/http';
@Injectable({
  providedIn: 'root'
})
export class HttpServerService {
  private REST_API_URL = 'http://localhost:8000/';
  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    })
    // headers2: new HttpHeaders({
    //   'Content-Type': 'multipart/form-data' ,
    //   'Accept': 'application/json', // Correct header key
    // }),
  };
  constructor(private httpClient: HttpClient) { }
  public getBan(): Observable<any> {
    const url = `${this.REST_API_URL}/ban`;
    return this.httpClient.get<any>(url, this.httpOptions)
  }
  public getMon(payload: any): Observable<any> {
    const url = `${this.REST_API_URL}/menu/${payload}`;
    return this.httpClient.get<any>(url, this.httpOptions)
  }
  public getOrderByDsDatBan(payload: any): Observable<any> {
    const url = `${this.REST_API_URL}/DsOrder/${payload}/get-order-by-DsDatBan/`;
    return this.httpClient.get<any>(url, this.httpOptions)
  }
  public getMenu(){
    const url = `${this.REST_API_URL}/menu`;
    return this.httpClient.get<any>(url, this.httpOptions);
  }
  public getActiveMenu(){
    const url = `${this.REST_API_URL}/menu`;
    return this.httpClient.get<any>(url, this.httpOptions);
  }
  public getDetailMenu(payload: any): Observable<any>{
    const url = `${this.REST_API_URL}/menu/` + payload;
    return this.httpClient.get<any>(url, this.httpOptions);
  }
  public getDetailMenu2(payload: any): Observable<HttpResponse<any>>{
    const url = `${this.REST_API_URL}/menu/` + payload;
    return this.httpClient.get(url, { ...this.httpOptions, observe: 'response' });
  }
  public updateDetailMenu(payload: any, data: any): Observable<any>{
    const url = `${this.REST_API_URL}/menu/` + payload +`/update-menu/`;
    return this.httpClient.put(url,data);
  }
  public upAnh(payload: any, data: any): Observable<any>{
    const url = `${this.REST_API_URL}/menu/` + payload + '/up-hinh/';
    return this.httpClient.post(url, data);
  }
  public delMenu(payload: any,): Observable<HttpResponse<any>>{
    const url = `${this.REST_API_URL}/menu/` + payload;
    return this.httpClient.delete(url, { ...this.httpOptions, observe: 'response' });

  }
  public changeTrangThai(payload: any): Observable<any>{
    const url = `${this.REST_API_URL}/menu/update-trang-thai/`;
    return this.httpClient.post<any>(url,payload);
  }
  public postMenu(payload: any): Observable<any>{
    const payloadString = JSON.stringify(payload);
    const url = `${this.REST_API_URL}/menu/`;
    return this.httpClient.post<any>(url, payload);
  }
  public thanhToan(payload: any): Observable<any>{
    const payloadString = JSON.stringify(payload);
    const url = `${this.REST_API_URL}/thanhToan/create-bill/`;
    return this.httpClient.post<any>(url, payloadString, this.httpOptions);
  }
  public postDatHang(payload: any): Observable<any>{
    const payloadString = JSON.stringify(payload);
    const url = `${this.REST_API_URL}/dsDatBan/them-dat-ban/`;
    return this.httpClient.post<any>(url, payloadString, this.httpOptions);
  }
  public getDsDatBanToday(): Observable<any>{
    const url = `${this.REST_API_URL}/dsDatBan/check-ds-dat-ban-today/`;
    return this.httpClient.get<any>(url,this.httpOptions);
  }
  public getDsDatBanToday2(): Observable<any>{
    const url = `${this.REST_API_URL}/dsDatBan/check-ds-dat-ban-today-2/`;
    return this.httpClient.get<any>(url,this.httpOptions);
  }
  public getDsDatBan(payload: any): Observable<any>{
    const url = `${this.REST_API_URL}/dsDatBan/`+ payload +`/get-by-id/`;
    return this.httpClient.get<any>(url,this.httpOptions);
  }
  public createMenu(payload: any): Observable<any>{
    const payloadString = JSON.stringify(payload);
    const url = `${this.REST_API_URL}/menu/create-menu/`;
    return this.httpClient.post<any>(url, payload);
  }
  public postData(payload: any): Observable<any>{
    const url = `${this.REST_API_URL}/menu/`;
    console.log("url =", url);
    console.log("post data: payload", payload);
    return this.httpClient.post<any>(url, payload, this.httpOptions);
  }
  public nhanBan(payload: any): Observable<any>{
    const url = `${this.REST_API_URL}/dsDatBan/${payload}/nhan-ban/`;
    return this.httpClient.put<any>(url, this.httpOptions)
  }
  public getBanTrong(payload: any):Observable<any>{
    const url = `${this.REST_API_URL}/dsDatBan/ngay-nhan/`;
    return this.httpClient.post<any>(url,payload, this.httpOptions);
  }public getBanTrongToday():Observable<any>{
    const url = `${this.REST_API_URL}/dsDatBan/check-today/`;
    return this.httpClient.get<any>(url, this.httpOptions);
  }
  public checkVoucher(payload: any):Observable<any>{
    const url = `${this.REST_API_URL}/GiamGia/check-ma-giam-gia/`;
    return this.httpClient.post<any>(url,payload, this.httpOptions);
  }
  public getBanTrong2(payload: any): Observable<any> {
    // Tạo một đối tượng HttpParams để chứa các query parameters
    let params = new HttpParams();

    // Thêm query parameters từ payload vào params
    if (payload) {
      // Ví dụ: Thêm một query parameter 'key' từ payload
      params = params.set('key', payload.key);
      // Thêm các query parameters khác từ payload vào params nếu cần
    }

    // Định nghĩa HttpOptions (nếu cần thiết)
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      }),
      params: params
    };

    const url = `${this.REST_API_URL}/DsDatBan`;

    // Gửi yêu cầu GET với các query parameters và HttpOptions
    return this.httpClient.get<any>(url, httpOptions);
  }
  public updateSdt(id:any, payload:any):Observable<any> {
    const url = `${this.REST_API_URL}/dsDatBan/${id}/update-sdt/`;
    return this.httpClient.put<any>(url,payload, this.httpOptions)
  }
  public updateTen(id:any, payload:any):Observable<any> {
    const url = `${this.REST_API_URL}/dsDatBan/${id}/update-ten/`;
    return this.httpClient.put<any>(url,payload, this.httpOptions)
  }
  public updateTime(id:any, payload:any):Observable<any> {
    const url = `${this.REST_API_URL}/dsDatBan/${id}/update-time-nhan-ban/`;
    return this.httpClient.put<any>(url,payload, this.httpOptions)
  }
  public updateBan(id: any, payload: any):Observable<any> {
    const url = `${this.REST_API_URL}/dsDatBan/${id}/update-so-luong-ban/`;
    return this.httpClient.put<any>(url,payload, this.httpOptions)
  }
  public updateDsOrder(id: any, payload: any):Observable<any> {
    const url = `${this.REST_API_URL}/dsDatBan/${id}/update-order/`;
    return this.httpClient.put<any>(url,payload, this.httpOptions)
  }
  public getTongOrder(id: any): Observable<any> {
    const url = `${this.REST_API_URL}/dsDatBan/${id}/load-bill-order/`;
    return this.httpClient.get<any>(url, this.httpOptions)
  }
  public huyDatBan(id: any): Observable<any> {
    const url = `${this.REST_API_URL}/dsDatBan/${id}/huy-dat-ban/`;
    return this.httpClient.put<any>(url, this.httpOptions)
  }
  public searchDatBan(data: any): Observable<any> {
    const url = `${this.REST_API_URL}/dsDatBan/get-ds-dat-ban/`;
    return this.httpClient.post<any>(url,data, this.httpOptions)
  }
  public createVoucher(data: any): Observable<any> {
    const url = `${this.REST_API_URL}/GiamGia/create-voucher/`;
    return this.httpClient.post<any>(url,data, this.httpOptions)
  }
  public searchVoucher(data: any): Observable<any> {
    const url = `${this.REST_API_URL}/GiamGia/search-voucher/`;
    return this.httpClient.post<any>(url,data, this.httpOptions)
  }
  public changeActive(id: any): Observable<any> {
    const url = `${this.REST_API_URL}/GiamGia/${id}/change-active/`;
    return this.httpClient.put<any>(url, this.httpOptions)
  }
  public loadDsBan(): Observable<any> {
    const url = `${this.REST_API_URL}/ban/get-ds-ban/`;
    return this.httpClient.get<any>(url, this.httpOptions)
  }
  public addBan(data: any): Observable<any> {
    const url = `${this.REST_API_URL}/ban/create-table/`;
    return this.httpClient.post<any>(url,data, this.httpOptions)
  }
  public changeActiveBan(id: any): Observable<any> {
    const url = `${this.REST_API_URL}/ban/${id}/change-active/`;
    return this.httpClient.put<any>(url,this.httpOptions)
  }
  public updateInfo(id: any, payload:any): Observable<any> {
    const url = `${this.REST_API_URL}/ban/${id}/update-info/`;
    return this.httpClient.put<any>(url,payload, this.httpOptions)
  }
  public thongKeDoanhThu(): Observable<any> {
    const url = `${this.REST_API_URL}/thanhToan/thong-ke-doanh-thu-theo-thang/`;
    return this.httpClient.get<any>(url, this.httpOptions)
  }
  public thongKeMonAnTheoThang(thang:any): Observable<any> {
    const url = `${this.REST_API_URL}/thanhToan/thong-ke-doanh-thu-theo-thang/`;
    return this.httpClient.post<any>(url, this.httpOptions)
  }
  public getKhachHang(payload:any): Observable<any> {
    const url = `${this.REST_API_URL}/khachHang/khach-hang-info/`;
    return this.httpClient.post<any>(url, payload, this.httpOptions)
  }
  public createKhachHang(payload:any): Observable<any> {
    const url = `${this.REST_API_URL}/khachHang/create-khach-hang/`;
    return this.httpClient.post<any>(url, payload, this.httpOptions)
  }
  public updateKhachHang(id:number,payload:any): Observable<any> {
    const url = `${this.REST_API_URL}/khachHang/${id}/update-info/`;
    return this.httpClient.put<any>(url, payload, this.httpOptions)
  }
  public deleteKhachHang(id:any): Observable<any> {
    const url = `${this.REST_API_URL}/khachHang/${id}/delete-info/`;
    return this.httpClient.delete<any>(url, this.httpOptions)
  }
}
