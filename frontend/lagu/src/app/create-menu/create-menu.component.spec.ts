import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateMenuComponent } from './create-menu.component';

describe('CreateMenuComponent', () => {
  let component: CreateMenuComponent;
  let fixture: ComponentFixture<CreateMenuComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CreateMenuComponent]
    });
    fixture = TestBed.createComponent(CreateMenuComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
