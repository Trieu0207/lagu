import { Component, OnInit } from '@angular/core';
import { HttpServerService } from '../Services/http-server.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-create-menu',
  templateUrl: './create-menu.component.html',
  styleUrls: ['./create-menu.component.css']
})
export class CreateMenuComponent implements OnInit{
  constructor(
    private httpServerServices: HttpServerService,
    private router: Router,
  ){};
  ngOnInit(): void {
  }
  public ten_san_pham: string = ''
  public don_gia:number = 0
  public loai: string = ''
  public anh: File = new File([], 'defaultFileName');
  public encodeLoai(loai:string):string {
    if(loai === "Món ăn") return "mon_nuoc";
    else if(loai === "Thức uống") return "mon_nuoc";
    else return "trang_mieng";
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
    formData.append('ten_san_pham', this.ten_san_pham)
    formData.append('don_gia', this.don_gia.toString())
    formData.append('loai', this.loai)
    this.httpServerServices.createMenu(formData).subscribe(
      (response) => {
        // Xử lý khi tải lên thành công
        alert(response)
        console.log('thêm thành công thành công:', response);
        this.router.navigateByUrl('/menu');
      },
      (error) => {
        // Xử lý khi xảy ra lỗi khi tải lên
        console.error('Lỗi:', error);
      }
    );
  }
  public thoat(): void {
    this.router.navigateByUrl('/menu');
  }
}
