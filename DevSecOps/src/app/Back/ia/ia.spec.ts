import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IA } from './ia';

describe('IA', () => {
  let component: IA;
  let fixture: ComponentFixture<IA>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [IA]
    })
    .compileComponents();

    fixture = TestBed.createComponent(IA);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
