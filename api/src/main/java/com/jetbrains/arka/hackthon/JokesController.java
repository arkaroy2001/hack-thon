package com.jetbrains.arka.hackthon;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class JokesController {
    @GetMapping("/api")
    public String hello(){
        return "Hello World!";
    }
}
