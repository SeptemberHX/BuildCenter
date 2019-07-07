package {package_name}

import com.septemberhx.mclient.annotation.MClient;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.EnableEurekaClient;
import org.springframework.cloud.openfeign.EnableFeignClients;

@SpringBootApplication
@MClient
@EnableEurekaClient
@EnableFeignClients
public class MMain {{
    public static void main(String[] args) {{
        SpringApplication.run(MMain.class, args);
    }}
}}
