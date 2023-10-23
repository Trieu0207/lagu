import { Component, OnInit } from '@angular/core';
import { HttpServerService } from '../Services/http-server.service';

@Component({
  selector: 'app-khach-hang',
  templateUrl: './khach-hang.component.html',
  styleUrls: ['./khach-hang.component.css']
})
export class KhachHangComponent implements OnInit{
  constructor(
    private httpServerServices: HttpServerService
    ){};
    public key: string="";
    public dsKhachHang:any[] = [];
    public idUpdate:number = 0;
    public old_khachHang = {
      so_dien_thoai: '',
      ho_ten: '',
      dia_chi: '',
      rank:0
    };
    public new_khachHang = {
      sdt: '',
      ho_ten: '',
      dia_chi: '',
    };

  ngOnInit(): void {

  }
  public create():void{
    this.httpServerServices.createKhachHang(this.new_khachHang).subscribe(
      (data) => {
        alert(data.message);
        window.location.reload();
      },
      (error) =>{
        alert(error.error)
      })
  }
  public update(khachHang: any): void {
    this.idUpdate = khachHang.id;
    this.old_khachHang = khachHang;
    console.log(this.old_khachHang);
  }
  public submitUpdate(): void {
    if (this.idUpdate !== 0){
      this.httpServerServices.updateKhachHang(this.idUpdate,this.old_khachHang).subscribe(
        (data) => {
          alert(data.message);
          window.location.reload();
        },
        (error) =>{
          alert(error.error)
          console.log(error);
        })
    }
  }

  public search(): void{
    if (this.key === '')
      this.dsKhachHang = [];
    else{
      const data = {"key": this.key}
      this.httpServerServices.getKhachHang(data).subscribe(
        (data) => {
          this.dsKhachHang = data
        },
        (error) =>{
          alert(error.error)
        })
    }

  }
  public delete(id:any): void{
    this.httpServerServices.deleteKhachHang(id).subscribe(
    (data) => {
      alert(data.message)
      const payload = {"key": this.key}
      this.httpServerServices.getKhachHang(payload).subscribe(
        (data) => {
          this.dsKhachHang = data
        },
        (error) =>{
          alert(error.error)
        })

    },
    (error) =>{
      alert(error.error)
    })
  }




}
