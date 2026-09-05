package com.landslide.backend.repository;

import com.landslide.backend.entity.Alert;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface AlertRepository extends JpaRepository<Alert, Long> {

    List<Alert> findByStatus(String status);

    List<Alert> findByLocationId(Long locationId);
}