package com.m1fonda.serviceproxy;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@SpringBootApplication
@EnableDiscoveryClient
public class ServiceProxyApplication {

    public static void main(String[] args) {
        SpringApplication.run(ServiceProxyApplication.class, args);
    }

}
