import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';

import { ChatbotService } from './chatbot';

describe('ChatbotService', () => {
  let service: ChatbotService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule]
    });
    service = TestBed.inject(ChatbotService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});