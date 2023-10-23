import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NhanBanComponent } from './nhan-ban.component';

describe('NhanBanComponent', () => {
  let component: NhanBanComponent;
  let fixture: ComponentFixture<NhanBanComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [NhanBanComponent]
    });
    fixture = TestBed.createComponent(NhanBanComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
