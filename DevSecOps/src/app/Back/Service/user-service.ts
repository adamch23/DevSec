import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { User } from '../../model/user/user-module';

@Injectable({
  providedIn: 'root' // Le service est disponible globalement
})
export class UserService {
  private baseUrl = 'http://localhost:8081/api/users';  // URL de ton API backend

  constructor(private http: HttpClient) {}

  // Enregistrer un nouvel utilisateur
  register(user: User): Observable<User> {
    return this.http.post<User>(`${this.baseUrl}/register`, user);
  }

  // Authentification et retour du token JWT
  login(user: { email: string; password: string }): Observable<string> {
    return this.http.post(`${this.baseUrl}/login`, user, { responseType: 'text' });
  }


  // Récupérer un utilisateur par ID
  getById(id: number): Observable<User> {
    return this.http.get<User>(`${this.baseUrl}/${id}`);
  }
}
