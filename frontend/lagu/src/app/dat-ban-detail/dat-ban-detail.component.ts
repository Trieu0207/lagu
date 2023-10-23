import { Component, OnInit } from '@angular/core';
import { HttpServerService } from '../Services/http-server.service';
import { ActivatedRoute, Router } from '@angular/router';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-dat-ban-detail',
  templateUrl: './dat-ban-detail.component.html',
  styleUrls: ['./dat-ban-detail.component.css']
})
export class DatBanDetailComponent implements OnInit{
  constructor(
    private httpServerServices: HttpServerService,
    private route: ActivatedRoute,
    private router: Router,
    private datePipe: DatePipe
  ){}
  public ban_id = this.route.snapshot.paramMap.get('id');
  public ban_info: any={};
  public ds_mon: any[] = [];
  public data_server: any[] = [];
  public menu: any[] = [];
  public search_menu: any[] = []
  public menu_options: any[] = [];
  public ten:string = '';
  public key: string = '';
  public bill_menu:any[] = [];
  public sdt: string = '0';
  public ngay: any;
  public so_luong:number = 0;
  public date = new Date();
  public checkTime = true;
  public tong_tien: number = 0;
  ngOnInit(): void {
    this.httpServerServices.getDsDatBan(this.ban_id).subscribe((data)=>{
      this.ban_info = data;
      this.so_luong = this.ban_info.so_luong_ban;
      this.httpServerServices.getTongOrder(this.ban_id).subscribe((data)=>{
        this.tong_tien = data.tong_tien;
      });
      // if (data.menus.length >0){
      //   for(let item of data.menus){
      //     this.httpServerServices.getMon(item).subscribe((data)=>{
      //       this.ds_mon.push(data);
      //     })
      // }
      // }
      this.httpServerServices.getOrderByDsDatBan(data.id).subscribe((data)=>{
        if(data){
          this.ds_mon = data;
        }
      })
      this.httpServerServices.getMenu().subscribe((data) => {
        this.data_server = data
        this.menu = this.data_server
      });
      if (this.search_menu.length > 0){
        this.menu = this.search_menu
      }
    })
  }
  public getMenu(): void{
    console.log(this.key)
    this.search_menu = [];
    if(this.key.toLowerCase() === 'mon_an' || this.key.toLowerCase() == 'mon_nuoc' ||this.key.toLowerCase() == 'trang_mieng'){
      for(let item of this.data_server){
        if(item.loai.toLowerCase().includes(this.key.toLowerCase())){
          this.search_menu.push(item)
        }
      }
    }
    else{
      for(let item of this.data_server){
        if(item.ten_san_pham.toLowerCase().includes(this.key.toLowerCase())){
          this.search_menu.push(item)
        }
      }
    }
      if(this.search_menu.length > 0 && this.key != ""){
        this.menu = this.search_menu
      }
      else
        this.menu = this.data_server;
  }
  public them(item: any): void{
    let bol: boolean = false;

    if(this.ds_mon !== null){
      for (let i of this.ds_mon) {
        if (item.ten_san_pham === i.mon) {
            i.so_luong += 1;
            bol = true;
        }
    }
    }
    if (!bol) {
      if (typeof item === 'object') {
        item['so_luong'] = 1;
        item['mon'] = item.ten_san_pham;
      }
      this.ds_mon.push({'mon': item.ten_san_pham,'so_luong': 1 });
    }
  }
  public xoa(item: any): void{
    this.ds_mon = this.ds_mon.filter(element => element !== item);
    console.log(this.ds_mon);
  }
  public onInputChange(event: any): void{
    const inputElement = event.target as HTMLInputElement;
    const inputValue = inputElement.value;

    // Kiểm tra xem giá trị nhập có phải là số
    if (/^\d*$/.test(inputValue)) {
      this.sdt = inputValue;
    } else {
      // Nếu giá trị không phải là số, gán lại giá trị trước đó
      inputElement.value = this.sdt = inputElement.value.slice(0, -1);
    }
  }
  public updateSdt():void{
    if(this.sdt.length == 10){
      let id = this.route.snapshot.paramMap.get('id');
      let payload = {"sdt": this.sdt}
      this.httpServerServices.updateSdt(id, payload).subscribe(
        (data)=>{
        alert(data.message);
        window.location.reload();
      },
      (error) => {
        // Xử lý khi xảy ra lỗi khi tải lên
        alert(error.message)
        console.log(error.message)
      })
    }
    else{
      alert("Số điện thoại không hợp lệ")
    }

  }
  public updateTen():void{
    if(this.ten !== ''){
      let id = this.route.snapshot.paramMap.get('id');
      let payload = {"ten": this.ten}
      this.httpServerServices.updateTen(id, payload).subscribe(
        (data)=>{
        alert(data.message);
        window.location.reload();
      },
      (error) => {
        // Xử lý khi xảy ra lỗi khi tải lên
        alert(error.message)
        console.log(error.message)
      })
    }
    else{
      alert("Tên không hợp lệ")
    }

  }
  public updateTime(){
    const formattedDateTime = this.datePipe.transform(this.ngay, 'yyyy-MM-dd HH:mm:ss');
    let id = this.route.snapshot.paramMap.get('id');
    if (formattedDateTime !== null && formattedDateTime !== undefined) {
      let data = {"time_update": formattedDateTime}
      this.httpServerServices.updateTime(id, data).subscribe(
        (data)=>{
        alert(data.message);
        window.location.reload();
      },
      (error) => {
        // Xử lý khi xảy ra lỗi khi tải lên
        alert(error.error)
      })
      // date_string = formattedDateTime.toString();
      // const data = {"ngay": date_string}
      //  this.httpServerServices.getBanTrong(data).subscribe((data) =>{
      //    this.ban_trong = data;
      //  })
      console.log(data)
     }
  }
  public inputOrder(event: any, item: any): void {
    item.so_luong = parseInt(event.target.value)
  }
  public checkInput(){
    if(this.so_luong > 2 && this.so_luong < 6){
      if(this.ds_mon.length < 2)
        console.log(this.so_luong);
    }
    else if(this.so_luong >= 6 && this.ds_mon.length < 4){
      return false;
    }
    return true
  }
  public changeOrder(){
    let id = this.route.snapshot.paramMap.get('id');
    let data: any = {"order": this.ds_mon}
    this.httpServerServices.updateDsOrder(id, data).subscribe(
      (data) =>{
        alert(data.message);
        window.location.reload();
      },
      (error) => {
        // Xử lý khi xảy ra lỗi khi tải lên
        alert(error.error)
      })
  }
  public change_so_luong_ban(){
    let id = this.route.snapshot.paramMap.get('id');
    let data: any = {"so_luong": this.so_luong, "order": this.ds_mon}
    this.httpServerServices.updateBan(id, data).subscribe(
      (data) =>{
        alert(data.message);
        window.location.reload();
      },
      (error) => {
        // Xử lý khi xảy ra lỗi khi tải lên
        alert(error.message)
        console.log(error)
      })
  }
  public checkChange(): boolean{
    if(this.so_luong > 0 && this.so_luong <= 2){
      return false;
    }
    else if(this.so_luong > 2 && this.so_luong < 6){
      if(this.ds_mon.length < 2)
        return true;
      else
        return false;
    }
    else if(this.so_luong >= 6 && this.ds_mon.length < 4){
      return true;

    }
    else if(this.so_luong >= 6 && this.ds_mon.length >= 4){
      return false;

    }
    return true;
  }
  public checkDel(): boolean{
    if(this.so_luong > 0 && this.so_luong <= 2){
      return false;
    }
    else if(this.so_luong > 2 && this.so_luong < 6){
      if(this.ds_mon.length <= 2)
        return true;
      else
        return false;
    }
    else if(this.so_luong >= 6 && this.ds_mon.length <= 4){
      return true;

    }
    return false;
  }
  public nhanBan(): void {
    let id = this.route.snapshot.paramMap.get('id');
    this.httpServerServices.nhanBan(id).subscribe((response) => {
      // Xử lý khi tải lên thành công
      alert(response.message)
      window.location.reload();
    },
    (error) => {
      // Xử lý khi xảy ra lỗi khi tải lên
      alert(error.error)
      console.error('Lỗi: ', error);
    });
  }
  public huyDatBan():void{
    let id = this.route.snapshot.paramMap.get('id');
    this.httpServerServices.huyDatBan(id).subscribe((response) => {
      // Xử lý khi tải lên thành công
      alert(response.message)
      window.location.reload();
    },
    (error) => {
      // Xử lý khi xảy ra lỗi khi tải lên
      alert(error.error)
      console.error('Lỗi: ', error);
    })
  }
  public checkTrangThai(): boolean {
    if(this.ban_info.is_trang_thai == true){
      return true;
    }
    return false;
  }
  public quaylai():void {
    this.router.navigateByUrl('/nhan-ban');
  }





}
