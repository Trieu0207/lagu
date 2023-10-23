import { Component, OnInit } from '@angular/core';
import { HttpServerService } from '../Services/http-server.service';
import { CurrencyPipe, DatePipe } from '@angular/common';

@Component({
  selector: 'app-dat-ban',
  templateUrl: './dat-ban.component.html',
  styleUrls: ['./dat-ban.component.css']
})
export class DatBanComponent implements OnInit{
  constructor(
    private httpServerServices: HttpServerService,
    private currencyPipe: CurrencyPipe,
    private datePipe: DatePipe
    ){};
    public data_server: any[] = [];
    public menu: any[] = [];
    public search_menu: any[] = []
    public menu_options: any[] = [];
    public key: string = '';
    public bill_menu:any[] = [];
    public so_dien_thoai: string='';
    public ten_nguoi_dat: string='';
    public tong_tien: number = 0;
    public so_luong: number = 0;
    public date = new Date();
    public ngay_nhan:string = this.date.toLocaleDateString();
    public loai: string = '';
    public ban_trong:any[] = [];
    public ten:string = '';
    public timeString: string ='';
    public warning: string = '';
    public check_so_luong_ban:boolean = false;
    public checkSubmit: boolean = false;
    public ngOnInit(): void {
      this.httpServerServices.getBanTrongToday().subscribe((data) => {
        this.ban_trong = data
      })
      this.httpServerServices.getMenu().subscribe((data) => {
        this.data_server = data
        this.menu = this.data_server
      });
      if (this.search_menu.length > 0){
        this.menu = this.search_menu
      }
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

      // console.log(item);
      let bol: boolean = false;

      for (let i of this.bill_menu) {
          if (item.id === i.id) {
              i.so_luong += 1;
              bol = true;
          }
      }

      if (!bol) {
        if (typeof item === 'object') {
          item['so_luong'] = 1;
        }
        this.bill_menu.push(item);
      }
      this.tong_tien = 0
      for (let i of this.bill_menu) {
        this.tong_tien += i.don_gia * i.so_luong;
      }
      this.tong_tien *= 0.4
    }
    public xoa(item: any): void{
      this.bill_menu = this.bill_menu.filter(element => element !== item);
      this.tong_tien = 0;
      for (let i of this.bill_menu) {
        this.tong_tien += i.don_gia * i.so_luong;
      }
      this.tong_tien *= 0.4
    }
    public getBanTrong(date: string): void{
      const formattedDateTime = this.datePipe.transform(date, 'yyyy-MM-dd HH:mm:ss');
      let date_string: string = '';
      if (formattedDateTime !== null && formattedDateTime !== undefined) {
         date_string = formattedDateTime.toString();
         const data = {"ngay": date_string}
          this.httpServerServices.getBanTrong(data).subscribe((data) =>{
            this.ban_trong = data;
          })
        }
        alert("date was checked")

    }
    public change(event:any, item:any){
      let num = parseInt(event.target.value)
      this.tong_tien = 0
      item.so_luong = num;
      for (let i of this.bill_menu){
        this.tong_tien += i.don_gia * i.so_luong
      }
      this.tong_tien *= 0.4
    }
    public submit(){
      const formattedDateTime = this.datePipe.transform(this.ngay_nhan, 'yyyy-MM-dd HH:mm:ss');
      let date_string: string = '';
      if (formattedDateTime !== null && formattedDateTime !== undefined &&
          this.so_dien_thoai !== '' && this.ten !== '') {
        date_string = formattedDateTime.toString();
        const data ={
          "so_dien_thoai" : this.so_dien_thoai,
          "ngay_nhan_ban": date_string,
          "so_luong": this.so_luong,
          "ten_nguoi_dat": this.ten,
          "loai_ban": this.loai,
          "mon_an": this.bill_menu

        }
        this.httpServerServices.postDatHang(data).subscribe((response) => {
          alert(response.message)
          window.location.reload();
        },
        (error) => {
          alert(error.error.message);

          console.error('Lỗi: ', error);
        })
      }
      else {alert('nhập thiếu thông tin');}

    }
    public dateFormat(event: any): void{
      const formattedDateTime = this.datePipe.transform(this.ngay_nhan, 'yyyy-MM-dd HH:mm:ss');
      if (formattedDateTime !== null && formattedDateTime !== undefined){
        this.timeString = formattedDateTime.toString();
      }
      console.log(event.target.value)
    }
    public changeSoLuongBan(event: any): void {
      for(let item of this.ban_trong){
        if(this.loai == item.loai && this.so_luong > item.total_so_luong){
          // alert(this.loai)
          this.warning = "vượt quá số lượng bàn đang có"
        }
        else this.warning = ""
      }
    }
    public checkSoLuongBan(): boolean {
      for(let item of this.ban_trong){
        if(this.loai == item.loai && this.so_luong > item.total_so_luong){
          // alert(this.loai)
          console.log(item.total_so_luong)
          this.warning = "Số lượng bàn không được phép"
          this.checkSubmit = false
          return false
          console.log(this.checkSubmit)
        }
      }
      if(this.so_luong > 0){
        this.checkSubmit = true
      }
      return true
      console.log(this.checkSubmit)
    }
    public setMaxValue():number{
      for(let item of this.ban_trong){
        if(this.loai == item.loai){
          return item.total_so_luong
        }
      }
      return 0
    }







}
