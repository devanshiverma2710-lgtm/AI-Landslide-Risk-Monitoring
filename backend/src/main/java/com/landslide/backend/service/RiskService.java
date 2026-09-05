package com.landslide.backend.service;

import com.landslide.backend.entity.Location;
import com.landslide.backend.entity.RiskAssessment;
import com.landslide.backend.entity.SensorReading;
import com.landslide.backend.repository.LocationRepository;
import com.landslide.backend.repository.RiskAssessmentRepository;
import com.landslide.backend.repository.SensorReadingRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class RiskService {

    private final LocationRepository locationRepository;
    private final SensorReadingRepository sensorRepository;
    private final RiskAssessmentRepository riskRepository;

    public RiskService(
            LocationRepository locationRepository,
            SensorReadingRepository sensorRepository,
            RiskAssessmentRepository riskRepository) {

        this.locationRepository = locationRepository;
        this.sensorRepository = sensorRepository;
        this.riskRepository = riskRepository;
    }

    public RiskAssessment calculateRisk(Long locationId) {

        Location location = locationRepository.findById(locationId)
                .orElseThrow(() ->
                        new RuntimeException("Location not found"));

        SensorReading sensor = sensorRepository
                .findTopByLocationIdOrderByTimestampDesc(locationId)
                .orElseThrow(() ->
                        new RuntimeException("No sensor data found"));

        double score = calculateScore(location, sensor);

        RiskAssessment risk = new RiskAssessment();

        risk.setLocation(location);
        risk.setRiskScore(score);
        risk.setProbability(score / 100.0);
        risk.setRiskLevel(getRiskLevel(score));
        risk.setTimestamp(LocalDateTime.now());

        return riskRepository.save(risk);
    }

    private double calculateScore(
            Location location,
            SensorReading sensor) {

        double rainfallScore =
                Math.min(sensor.getRainfall24h() / 200.0 * 100.0, 100.0);

        double moistureScore =
                Math.min(sensor.getSoilMoisture(), 100.0);

        double slopeScore =
                Math.min(location.getSlope() / 45.0 * 100.0, 100.0);

        double porePressureScore =
                Math.min(sensor.getPorePressure() / 5.0 * 100.0, 100.0);

        double score =
                rainfallScore * 0.35 +
                        moistureScore * 0.25 +
                        slopeScore * 0.25 +
                        porePressureScore * 0.15;

        return Math.round(score * 100.0) / 100.0;
    }

    private String getRiskLevel(double score) {

        if (score >= 80) {
            return "CRITICAL";
        } else if (score >= 60) {
            return "HIGH";
        } else if (score >= 30) {
            return "MEDIUM";
        } else {
            return "LOW";
        }
    }

    public List<RiskAssessment> getRiskHistory(Long locationId) {
        return riskRepository.findByLocationId(locationId);
    }
}