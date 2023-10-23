import { HttpServerService } from './../Services/http-server.service';
import { Component, OnInit } from '@angular/core';
import { CurrencyPipe } from '@angular/common';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { of } from 'rxjs';
import { FileUploadModule } from 'ng2-file-upload';
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  constructor(
    private fb: FormBuilder,
    private httpServerServices: HttpServerService,
    private currencyPipe: CurrencyPipe,

    ){};
  public uploader: FileUploadModule = new FileUploadModule();
  public data_server: any[] = [];
  public menu: any[] = [];
  public search_menu: any[] = []
  public menu_options: any[] = [];
  public key: string = '';
  public bill_menu:any[] = [];
  public trang_thai: string = '';
  public so_dien_thoai: string='';
  public tong_tien: number = 0;
  public voucher: string = '';
  public alert:any;
  public tien_nhan: number = 0;
  public tien_thoi: number = 0
  public ngOnInit(): void {
    console.log(this.bill_menu);
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

    console.log(item);
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
  }
  public xoa(item: any): void{
    this.bill_menu = this.bill_menu.filter(element => element !== item);
    this.tong_tien = 0;
    for (let i of this.bill_menu) {
      this.tong_tien += i.don_gia * i.so_luong;
    }
  }

  public change(event:any, item:any){
    let num = parseInt(event.target.value)
    this.tong_tien = 0
    item.so_luong = num;
    for (let i of this.bill_menu){
      this.tong_tien += i.don_gia * i.so_luong
    }
  }
  public submit(){
    let data = [];
    for(let item of this.bill_menu){
      data.push({"id": item.id, "so_luong": item.so_luong})
    }
    let payload = {}
    if(this.so_dien_thoai !=='' && this.voucher !== ''){
      payload = {"ds_mon_an": data, "so_dien_thoai": this.so_dien_thoai, "voucher": this.voucher}
    }
    else if(this.voucher !== ''){
      payload = {"ds_mon_an": data,"voucher": this.voucher}
    }
    else if(this.so_dien_thoai !==''){
      payload = {"ds_mon_an": data, "so_dien_thoai": this.so_dien_thoai}
    }
    else
      payload = {"ds_mon_an": data}
    if(data.length > 0){
      this.httpServerServices.thanhToan(payload).subscribe(data => {
        this.tong_tien = data.tong_tien
        // window.location.reload();
      })
    }
    else{
      this.alert ="chưa chọn món để thanh toán"
    }
  }
  public tien(event: any){
    let num = parseInt(event.target.value)
    if(num > 0){
      this.tien_nhan = num
      if(this.tien_nhan >= this.tong_tien)
        this.tien_thoi = this.tien_nhan - this.tong_tien
    }
    else this.tien_nhan = 0

  }
  public check_code(code: string):void{
    const data = {"code": code}
    this.httpServerServices.checkVoucher(data).subscribe((response) => {
      alert(response)
    },
    (error) => {
      alert(error.error)
      console.error('Lỗi: ', error);
    })
  }
  public xacNhan(): void{
    window.location.reload();
  }
}
