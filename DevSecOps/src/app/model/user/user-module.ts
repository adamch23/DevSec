import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Register } from '../../Front/register/register';

@NgModule({
  imports: [
    CommonModule,  
    FormsModule,   // Assure-toi que FormsModule est bien importé
  ]
})
export class UserModule { 
  
}
export interface User {
  idUser?: number;       // facultatif, généré automatiquement
  username: string;
  email: string;
 phone: number;  
   password: string;
}
