package com.esprit.ms.apigateway4sa11;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
@EnableDiscoveryClient
public class ApiGateway4Sa11Application {

	public static void main(String[] args) {
		SpringApplication.run(ApiGateway4Sa11Application.class, args);
	}

	@Bean
	public RouteLocator getRouteApiGateway(RouteLocatorBuilder builder)
	{
		return builder.routes()
				// Add route for HEBERGEMENT service
				.route("USERS", r -> r.path("/api/users/**")
						.uri("lb://USERS"))

				.route("VULNERABILITIES", r -> r.path("/api/vulnerabilities/**")
						.uri("lb://VULNERABILITIES"))
				// Add route for USER service
				.route("EXPLOIT_REPORTS", r -> r.path("/api/exploit-reports/**")
						.uri("lb://EXPLOIT_REPORTS"))





				.build();



	}
}
