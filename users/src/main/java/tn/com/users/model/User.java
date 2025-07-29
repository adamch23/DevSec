package tn.com.users.model;


import lombok.*;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@ToString
public class User {
    @Id
    private Long idUser; // auto-incremented
    private String username;
    private String email;
    private Long Phone;
    private String password; // hashed


}
