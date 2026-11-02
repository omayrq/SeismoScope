import json
import urllib.request
import urllib.parse
import os

# Configuration
USGS_BASE = "https://earthquake.usgs.gov/fdsnws/event/1/query"

def lambda_handler(event, context):
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "GET,OPTIONS",
        "Content-Type": "application/json"
    }

    # Handle CORS preflight
    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 200, "headers": cors_headers, "body": ""}

    # Parse query parameters
    params = event.get("queryStringParameters") or {}
    start_time  = params.get("starttime", "2026-10-02")
    end_time    = params.get("endtime",   "2026-11-02")
    min_mag     = params.get("minmagnitude", "2.5")
    max_mag     = params.get("maxmagnitude", "10.0")
    min_lat     = params.get("minlatitude",  "-90")
    max_lat     = params.get("maxlatitude",   "90")
    min_lon     = params.get("minlongitude", "-180")
    max_lon     = params.get("maxlongitude",  "180")
    limit       = min(int(params.get("limit", "3000")), 5000)

    usgs_params = {
        "format": "geojson",
        "starttime": start_time,
        "endtime": end_time,
        "minmagnitude": min_mag,
        "maxmagnitude": max_mag,
        "minlatitude": min_lat,
        "maxlatitude": max_lat,
        "minlongitude": min_lon,
        "maxlongitude": max_lon,
        "orderby": "time",
        "limit": str(limit)
    }

    usgs_url = USGS_BASE + "?" + urllib.parse.urlencode(usgs_params)

    try:
        req = urllib.request.Request(usgs_url, headers={"User-Agent": "SeismoScope-Lambda/1.0"})
        with urllib.request.urlopen(req, timeout=25) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        # Add SeismoScope metadata
        data["seismoscope"] = {
            "query": usgs_params,
            "count": len(data.get("features", [])),
            "powered_by": "USGS Earthquake Hazards Program + AWS Lambda"
        }

        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": json.dumps(data, separators=(",", ":"))
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": cors_headers,
            "body": json.dumps({"error": str(e), "usgs_url": usgs_url})
        }
