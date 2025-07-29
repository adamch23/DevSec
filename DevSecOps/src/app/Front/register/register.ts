import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { UserService } from '../../Back/Service/user-service';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { Router } from '@angular/router'; // ✅ Importer le Router

@Component({
  selector: 'app-register',
  templateUrl: './register.html',
  styleUrls: ['./register.css'],
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
})
export class Register {
  user = {
    username: '',
    email: '',
    password: '',
    phone: 0
  };

  loginData = {
    email: '',
    password: ''
  };

  constructor(
    private userService: UserService,
    private router: Router // ✅ Injecter le Router
  ) {}

  onRegister(): void {
    this.userService.register(this.user).subscribe({
      next: (response) => {
        alert('Inscription réussie !');
      },
      error: (err) => {
        console.error('Erreur lors de l\'inscription:', err);
        alert('Erreur lors de l\'inscription');
      }
    });
  }

  onLogin(): void {
    this.userService.login(this.loginData).subscribe({
      next: (token) => {
        localStorage.setItem('authToken', token);
        alert('Connexion réussie');

        // ✅ Redirection après login réussi
        this.router.navigate(['/Back']); // 🔁 modifie '/dashboard' selon ta route cible
      },
      error: (err) => {
        alert('Identifiants incorrects');
        console.error(err);
      }
    });
  }
}
