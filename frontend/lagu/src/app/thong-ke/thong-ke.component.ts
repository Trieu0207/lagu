import { Component, OnInit } from '@angular/core';
import { HttpServerService } from '../Services/http-server.service';

@Component({
  selector: 'app-thong-ke',
  templateUrl: './thong-ke.component.html',
  styleUrls: ['./thong-ke.component.css']
})
export class ThongKeComponent implements OnInit {
  constructor(
    private httpServerServices: HttpServerService
    ){};
    public thongKeDoanhThu: any[] = [];
  ngOnInit(): void {
    this.httpServerServices.thongKeDoanhThu().subscribe((data)=>{
      this.thongKeDoanhThu = data
    })
  }

}
