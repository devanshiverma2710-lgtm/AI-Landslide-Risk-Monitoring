package com.landslide.backend.repository;

import com.landslide.backend.entity.SensorReading;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface SensorReadingRepository
        extends JpaRepository<SensorReading, Long> {

    List<SensorReading> findByLocationId(Long locationId);

    Optional<SensorReading> findTopByLocationIdOrderByTimestampDesc(Long locationId);
}