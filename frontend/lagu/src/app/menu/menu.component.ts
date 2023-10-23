import { Router } from '@angular/router';
import { CommonService } from './../Services/common.service';
import { HttpServerService } from './../Services/http-server.service';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.css']
})
export class MenuComponent implements OnInit{
  constructor(
    private commonService: CommonService,
    private httpServerServices: HttpServerService,
    private router: Router,
    ){};
    public key: string = '';
    public data_server: any[] = [];
    public menu: any[] = [];
    public search_menu: any[] = []
    public menu_options: any[] = [];
  ngOnInit(): void {
    this.httpServerServices.getMenu().subscribe((data) => {
      this.data_server = data
      this.menu = this.data_server
      // console.log('data', data);
    });
    if (this.search_menu.length > 0){
      this.menu = this.search_menu
    }
  }

  public getMenu(): void{
    console.log(this.key)
    this.search_menu = [];
    if (this.menu_options.length > 0){
      for(let item of this.menu_options){
        if(item.ten_san_pham.toLowerCase().includes(this.key.toLowerCase())){
          this.search_menu.push(item)
        }
      }
      if(this.search_menu.length > 0 && this.key != ""){
        this.menu = this.search_menu
      }
      // else if(this.menu_options.length > 0){
      //   this.menu = this.menu_options
      // }
      else{
        alert('Không tìm được món');
      }
    }
    else{
      for(let item of this.data_server){
        if(item.ten_san_pham.toLowerCase().includes(this.key.toLowerCase())){
          this.search_menu.push(item)
        }
      }
      if(this.search_menu.length > 0 && this.key != ""){
        this.menu = this.search_menu
      }
      // else if(this.menu_options.length > 0){
      //   this.menu = this.menu_options
      // }
      else{
        alert('Không tìm được món');
      }
    }
  }
  public mon_an(): void{
    this.menu_options = [];
    for(let item of this.data_server){
      if(item.loai.includes('mon_an')){
        this.menu_options.push(item)
      }
    }
    if(this.menu_options.length > 0){
      this.menu = this.menu_options
    }
  }
  public thuc_uong(): void{
    this.menu_options = [];
    for(let item of this.data_server){
      if(item.loai.includes('mon_nuoc')){
        this.menu_options.push(item)
      }
    }
    if(this.menu_options.length > 0){
      this.menu = this.menu_options
    }
  }
  public trang_mieng(): void{
    this.menu_options = [];
    for(let item of this.data_server){
      if(item.loai.includes('trang_mieng')){
        this.menu_options.push(item)
      }
    }
    if(this.menu_options.length > 0){
      this.menu = this.menu_options
    }
  }
  public all(): void{
    this.menu = this.data_server
  }
  public get_detail(data: any): void{
    let link = '/menu-detail'
    this.commonService.mon = data
    this.router.navigate(['/menu-detail', data.id]);
    console.log(link)
  }
  public changeTrangThai(item_id: number): void {
    let formData = new FormData();
    formData.append('id', item_id.toString());
    const jsonData = {};
    this.httpServerServices.changeTrangThai(formData).subscribe((response) => {
      // Xử lý khi tải lên thành công
      window.location.reload();
    },
    (error) => {
      // Xử lý khi xảy ra lỗi khi tải lên
      console.error('Lỗi: ', error);
    })
  }
  public routeCreate(): void {
    this.router.navigateByUrl('/create-menu');
  }
}
