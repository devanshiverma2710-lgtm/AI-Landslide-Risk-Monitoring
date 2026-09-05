package com.landslide.backend.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "sensor_readings")
public class SensorReading {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "location_id", nullable = false)
    private Location location;

    private Double rainfall24h;

    private Double soilMoisture;

    private Double porePressure;

    private Double tilt;

    private Double vibration;

    private LocalDateTime timestamp;

    public SensorReading() {
    }

    public Long getId() {
        return id;
    }

    public Location getLocation() {
        return location;
    }

    public void setLocation(Location location) {
        this.location = location;
    }

    public Double getRainfall24h() {
        return rainfall24h;
    }

    public void setRainfall24h(Double rainfall24h) {
        this.rainfall24h = rainfall24h;
    }

    public Double getSoilMoisture() {
        return soilMoisture;
    }

    public void setSoilMoisture(Double soilMoisture) {
        this.soilMoisture = soilMoisture;
    }

    public Double getPorePressure() {
        return porePressure;
    }

    public void setPorePressure(Double porePressure) {
        this.porePressure = porePressure;
    }

    public Double getTilt() {
        return tilt;
    }

    public void setTilt(Double tilt) {
        this.tilt = tilt;
    }

    public Double getVibration() {
        return vibration;
    }

    public void setVibration(Double vibration) {
        this.vibration = vibration;
    }

    public LocalDateTime getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(LocalDateTime timestamp) {
        this.timestamp = timestamp;
    }
}