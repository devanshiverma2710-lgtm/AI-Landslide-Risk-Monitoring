package com.landslide.backend.dto;

public class PredictionRequest {

    private Double latitude;
    private Double longitude;

    private Double elevation_m;
    private Double slope_deg;
    private Double aspect_sin;
    private Double aspect_cos;
    private Double curvature;

    private Double rainfall_1d_mm;
    private Double rainfall_3d_mm;
    private Double rainfall_7d_mm;
    private Double max_rainfall_7d_mm;
    private Double rainfall_anomaly_z;

    private Double soil_moisture_m3_m3;
    private Double soil_moisture_anomaly;

    private Double historical_landslide_density;
    private Double historical_event_frequency;

    private Integer land_cover_class;
    private Double ndvi;

    private Double distance_to_road_km;
    private Double distance_to_river_km;
    private Double distance_to_fault_km;

    private Double population_density;
    private Double settlement_exposure;

    public PredictionRequest() {
    }

    public Double getLatitude() {
        return latitude;
    }

    public void setLatitude(Double latitude) {
        this.latitude = latitude;
    }

    public Double getLongitude() {
        return longitude;
    }

    public void setLongitude(Double longitude) {
        this.longitude = longitude;
    }

    public Double getElevation_m() {
        return elevation_m;
    }

    public void setElevation_m(Double elevation_m) {
        this.elevation_m = elevation_m;
    }

    public Double getSlope_deg() {
        return slope_deg;
    }

    public void setSlope_deg(Double slope_deg) {
        this.slope_deg = slope_deg;
    }

    public Double getAspect_sin() {
        return aspect_sin;
    }

    public void setAspect_sin(Double aspect_sin) {
        this.aspect_sin = aspect_sin;
    }

    public Double getAspect_cos() {
        return aspect_cos;
    }

    public void setAspect_cos(Double aspect_cos) {
        this.aspect_cos = aspect_cos;
    }

    public Double getCurvature() {
        return curvature;
    }

    public void setCurvature(Double curvature) {
        this.curvature = curvature;
    }

    public Double getRainfall_1d_mm() {
        return rainfall_1d_mm;
    }

    public void setRainfall_1d_mm(Double rainfall_1d_mm) {
        this.rainfall_1d_mm = rainfall_1d_mm;
    }

    public Double getRainfall_3d_mm() {
        return rainfall_3d_mm;
    }

    public void setRainfall_3d_mm(Double rainfall_3d_mm) {
        this.rainfall_3d_mm = rainfall_3d_mm;
    }

    public Double getRainfall_7d_mm() {
        return rainfall_7d_mm;
    }

    public void setRainfall_7d_mm(Double rainfall_7d_mm) {
        this.rainfall_7d_mm = rainfall_7d_mm;
    }

    public Double getMax_rainfall_7d_mm() {
        return max_rainfall_7d_mm;
    }

    public void setMax_rainfall_7d_mm(Double max_rainfall_7d_mm) {
        this.max_rainfall_7d_mm = max_rainfall_7d_mm;
    }

    public Double getRainfall_anomaly_z() {
        return rainfall_anomaly_z;
    }

    public void setRainfall_anomaly_z(Double rainfall_anomaly_z) {
        this.rainfall_anomaly_z = rainfall_anomaly_z;
    }

    public Double getSoil_moisture_m3_m3() {
        return soil_moisture_m3_m3;
    }

    public void setSoil_moisture_m3_m3(Double soil_moisture_m3_m3) {
        this.soil_moisture_m3_m3 = soil_moisture_m3_m3;
    }

    public Double getSoil_moisture_anomaly() {
        return soil_moisture_anomaly;
    }

    public void setSoil_moisture_anomaly(Double soil_moisture_anomaly) {
        this.soil_moisture_anomaly = soil_moisture_anomaly;
    }

    public Double getHistorical_landslide_density() {
        return historical_landslide_density;
    }

    public void setHistorical_landslide_density(Double historical_landslide_density) {
        this.historical_landslide_density = historical_landslide_density;
    }

    public Double getHistorical_event_frequency() {
        return historical_event_frequency;
    }

    public void setHistorical_event_frequency(Double historical_event_frequency) {
        this.historical_event_frequency = historical_event_frequency;
    }

    public Integer getLand_cover_class() {
        return land_cover_class;
    }

    public void setLand_cover_class(Integer land_cover_class) {
        this.land_cover_class = land_cover_class;
    }

    public Double getNdvi() {
        return ndvi;
    }

    public void setNdvi(Double ndvi) {
        this.ndvi = ndvi;
    }

    public Double getDistance_to_road_km() {
        return distance_to_road_km;
    }

    public void setDistance_to_road_km(Double distance_to_road_km) {
        this.distance_to_road_km = distance_to_road_km;
    }

    public Double getDistance_to_river_km() {
        return distance_to_river_km;
    }

    public void setDistance_to_river_km(Double distance_to_river_km) {
        this.distance_to_river_km = distance_to_river_km;
    }

    public Double getDistance_to_fault_km() {
        return distance_to_fault_km;
    }

    public void setDistance_to_fault_km(Double distance_to_fault_km) {
        this.distance_to_fault_km = distance_to_fault_km;
    }

    public Double getPopulation_density() {
        return population_density;
    }

    public void setPopulation_density(Double population_density) {
        this.population_density = population_density;
    }

    public Double getSettlement_exposure() {
        return settlement_exposure;
    }

    public void setSettlement_exposure(Double settlement_exposure) {
        this.settlement_exposure = settlement_exposure;
    }
}