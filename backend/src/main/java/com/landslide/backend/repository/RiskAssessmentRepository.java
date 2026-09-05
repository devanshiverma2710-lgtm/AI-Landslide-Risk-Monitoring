package com.landslide.backend.repository;

import com.landslide.backend.entity.RiskAssessment;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface RiskAssessmentRepository
        extends JpaRepository<RiskAssessment, Long> {

    List<RiskAssessment> findByLocationId(Long locationId);
}