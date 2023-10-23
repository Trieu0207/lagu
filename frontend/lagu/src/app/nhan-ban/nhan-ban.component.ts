import { Component, OnInit } from '@angular/core';
import { HttpServerService } from '../Services/http-server.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-nhan-ban',
  templateUrl: './nhan-ban.component.html',
  styleUrls: ['./nhan-ban.component.css']
})

export class NhanBanComponent implements OnInit{
  constructor(
    private httpServerServices: HttpServerService,
    private router: Router,
    ){};
  public dsDatBan: any[] = []
  private item: any;
  public key: string = '';
  public searchDs:any[] = [];
  public dsBanDaThanhToan: any[] = [];
  ngOnInit(): void {
    if (this.searchDs.length > 0) {
      this.dsDatBan = this.searchDs
    }
    this.httpServerServices.getDsDatBanToday().subscribe((data) => {
      this.dsDatBan = data
    })
  }
  public get_detail(data: any): void{
    let link = '/dat-ban-detail'
    this.router.navigate(['/dat-ban-detail', data.id]);
  }
  public nhanBan(id: number): void {
    this.httpServerServices.nhanBan(id).subscribe((response) => {
      // Xử lý khi tải lên thành công
      alert(response)
      window.location.reload();
    },
    (error) => {
      // Xử lý khi xảy ra lỗi khi tải lên
      alert(error.error)
      console.error('Lỗi: ', error);
    });
  }
  public search():void {
    let payload = {"key": this.key}
    this.httpServerServices.searchDatBan(payload).subscribe(
      (data)=>{
      this.dsDatBan = data;
    },
    (error) => {
      // Xử lý khi xảy ra lỗi khi tải lên
      alert(error.error)
      window.location.reload()
    })
  }
  public huyDatBan(id: any):void{
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






}
