package tn.com.users.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import tn.com.users.model.User;

import java.util.Optional;

public interface UserRepository extends MongoRepository<User, Long> {
    Optional<User> findByUsername(String username);
    Optional<User> findByEmail(String email);

}