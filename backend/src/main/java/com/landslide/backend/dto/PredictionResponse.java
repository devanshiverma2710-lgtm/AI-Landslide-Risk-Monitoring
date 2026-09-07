package com.landslide.backend.dto;

import java.util.List;

public class PredictionResponse {

    private Double latitude;
    private Double longitude;

    private Double landslide_probability;
    private Integer landslide_prediction;

    private String risk_level;
    private String warning;

    private String model;
    private String model_version;
    private String risk_engine_version;

    private Double susceptibility_score;
    private String susceptibility_level;

    private Double trigger_score;
    private String trigger_level;

    private Double exposure_score;
    private String exposure_level;

    private Double final_risk_score;

    private String alert_status;

    private List<TopFactor> top_factors;

    private String prediction_timestamp;

    public PredictionResponse() {
    }

    public PredictionResponse(
            Double latitude,
            Double longitude,
            Double landslideProbability,
            String riskLevel,
            List<String> topFactors) {

        this.latitude = latitude;
        this.longitude = longitude;
        this.landslide_probability = landslideProbability;
        this.risk_level = riskLevel;
    }

    public static class TopFactor {

        private String feature;
        private Double value;
        private Double shap_value;
        private String direction;

        public TopFactor() {
        }

        public String getFeature() {
            return feature;
        }

        public void setFeature(String feature) {
            this.feature = feature;
        }

        public Double getValue() {
            return value;
        }

        public void setValue(Double value) {
            this.value = value;
        }

        public Double getShap_value() {
            return shap_value;
        }

        public void setShap_value(Double shap_value) {
            this.shap_value = shap_value;
        }

        public String getDirection() {
            return direction;
        }

        public void setDirection(String direction) {
            this.direction = direction;
        }
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

    public Double getLandslide_probability() {
        return landslide_probability;
    }

    public void setLandslide_probability(Double landslide_probability) {
        this.landslide_probability = landslide_probability;
    }

    public Integer getLandslide_prediction() {
        return landslide_prediction;
    }

    public void setLandslide_prediction(Integer landslide_prediction) {
        this.landslide_prediction = landslide_prediction;
    }

    public String getRisk_level() {
        return risk_level;
    }

    public void setRisk_level(String risk_level) {
        this.risk_level = risk_level;
    }

    public String getWarning() {
        return warning;
    }

    public void setWarning(String warning) {
        this.warning = warning;
    }

    public String getModel() {
        return model;
    }

    public void setModel(String model) {
        this.model = model;
    }

    public String getModel_version() {
        return model_version;
    }

    public void setModel_version(String model_version) {
        this.model_version = model_version;
    }

    public String getRisk_engine_version() {
        return risk_engine_version;
    }

    public void setRisk_engine_version(String risk_engine_version) {
        this.risk_engine_version = risk_engine_version;
    }

    public Double getSusceptibility_score() {
        return susceptibility_score;
    }

    public void setSusceptibility_score(Double susceptibility_score) {
        this.susceptibility_score = susceptibility_score;
    }

    public String getSusceptibility_level() {
        return susceptibility_level;
    }

    public void setSusceptibility_level(String susceptibility_level) {
        this.susceptibility_level = susceptibility_level;
    }

    public Double getTrigger_score() {
        return trigger_score;
    }

    public void setTrigger_score(Double trigger_score) {
        this.trigger_score = trigger_score;
    }

    public String getTrigger_level() {
        return trigger_level;
    }

    public void setTrigger_level(String trigger_level) {
        this.trigger_level = trigger_level;
    }

    public Double getExposure_score() {
        return exposure_score;
    }

    public void setExposure_score(Double exposure_score) {
        this.exposure_score = exposure_score;
    }

    public Double getFinal_risk_score() {
        return final_risk_score;
    }

    public void setFinal_risk_score(Double final_risk_score) {
        this.final_risk_score = final_risk_score;
    }

    public String getAlert_status() {
        return alert_status;
    }

    public void setAlert_status(String alert_status) {
        this.alert_status = alert_status;
    }

    public List<TopFactor> getTop_factors() {
        return top_factors;
    }

    public void setTop_factors(List<TopFactor> top_factors) {
        this.top_factors = top_factors;
    }

    public String getPrediction_timestamp() {
        return prediction_timestamp;
    }

    public void setPrediction_timestamp(String prediction_timestamp) {
        this.prediction_timestamp = prediction_timestamp;
    }
}