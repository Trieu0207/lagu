import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DatBanComponent } from './dat-ban.component';

describe('DatBanComponent', () => {
  let component: DatBanComponent;
  let fixture: ComponentFixture<DatBanComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DatBanComponent]
    });
    fixture = TestBed.createComponent(DatBanComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
