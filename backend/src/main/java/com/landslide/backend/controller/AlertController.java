package com.landslide.backend.controller;

import com.landslide.backend.entity.Alert;
import com.landslide.backend.service.AlertService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/alerts")
public class AlertController {

    private final AlertService alertService;

    public AlertController(AlertService alertService) {
        this.alertService = alertService;
    }

    @GetMapping("/active")
    public List<Alert> getActiveAlerts() {
        return alertService.getActiveAlerts();
    }

    @GetMapping("/location/{locationId}")
    public List<Alert> getLocationAlerts(
            @PathVariable Long locationId) {

        return alertService.getLocationAlerts(locationId);
    }

    @PostMapping("/{locationId}")
    public Alert createAlert(
            @PathVariable Long locationId,
            @RequestParam String severity,
            @RequestParam String headline,
            @RequestParam String message) {

        return alertService.createAlert(
                locationId,
                severity,
                headline,
                message
        );
    }
}