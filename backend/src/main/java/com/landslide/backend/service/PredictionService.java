package com.landslide.backend.service;

import com.landslide.backend.dto.PredictionRequest;
import com.landslide.backend.dto.PredictionResponse;

public interface PredictionService {

    PredictionResponse predict(PredictionRequest request);
}