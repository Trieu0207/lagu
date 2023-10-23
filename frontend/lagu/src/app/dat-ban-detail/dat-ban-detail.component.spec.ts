import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DatBanDetailComponent } from './dat-ban-detail.component';

describe('DatBanDetailComponent', () => {
  let component: DatBanDetailComponent;
  let fixture: ComponentFixture<DatBanDetailComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DatBanDetailComponent]
    });
    fixture = TestBed.createComponent(DatBanDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
