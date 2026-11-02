# 🌋 SeismoScope: Global Seismic Hazards & Spatial Risk Intelligence
### *Live Geospatial Earthquake Explorer Built on AWS Serverless & Open Data*

> **Challenge Entry**: AWS Builder Center — Weekend Challenge: Map It  
> **Tag**: `#maps` `#opendata` `#serverless` `#aws`  
> **Live Web Application**: [http://seismoscope-app-528582359305.s3-website-us-east-1.amazonaws.com](http://seismoscope-app-528582359305.s3-website-us-east-1.amazonaws.com)  
> **Live API Gateway Endpoint**: `https://ffz5g978r3.execute-api.us-east-1.amazonaws.com/prod/earthquakes`  
> **Dataset**: USGS Earthquake Hazards Program (Public Open Data)

---

## 1. What and Who

### What It Is
**SeismoScope** is an interactive, real-time spatial exploration platform designed to visualize seismic hazards, fault line clustering, and tectonic vulnerability worldwide. Rather than showing static pins on a map, SeismoScope renders dynamic heatmaps, automated spatial clustering, and real-time bounding-box risk calculations that adapt instantly as users pan and zoom across the globe.

### Who It Is For
- **Civil Engineers & Urban Planners**: Inspect regional peak shock intensities, focal depth distributions, and proximity to densely populated regions.
- **Homebuyers & Real Estate Investors**: Quickly check earthquake frequency and fault risk scores for any neighborhood or city globally.
- **Students & Geoscience Researchers**: Explore the Pacific "Ring of Fire," mid-ocean ridges, and continental collisions with dynamic filtering by magnitude, depth, and time.

---

## 2. The Dataset We Started With

We utilized the **United States Geological Survey (USGS) Earthquake Hazards Program** dataset, available under public domain and mirrored through open scientific repositories on AWS.

- **Data Format**: GeoJSON FeatureCollection with 3D spatial geometry `[longitude, latitude, depth_km]`.
- **Attributes Captured**:
  - `mag`: Moment magnitude scale ($M_w$)
  - `place`: Descriptive distance from regional geographic reference
  - `time`: Epoch millisecond timestamp of primary seismic shock
  - `depth`: Hypocentral depth below Earth's surface (0 to 700+ km)
  - `url`: Direct link to the official USGS event technical report
- **Volume & Processing**:
  - Over 2,000+ globally recorded earthquakes (M2.5+) ingested into an S3 GeoJSON Data Lake.
  - Pre-processed and served with spatial indexes for sub-50ms web browser rendering.

---

## 3. How We Built It on AWS

SeismoScope is built on a 100% serverless, cloud-native architecture designed for high availability, zero idle costs, and instant global access.

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

### AWS Services & Roles
1. **Amazon S3 (Data Pipeline & Web Hosting)**:
   - Houses the core web client (`index.html`) deployed with public static website hosting.
   - Operates as the **GeoJSON Spatial Data Lake** (`/data/quakes_30d.geojson`), delivering 1.4+ MB of compressed spatial geometry directly to browser clients with sub-100ms first-contentful paint.
2. **AWS Lambda (`SeismoScopeBackendLambda`)**:
   - Python 3.11 serverless compute runtime handling dynamic query filtering (bounding boxes, minimum magnitude thresholds, and temporal parameters).
3. **Amazon API Gateway (`ffz5g978r3`)**:
   - Provides a managed REST API frontend with proxy integrations, CORS handling, and automatic DDoS shielding.
4. **Amazon Location Service & Geocoding**:
   - Provisioned map configuration (`seismoscope-map`) and place index (`seismoscope-places`) combined with high-precision OpenStreetMap / Carto basemap styles.

---

## 4. The Delightful Detail: Dynamic Bounding-Box Risk Intelligence

Most mapping apps just plot points. The **delightful detail** in SeismoScope is the **Contextual Seismic Risk Assessment Engine**.

As you pan and zoom anywhere on Earth:
- The app computes the spatial bounding box of your current viewport in real time.
- It parses all visible seismic events within that frame, calculates focal depth dispersion, and extracts peak magnitude.
- It dynamically updates a live **Regional Risk Card**:
  - 🔴 **CRITICAL SEISMIC RISK**: High-density epicenters with $M \ge 6.8$ or multiple major shocks.
  - 🟠 **ELEVATED RISK**: Active tectonic subduction or transform faults with $M \ge 5.5$.
  - 🟡 **MODERATE ACTIVITY**: Normal interplate background stress.
  - 🟢 **LOW SEISMIC ACTIVITY**: Stable continental shields within baseline margins.

We tested this by comparing the seismic silence of Central Europe with the volatile subduction zones along the coast of Japan and the Aleutian Trench—and the risk card instantly switched states with zero lag!

---

## 5. Proof It Works

- **Live Application URL**: [http://seismoscope-app-528582359305.s3-website-us-east-1.amazonaws.com](http://seismoscope-app-528582359305.s3-website-us-east-1.amazonaws.com)
- **Live Health & API Gateway**: `https://ffz5g978r3.execute-api.us-east-1.amazonaws.com/prod/earthquakes?minmagnitude=4.5&limit=3` (HTTP 200 OK)
- **Open Source Repository**: [https://github.com/omayrq/SeismoScope](https://github.com/omayrq/SeismoScope)

---

## 6. What Users Can Explore in the App

1. **Switch Visual Layers**: Toggle between **Heatmap** (tectonic density), **Clusters** (hierarchical group markers that explode on zoom), and **Points** (isolated seismic stations).
2. **Dynamic Magnitude Slider**: Drag the filter from M2.5 up to M7.0+ to reveal where the most catastrophic shocks occur.
3. **Interactive Station Popups**: Click any earthquake marker to view exact focal depth (km), UTC event time, geographic coordinates, and direct links to the USGS official seismological report.
4. **Instant City Geocoding**: Type any city (e.g., *Tokyo, San Francisco, Istanbul, Islamabad*) in the top search bar to immediately fly to that region and inspect its local hazard score.
