import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  constructor(private router: Router) {}
  isClicked = false;
  title = 'test';
  name = 'phungtantrieu@gmail.com'
  menuItems = [
    { label: 'Thanh toán', link: '/home' },
    { label: 'Danh mục Menu', link: '/menu' },
    { label: 'Đặt bàn', link: '/dat-ban' },
    {label: 'Nhận bàn', link: '/nhan-ban' },
    { label: 'Voucher', link: '/voucher' },
    { label: 'Danh mục Bàn ăn', link: '/ban' },
    { label: 'Quản lý khách hàng', link: '/khach-hang' },
    { label: 'Thống kê - Báo cáo', link: '/thong-ke' },
    { label: 'Liên hệ', link: '**' }
  ];

  handleItemClick(link: string) {
    this.router.navigateByUrl(link);
  }
  style: any = {};

}
