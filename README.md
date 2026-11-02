# 🌋 SeismoScope — Global Seismic Hazards & Spatial Risk Intelligence

> **AWS Builder Center Hackathon Entry**: *Weekend Challenge: Map It*  
> **Live Web Application**: [http://seismoscope-app-528582359305.s3-website-us-east-1.amazonaws.com](http://seismoscope-app-528582359305.s3-website-us-east-1.amazonaws.com)  
> **Live API Gateway Endpoint**: `https://ffz5g978r3.execute-api.us-east-1.amazonaws.com/prod/earthquakes`  
> **License**: MIT (Approved OSI Open Source License)

---

## 📌 Overview

**SeismoScope** is an interactive, GPU-accelerated geospatial intelligence platform that visualizes real-time global seismic hazards, tectonic fault lines, and earthquake density patterns across the globe. Built entirely on an **AWS Serverless Data Pipeline**, it transforms open public datasets into an exploratory, high-performance web experience.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      END USER CLIENT                        │
│          MapLibre GL JS + Vector Hardware Acceleration      │
└──────────────────────────────┬──────────────────────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
┌──────────────────────────────┐     ┌────────────────────────┐
│      Amazon S3 Website       │     │   Amazon API Gateway   │
│  Static Single Page App      │     │       (REST API)       │
│  + GeoJSON Data Pipeline     │     └───────────┬────────────┘
└──────────────────────────────┘                 │
                                                 ▼
                                     ┌────────────────────────┐
                                     │    AWS Lambda Backend  │
                                     │   (Python 3.11 Engine) │
                                     └───────────┬────────────┘
                                                 │
                                                 ▼
                                     ┌────────────────────────┐
                                     │  USGS GeoJSON API Lake │
                                     │    (Live Shock Feeds)  │
                                     └────────────────────────┘
```

### AWS Cloud Stack
- **Amazon S3**: Hosts the high-performance Single Page App (`index.html`) and serves the spatial GeoJSON data pipeline (`/data/quakes_30d.geojson`).
- **AWS Lambda (`SeismoScopeBackendLambda`)**: Serverless Python 3.11 compute engine filtering events dynamically by magnitude, depth, and bounding-box.
- **Amazon API Gateway**: Managed REST API proxy delivering live queries with automatic CORS and DDoS shielding.
- **Amazon Location Service / OpenFreeMap**: Clean, watermark-free vector basemaps with high-contrast Dark, Satellite, and Streets layers.

---

## ✨ Key Features

1. **GPU Heatmaps**: Dynamic WebGL-accelerated kernel density maps showing tectonic stress accumulation.
2. **Interactive Spatial Clustering**: Hierarchical marker clusters with smooth zoom transitions and count badges.
3. **Magnitude Filter Slider**: Instant slider filtering from $M2.5 \to M7.0+$.
4. **Contextual Risk Intelligence**: Dynamic viewport evaluation calculating real-time hazard ratings (`CRITICAL`, `ELEVATED`, `MODERATE`, or `LOW`).
5. **Instant City Geocoding**: Search bar autocomplete to fly to any global city or tectonic zone in milliseconds.
6. **Station Metadata Popups**: Inspect exact focal depth in km, UTC timestamps, coordinates, and direct links to USGS technical sheets.

---

## 🚀 Local Development

### 1. Fetch Latest Data
```bash
python fetch_data.py
```
This queries the USGS API and compiles the latest seismic events into `data/quakes_30d.geojson`.

### 2. Run Local Server
```bash
python -m http.server 8000
```
Open `http://localhost:8000` in any web browser.

---

## 📂 Repository Structure

```
.
├── index.html                     # Full MapLibre GL frontend with spatial layers
├── fetch_data.py                  # Python data pipeline script for USGS ingestion
├── lambda/
│   └── lambda_function.py        # AWS Lambda serverless query handler
├── data/
│   └── quakes_30d.geojson        # Compressed GeoJSON dataset (~2,000+ events)
├── AWS_BUILDER_CENTER_ARTICLE.md  # Official AWS Builder Center submission article
├── LICENSE                        # MIT License
└── README.md                      # Project documentation
```

---

## 📄 License
This project is open-sourced under the [MIT License](LICENSE).
