import { ActivatedRoute, Router } from '@angular/router';
import { HttpServerService } from '../Services/http-server.service';
import { CommonService } from './../Services/common.service';
import { Component, OnInit } from '@angular/core';
import { HttpErrorResponse, HttpResponse } from '@angular/common/http';
@Component({
  selector: 'app-menu-detail',
  templateUrl: './menu-detail.component.html',
  styleUrls: ['./menu-detail.component.css']
})
export class MenuDetailComponent implements OnInit {
  constructor(
    private commonService: CommonService,
    private httpServerServices: HttpServerService,
    private route: ActivatedRoute,
    private router: Router
  ){};
  // public ten_san_pham:any[] = this.commonService.mon.ten_san_pham
  public item:any= {}
  public menuId = this.route.snapshot.paramMap.get('id');
  ngOnInit(): void {
    this.httpServerServices.getDetailMenu(this.menuId).subscribe(data => {
      this.item = data
    })
    console.log(this.item.is_trang_thai)
  }
  public ten_san_pham: string = ''
  public don_gia:number = 0
  public loai: string = ''
  public link_anh: any = null;
  public trang_thai: string = '';
  public is_trang_thai: boolean = false;
  public loaiSanPham(loai:string):string {
    if(loai == "mon_an") return "Món ăn";
    else if(loai == "mon_nuoc") return "Thức uống";
    else return "Tráng miệng";
  }
  public encodeLoai(loai:string):string {
    if(loai === "Món ăn") return "mon_nuoc";
    else if(loai === "Thức uống") return "mon_nuoc";
    else return "trang_mieng";
  }
  public xoa(id:string):void {
    this.httpServerServices.delMenu(id).subscribe((res: HttpResponse<any>) => {
      console.log("Response status:", res.status)
      if(res.status == 204) {
        this.router.navigateByUrl('/menu');
      }
      else if(res.status == 400) {
        alert("không thể xóa món ăn")
        console.log(res.status)
      }
      else
        this.router.navigateByUrl('**');
    })
  }

  public checkNull(text:string):boolean {
    if(text == "")
      return false;
    else return true;
  }
  public anh: File = new File([], 'defaultFileName');
  public formAnh = {
    anh:File
  }
  onFileSelected(event: any){
    const selectedFile: File = event.target.files[0];
    this.anh = selectedFile
  }
  // public isAlert: boolean = false;
  public submit():void {
    if(this.anh.name !== "defaultFileName")
      console.log(this.anh.name)
    const formData = new FormData();
    // formData.append('link_anh', this.anh)
    if(this.anh.name !== "defaultFileName") {
      formData.append('link_anh', this.anh)
    }
    if(this.ten_san_pham)
      formData.append('ten_san_pham', this.ten_san_pham)
    if(this.don_gia != 0)
      formData.append('don_gia', this.don_gia.toString())
    if(this.loai){
      formData.append('loai', this.loai)
    }
    // this.trang_thai = this.item.is_trang_thai.toString();
    var text = this.item.is_trang_thai.toString()
    if(this.trang_thai != text)
      formData.append('is_trang_thai', this.trang_thai.toString())
    console.log(this.trang_thai + this.item.is_trang_thai.toString())
    this.httpServerServices.updateDetailMenu(this.item.id, formData).subscribe(
      (response) => {
        // Xử lý khi tải lên thành công
        alert(response)
        console.log('Tải lên thành công:', response);
        window.location.reload();
      },
      (error) => {
        // Xử lý khi xảy ra lỗi khi tải lên
        console.error('Lỗi khi tải lên hình ảnh:', error);
      }
    );
  }
  public changeTrangThai(): void {
    const data = {"id": this.item.id}
    let formData = new FormData();
    formData.append('id', this.item.id.toString());
    const jsonData = {};
    console.log(JSON.stringify(data));
    // this.httpServerServices.changeTrangThai(formData);
    // window.location.reload();
    //
    this.httpServerServices.changeTrangThai(formData).subscribe((response) => {
      // Xử lý khi tải lên thành công
      alert(response)
      window.location.reload();
    },
    (error) => {
      // Xử lý khi xảy ra lỗi khi tải lên
      console.error('Lỗi: ', error);
    })
  }
}
