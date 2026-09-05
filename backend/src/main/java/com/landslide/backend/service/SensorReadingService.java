package com.landslide.backend.service;

import com.landslide.backend.entity.Location;
import com.landslide.backend.entity.SensorReading;
import com.landslide.backend.repository.LocationRepository;
import com.landslide.backend.repository.SensorReadingRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class SensorReadingService {

    private final SensorReadingRepository sensorRepository;
    private final LocationRepository locationRepository;

    public SensorReadingService(
            SensorReadingRepository sensorRepository,
            LocationRepository locationRepository) {

        this.sensorRepository = sensorRepository;
        this.locationRepository = locationRepository;
    }

    public SensorReading createReading(
            Long locationId,
            SensorReading reading) {

        Location location = locationRepository
                .findById(locationId)
                .orElseThrow(() ->
                        new RuntimeException("Location not found"));

        reading.setLocation(location);
        reading.setTimestamp(LocalDateTime.now());

        return sensorRepository.save(reading);
    }

    public List<SensorReading> getReadings(Long locationId) {
        return sensorRepository.findByLocationId(locationId);
    }
}