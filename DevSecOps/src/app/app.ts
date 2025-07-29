// app.ts
import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet], // PAS RouterModule ici
  templateUrl: './app.html',
  styleUrls: ['./app.css']  // Ajoute bien "styleUrls" (au pluriel)
})
export class App {
  protected readonly title = signal('DevSecOps');
}
