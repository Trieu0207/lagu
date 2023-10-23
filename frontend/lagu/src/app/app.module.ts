import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {HttpClientModule} from '@angular/common/http';
import { CurrencyPipe } from '@angular/common';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { MenuComponent } from './menu/menu.component';
import { ReactiveFormsModule } from '@angular/forms';
import {FormsModule} from '@angular/forms';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { NhanBanComponent } from './nhan-ban/nhan-ban.component';
import { MenuDetailComponent } from './menu-detail/menu-detail.component';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { CreateMenuComponent } from './create-menu/create-menu.component';
import { DatBanComponent } from './dat-ban/dat-ban.component';
import { DatBanDetailComponent } from './dat-ban-detail/dat-ban-detail.component';
import { DatePipe } from '@angular/common';
import { VoucherComponent } from './voucher/voucher.component';
import { BanComponent } from './ban/ban.component';
import { ThongKeComponent } from './thong-ke/thong-ke.component';
import { KhachHangComponent } from './khach-hang/khach-hang.component';
@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    MenuComponent,
    PageNotFoundComponent,
    NhanBanComponent,
    MenuDetailComponent,
    CreateMenuComponent,
    DatBanComponent,
    DatBanDetailComponent,
    VoucherComponent,
    BanComponent,
    ThongKeComponent,
    KhachHangComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    FormsModule,
    NoopAnimationsModule,

  ],
  providers: [CurrencyPipe,DatePipe,],
  bootstrap: [AppComponent]
})
export class AppModule { }
