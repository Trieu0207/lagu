import { Component, OnInit } from '@angular/core';
import { HttpServerService } from '../Services/http-server.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-ban',
  templateUrl: './ban.component.html',
  styleUrls: ['./ban.component.css']
})
export class BanComponent implements OnInit {
  constructor(
    private httpServerServices: HttpServerService
    ){};
    public id: string ='';
    public so_luong: string ='';
    public trang_thai: boolean = false;
    public suc_chua: string ='';
    public loai_ban: string ='';
    public new_ban:any ={
      so_luong:0,
      suc_chua:0,
      loai_ban:""
    };
    public dsBan:any[] = [];
    public banId:number =0;
    ngOnInit(): void {
      this.httpServerServices.loadDsBan().subscribe((data)=>{
        this.dsBan = data;
      })
    }
    public setBan(ban: any):void{
      this.banId = ban.id;
      this.so_luong = ban.so_luong;
      this.suc_chua = ban.suc_chua;
      this.trang_thai = ban.is_trang_thai;
      this.loai_ban = ban.loai_ban;
      let data:any = [this.so_luong, this.suc_chua, this.trang_thai, this.loai_ban]
      console.log(data);
    }
    public checkClick():boolean{
      if(this.banId === 0){
        return true;
      }
      return false
    }
    public updateData():void{
      if(this.banId !== 0){
        let payload = {
          "so_luong": this.so_luong,
          "suc_chua": this.suc_chua,
          "loai_ban": this.loai_ban
        }
        this.httpServerServices.updateInfo(this.banId, payload).subscribe( (data) =>{
          alert(data.message)
          window.location.reload()
        },(error) => {
          console.log(error)
        })
      }}

      public hetBan(): void {
        if(this.banId !== 0){
          this.httpServerServices.changeActiveBan(this.banId).subscribe( (data) =>{
            alert(data.message)
            window.location.reload()
          },(error) => {
            console.log(error)
          })
        }
      }
      public checkTrangThai(): boolean {
        if(this.trang_thai === true){
          return true
        }
        return false
      }
      public addBan(): void {
        console.log(this.new_ban);
        this.httpServerServices.addBan(this.new_ban).subscribe( (data) =>{
          alert(data.message)
          window.location.reload()
        },(error) => {
          console.log(error)
        })
      }


}
