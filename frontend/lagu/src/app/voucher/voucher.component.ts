import { Component, OnInit } from '@angular/core';
import { HttpServerService } from '../Services/http-server.service';
import { Router } from '@angular/router';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-voucher',
  templateUrl: './voucher.component.html',
  styleUrls: ['./voucher.component.css']
})
export class VoucherComponent implements OnInit{
  constructor(
    private httpServerServices: HttpServerService,
    private router: Router,
    private datePipe: DatePipe
    ){};
    public time_start:string= '';
    public time_end:string= '';
    public so_tien_giam:number = 0;
    public phan_tram_giam:number = 0;
    public so_luong:number = 0;
    public new_voucher: string='';
    public search_voucher:any[] = [];
    public key:string = '';
  ngOnInit(): void {
  }
  public check_tien(): boolean {
    if (this.phan_tram_giam > 0) {
      return true;
    }
    return false;
  }
  public check_phan_tram(): boolean {
    if (this.so_tien_giam > 0) {
      return true;
    }
    return false;
  }
  public taoVoucher(): void{
    const start = this.datePipe.transform(this.time_start, 'yyyy-MM-dd HH:mm:ss');
    const end = this.datePipe.transform(this.time_end, 'yyyy-MM-dd HH:mm:ss');
    let payload:any;
    if((start !== null && start !== undefined) && (end !== null && end !== undefined)){
      if(this.so_luong!== 0){
        if(this.so_tien_giam !== 0){
          payload = {
            "time_start": start,
            "time_end": end,
            "so_tien_giam":this.so_tien_giam,
            "so_luong": this.so_luong
          }
        }
        if(this.phan_tram_giam !== 0){
          payload = {
            "time_start": start,
            "time_end": end,
            "so_luong":this.so_luong,
            "ty_le_giam": this.phan_tram_giam
          }
        }
      }
      else{
        if(this.so_tien_giam !== 0){
          payload = {
            "time_start": start,
            "time_end": end,
            "so_tien_giam":this.so_tien_giam
          }
        }
        if(this.phan_tram_giam !== 0){
          payload = {
            "time_start": start,
            "time_end": end,
            "ty_le_giam":this.phan_tram_giam
          }
        }
      }
    }
    console.log(payload)
    this.httpServerServices.createVoucher(payload).subscribe( (data) =>{
      this.new_voucher = data.ma_giam_gia
      alert(this.new_voucher);
    },
    (error) => {
      alert(error.error)
    })
  }
  public searchVoucher(): void{
    if (this.key !== ''){
      let data = {"key": this.key}
      this.httpServerServices.searchVoucher(data).subscribe( (data) =>{
        this.search_voucher = data
        console.log(this.search_voucher)
      },
      (error) => {
        alert(error.error)
      })
    }
  }
  public changeActive(id: any): void {
    this.httpServerServices.changeActive(id).subscribe( (data) =>{
      alert(data.message)
      window.location.reload()
    },(error) => {
      console.log(error)
    })
  }

}
