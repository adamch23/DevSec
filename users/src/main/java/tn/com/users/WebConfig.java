package tn.com.users;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        // Configuration globale des CORS
        registry.addMapping("/api/**")  // Permet l'accès aux URL commençant par /api/
                .allowedOrigins("http://localhost:4200")  // Autorise l'accès depuis le frontend Angular
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")  // Autorise les méthodes HTTP spécifiques
                .allowedHeaders("*")  // Permet tous les headers
                .allowCredentials(true);  // Autorise les cookies si nécessaire
    }
}
