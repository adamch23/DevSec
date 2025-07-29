import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
@Component({
  selector: 'app-dashbord',
    standalone: true,
    imports: [CommonModule], // ✅ Importe NgIf, NgFor, NgClass, etc.
  templateUrl: './dashbord.html',
  styleUrl: './dashbord.css'
})
export class Dashbord {
 menuOpen = false;
   sidebarOpen = true;


  toggleMenu() {
    this.menuOpen = !this.menuOpen;
  }
    toggleSidebar() {
    this.sidebarOpen = !this.sidebarOpen;
  }
}
