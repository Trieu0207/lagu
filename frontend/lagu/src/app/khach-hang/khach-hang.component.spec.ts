import { ComponentFixture, TestBed } from '@angular/core/testing';

import { KhachHangComponent } from './khach-hang.component';

describe('KhachHangComponent', () => {
  let component: KhachHangComponent;
  let fixture: ComponentFixture<KhachHangComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [KhachHangComponent]
    });
    fixture = TestBed.createComponent(KhachHangComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
