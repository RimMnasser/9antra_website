import { TestBed } from '@angular/core/testing';

import { DocumentsCours } from './documents-cours';

describe('DocumentsCours', () => {
  let service: DocumentsCours;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DocumentsCours);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
