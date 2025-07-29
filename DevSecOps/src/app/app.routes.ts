// src/app/app.routes.ts
import { Routes } from '@angular/router';
import { Register } from './Front/register/register';
import { Dashbord } from './Back/dashbord/dashbord';
import { VulnerabilityComponent } from './Back/vulnerability/vulnerability';
import { IaComponent } from './Back/ia/ia';

export const routes: Routes = [  // Ajoutez "export" ici
  { path: 'Register', component: Register },  
  { path: 'Back', component: Dashbord },  
  { path: 'vulnerability', component: VulnerabilityComponent },  
  { path: 'IA', component: IaComponent },  
  { path: '', redirectTo: '/Register', pathMatch: 'full' }
];
