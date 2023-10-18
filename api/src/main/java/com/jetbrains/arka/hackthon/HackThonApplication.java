package com.jetbrains.arka.hackthon;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration;

@SpringBootApplication ( exclude = {SecurityAutoConfiguration.class} )
public class HackThonApplication {

	public static void main(String[] args) {
		SpringApplication.run(HackThonApplication.class, args);
	}

}
