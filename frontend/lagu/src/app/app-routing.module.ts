import { HomeComponent } from './home/home.component';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { MenuComponent } from './menu/menu.component';
import { NhanBanComponent } from './nhan-ban/nhan-ban.component';
import { MenuDetailComponent } from './menu-detail/menu-detail.component';
import { CreateMenuComponent } from './create-menu/create-menu.component';
import { DatBanComponent } from './dat-ban/dat-ban.component';
import { DatBanDetailComponent } from './dat-ban-detail/dat-ban-detail.component';
import { VoucherComponent } from './voucher/voucher.component';
import { BanComponent } from './ban/ban.component';
import { ThongKeComponent } from './thong-ke/thong-ke.component';
import { KhachHangComponent } from './khach-hang/khach-hang.component';

const routes: Routes = [
  // { path: '', component: PageNotFoundComponent},
  { path:'home', component: HomeComponent},
  {path:'', component: HomeComponent},
  {path:'menu', component: MenuComponent},
  {path:'ban', component: BanComponent},
  {path:'nhan-ban', component: NhanBanComponent},
  {path:'dat-ban', component: DatBanComponent},
  {path:'voucher', component: VoucherComponent},
  {path:'thong-ke', component: ThongKeComponent},
  {path:'khach-hang', component: KhachHangComponent},
  {path:'create-menu', component: CreateMenuComponent},
  {path:'menu-detail/:id', component: MenuDetailComponent},
  {path:'dat-ban-detail/:id', component: DatBanDetailComponent},
  {path:'**', component: PageNotFoundComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
