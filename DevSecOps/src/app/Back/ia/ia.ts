import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-ia',
  templateUrl: './ia.html',
    imports: [CommonModule, FormsModule],
  styleUrls: ['./ia.css']
})
export class IaComponent {
  prompt = '';
  response = '';
  selectedModel = 'llama2'; // Modèle par défaut (ou modifiez selon vos besoins)
  models: string[] = [];

  constructor(private http: HttpClient) {
    this.getModels();
  }

  getModels() {
    this.http.get<any>('http://localhost:11434/api/tags').subscribe(res => {
      this.models = res.models.map((m: any) => m.name);
    });
  }

  sendPrompt() {
    const data = {
      prompt: this.prompt,
      model: this.selectedModel,
      stream: false
    };

    this.http.post<any>('http://localhost:11434/api/generate', data).subscribe(res => {
      this.response = res.response;
    });
  }
}
