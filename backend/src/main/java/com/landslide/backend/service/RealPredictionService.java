package com.landslide.backend.service;

import com.landslide.backend.dto.PredictionRequest;
import com.landslide.backend.dto.PredictionResponse;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

@Service
public class RealPredictionService implements PredictionService {

    private final RestClient restClient;

    public RealPredictionService() {
        this.restClient = RestClient.builder()
                .baseUrl("http://127.0.0.1:8000")
                .build();
    }

    @Override
    public PredictionResponse predict(PredictionRequest request) {

        return restClient.post()
                .uri("/predict")
                .body(request)
                .retrieve()
                .body(PredictionResponse.class);
    }
}