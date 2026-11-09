import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormulaireFormation } from './formulaire-formation';

describe('FormulaireFormation', () => {
  let component: FormulaireFormation;
  let fixture: ComponentFixture<FormulaireFormation>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FormulaireFormation],
    }).compileComponents();

    fixture = TestBed.createComponent(FormulaireFormation);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
