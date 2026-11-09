import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModifierFormation } from './modifier-formation';

describe('ModifierFormation', () => {
  let component: ModifierFormation;
  let fixture: ComponentFixture<ModifierFormation>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ModifierFormation],
    }).compileComponents();

    fixture = TestBed.createComponent(ModifierFormation);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
