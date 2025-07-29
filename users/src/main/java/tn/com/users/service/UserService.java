package tn.com.users.service;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import tn.com.users.model.User;
import tn.com.users.repository.UserRepository;

import java.util.List;
import java.util.Optional;

@Service
public class UserService {

    private final UserRepository repository;
    private final SequenceGeneratorService sequenceService;
    private final BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();

    public UserService(UserRepository repository, SequenceGeneratorService sequenceService) {
        this.repository = repository;
        this.sequenceService = sequenceService;
    }

    // Enregistrer un nouvel utilisateur
    public User register(User user) {
        user.setIdUser(sequenceService.generateSequence("user_sequence"));
        user.setPassword(encoder.encode(user.getPassword())); // On crypte le mot de passe
        return repository.save(user);
    }

    // Authentification de l'utilisateur
    public Optional<User> login(String email, String rawPassword) {
        return repository.findByEmail(email)
                .filter(user -> encoder.matches(rawPassword, user.getPassword()));
    }


    // Récupérer tous les utilisateurs
    public List<User> findAll() {
        return repository.findAll();
    }

    // Trouver un utilisateur par son ID
    public Optional<User> findById(Long id) {
        return repository.findById(id);
    }
}
