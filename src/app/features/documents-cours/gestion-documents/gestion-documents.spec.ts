import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GestionDocuments } from './gestion-documents';

describe('GestionDocuments', () => {
  let component: GestionDocuments;
  let fixture: ComponentFixture<GestionDocuments>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GestionDocuments],
    }).compileComponents();

    fixture = TestBed.createComponent(GestionDocuments);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
