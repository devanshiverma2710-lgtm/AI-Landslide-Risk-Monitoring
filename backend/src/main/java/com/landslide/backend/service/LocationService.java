package com.landslide.backend.service;

import com.landslide.backend.entity.Location;
import com.landslide.backend.repository.LocationRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class LocationService {

    private final LocationRepository locationRepository;

    public LocationService(LocationRepository locationRepository) {
        this.locationRepository = locationRepository;
    }

    public List<Location> getAllLocations() {
        return locationRepository.findAll();
    }

    public Location getLocationById(Long id) {
        return locationRepository.findById(id)
                .orElse(null);
    }

    public Location createLocation(Location location) {
        return locationRepository.save(location);
    }
}