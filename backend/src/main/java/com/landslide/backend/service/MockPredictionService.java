package com.landslide.backend.service;

import com.landslide.backend.dto.PredictionRequest;
import com.landslide.backend.dto.PredictionResponse;
import org.springframework.stereotype.Service;

import java.util.List;

@Service("mockPredictionService")
public class MockPredictionService implements PredictionService {

    @Override
    public PredictionResponse predict(PredictionRequest request) {

        return new PredictionResponse(
                request.getLatitude(),
                request.getLongitude(),
                0.78,
                "CRITICAL",
                List.of(
                        "High 7-day rainfall",
                        "Steep slope",
                        "High historical landslide activity"
                )
        );
    }
}