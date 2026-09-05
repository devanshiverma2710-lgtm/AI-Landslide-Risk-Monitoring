package com.landslide.backend.controller;

import com.landslide.backend.entity.RiskAssessment;
import com.landslide.backend.service.RiskService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/risk")
public class RiskController {

    private final RiskService riskService;

    public RiskController(RiskService riskService) {
        this.riskService = riskService;
    }

    @PostMapping("/{locationId}/calculate")
    public RiskAssessment calculateRisk(
            @PathVariable Long locationId) {

        return riskService.calculateRisk(locationId);
    }

    @GetMapping("/{locationId}")
    public List<RiskAssessment> getRiskHistory(
            @PathVariable Long locationId) {

        return riskService.getRiskHistory(locationId);
    }
}