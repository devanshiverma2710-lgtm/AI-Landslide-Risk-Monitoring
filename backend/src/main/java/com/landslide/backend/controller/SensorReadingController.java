package com.landslide.backend.controller;

import com.landslide.backend.entity.SensorReading;
import com.landslide.backend.service.SensorReadingService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/sensors")
public class SensorReadingController {

    private final SensorReadingService sensorService;

    public SensorReadingController(
            SensorReadingService sensorService) {

        this.sensorService = sensorService;
    }

    @PostMapping("/{locationId}")
    public SensorReading createReading(
            @PathVariable Long locationId,
            @RequestBody SensorReading reading) {

        return sensorService.createReading(locationId, reading);
    }

    @GetMapping("/{locationId}")
    public List<SensorReading> getReadings(
            @PathVariable Long locationId) {

        return sensorService.getReadings(locationId);
    }
}