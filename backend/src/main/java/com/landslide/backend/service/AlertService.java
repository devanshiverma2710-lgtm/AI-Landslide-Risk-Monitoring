package com.landslide.backend.service;

import com.landslide.backend.entity.Alert;
import com.landslide.backend.entity.Location;
import com.landslide.backend.repository.AlertRepository;
import com.landslide.backend.repository.LocationRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class AlertService {

    private final AlertRepository alertRepository;
    private final LocationRepository locationRepository;

    public AlertService(
            AlertRepository alertRepository,
            LocationRepository locationRepository) {

        this.alertRepository = alertRepository;
        this.locationRepository = locationRepository;
    }

    public Alert createAlert(
            Long locationId,
            String severity,
            String headline,
            String message) {

        Location location = locationRepository
                .findById(locationId)
                .orElseThrow(() ->
                        new RuntimeException("Location not found"));

        Alert alert = new Alert();

        alert.setLocation(location);
        alert.setSeverity(severity);
        alert.setHeadline(headline);
        alert.setMessage(message);
        alert.setStatus("ACTIVE");
        alert.setCreatedAt(LocalDateTime.now());

        return alertRepository.save(alert);
    }

    public List<Alert> getActiveAlerts() {
        return alertRepository.findByStatus("ACTIVE");
    }

    public List<Alert> getLocationAlerts(Long locationId) {
        return alertRepository.findByLocationId(locationId);
    }
}