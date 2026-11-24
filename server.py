"""
Delhi Bus Traffic Model & Journey Planner
==========================================
High-Performance FastAPI Backend Server.
Provides real-time REST endpoints for Delhi transit telemetry, dynamic A* routing,
road congestion modeling, and ML velocity forecasting.

Run with:  uvicorn server:app --reload --port 8000
"""

from __future__ import annotations

import asyncio
import os
import sys
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

# Ensure project root is on sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# Core modules
from data.delhi_bus_stops import BUS_STOPS, BUS_ROUTES
from pipeline.ingestion import (
    load_telemetry,
    fetch_live_delhi_otd,
    derive_delta_speeds,
    DEFAULT_OTD_API_KEY,
)
from pipeline.preprocessing import clean_gps, filter_dwell_times
from traffic.segments import create_delhi_road_network, snap_to_segment
from traffic.model import TrafficModel
from traffic.predictor import TrafficPredictor
from routing.graph import build_graph, update_weights
from routing.planner import plan_route, get_route_geojson, haversine
from routing.branching import get_corridor_branches

DATA_DIR = os.path.join(PROJECT_ROOT, "data")
TELEMETRY_PATH = os.path.join(DATA_DIR, "synthetic_telemetry.csv")

# ---------------------------------------------------------------------------
# FastAPI Application setup
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Delhi Bus Traffic Engine API",
    description="Real-time transit intelligence, dynamic A* routing, and congestion analytics for Delhi.",
    version="2.0.0",
)

# Enable CORS for React frontend (Vite dev server + production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Global State Management
# ---------------------------------------------------------------------------
class AppState:
    def __init__(self):
        self.segments = create_delhi_road_network()
        self.traffic_model = TrafficModel()
        self.routing_graph = build_graph(self.segments)
        self.raw_df: Optional[pd.DataFrame] = None
        self.prev_raw_df: Optional[pd.DataFrame] = None
        self.is_live: bool = False
        self.last_sync_time: str = "Initializing..."
        self.predictor: Optional[TrafficPredictor] = None
        self.is_syncing: bool = False

state = AppState()


def update_model_with_df(df: pd.DataFrame):
    """Clean telemetry and update the traffic model and routing weights."""
    if df is None or df.empty:
        return

    cleaned = clean_gps(df)
    cleaned = filter_dwell_times(cleaned, BUS_STOPS)

    state.raw_df = cleaned
    state.traffic_model.update(cleaned, state.segments)
    state.routing_graph = update_weights(state.routing_graph, state.traffic_model)


def init_baseline():
    """Load baseline synthetic telemetry on startup."""
    try:
        if os.path.exists(TELEMETRY_PATH):
            df = load_telemetry(TELEMETRY_PATH)
            update_model_with_df(df)
            state.last_sync_time = datetime.now().strftime("%I:%M:%S %p")
    except Exception as e:
        print(f"[Warning] Failed to load baseline telemetry: {e}")


def sync_delhi_otd_telemetry(api_key: str = DEFAULT_OTD_API_KEY):
    """Fetch live data from Delhi OTD API, calculate delta velocities, and update model."""
    if state.is_syncing:
        return
    state.is_syncing = True
    try:
        new_raw_df = fetch_live_delhi_otd(api_key=api_key)
        if len(new_raw_df) > 0:
            live_df_with_speeds = derive_delta_speeds(new_raw_df, state.prev_raw_df)
            state.prev_raw_df = new_raw_df.copy()
            update_model_with_df(live_df_with_speeds)
            state.is_live = True
            state.last_sync_time = datetime.now().strftime("%I:%M:%S %p")
            print(f"[Live OTD] Successfully ingested {len(new_raw_df):,} live Delhi buses.")
    except Exception as exc:
        print(f"[Live OTD Notice] Background fetch throttled or socket paused ({exc}). Using cached fleet.")
    finally:
        state.is_syncing = False


# Background periodic sync task
async def background_otd_worker():
    """Poll live Delhi OTD transit feed every 20 seconds in the background."""
    while True:
        await asyncio.sleep(20)
        try:
            await asyncio.to_thread(sync_delhi_otd_telemetry)
        except Exception as e:
            print(f"[Worker Error] {e}")


@app.on_event("startup")
async def on_startup():
    init_baseline()
    # Trigger initial live fetch in thread
    asyncio.create_task(asyncio.to_thread(sync_delhi_otd_telemetry))
    # Start periodic background worker
    asyncio.create_task(background_otd_worker())


# ---------------------------------------------------------------------------
# API Request / Response Models
# ---------------------------------------------------------------------------
class RouteRequest(BaseModel):
    start_lat: float = Field(..., description="Latitude of starting point")
    start_lon: float = Field(..., description="Longitude of starting point")
    end_lat: float = Field(..., description="Latitude of destination")
    end_lon: float = Field(..., description="Longitude of destination")


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------
@app.get("/api/status")
def get_system_status():
    """Return overall real-time telematics status and KPI metrics."""
    df = state.raw_df
    if df is not None and not df.empty and "bus_id" in df.columns:
        if "timestamp" in df.columns:
            latest = df.sort_values("timestamp").groupby("bus_id").last().reset_index()
        else:
            latest = df.groupby("bus_id").last().reset_index()

        total_buses = len(latest)
        speeds = latest["speed"].fillna(0.0) if "speed" in latest.columns else pd.Series([0.0] * total_buses)
        moving_buses = int((speeds >= 5.0).sum())
        idle_buses = max(0, total_buses - moving_buses)
        fleet_avg_speed = float(speeds.mean()) if total_buses > 0 else 0.0
    else:
        total_buses = 0
        moving_buses = 0
        idle_buses = 0
        fleet_avg_speed = 0.0

    return {
        "is_live": state.is_live,
        "telemetry_source": "Live Delhi OTD Feed" if state.is_live else "Synthetic Simulation",
        "last_sync_time": state.last_sync_time,
        "total_active_fleet": total_buses,
        "moving_buses": moving_buses,
        "idle_buses": idle_buses,
        "fleet_avg_speed_kmh": round(fleet_avg_speed, 1),
        "total_road_segments": len(state.segments),
    }


@app.get("/api/fleet")
def get_fleet_telemetry(limit: int = 600, status_filter: Optional[str] = None):
    """
    Return latest coordinates, velocity, and status for active Delhi buses.
    Vectorized for sub-millisecond response time.
    """
    if state.raw_df is None or state.raw_df.empty:
        return []

    df = state.raw_df
    lat_col = "lat" if "lat" in df.columns else "latitude"
    lon_col = "lon" if "lon" in df.columns else "longitude"
    route_col = "route_id" if "route_id" in df.columns else "route"

    if "timestamp" in df.columns:
        latest = df.sort_values("timestamp").groupby("bus_id").last().reset_index()
    else:
        latest = df.groupby("bus_id").last().reset_index()

    speeds = latest["speed"].fillna(0.0).astype(float).round(1) if "speed" in latest.columns else pd.Series([0.0] * len(latest))
    
    conds = [speeds >= 20.0, speeds >= 5.0]
    choices = ["Free Flow", "Moderate"]
    statuses = np.select(conds, choices, default="Slow / Dwell")

    routes = latest[route_col].astype(str) if route_col in latest.columns else ["DTC"] * len(latest)

    fleet = []
    for i in range(min(len(latest), limit)):
        row_status = statuses[i]
        if status_filter and status_filter.lower() not in row_status.lower():
            continue
        fleet.append({
            "bus_id": str(latest["bus_id"].iloc[i]),
            "route_id": str(routes[i]),
            "lat": round(float(latest[lat_col].iloc[i]), 4),
            "lon": round(float(latest[lon_col].iloc[i]), 4),
            "speed": float(speeds[i]),
            "status": row_status,
            "heading": float(latest["heading"].iloc[i]) if "heading" in latest.columns and pd.notna(latest["heading"].iloc[i]) else 0.0,
        })

    return fleet


@app.get("/api/segments")
def get_road_segments():
    """Return all Delhi road network segments with live velocity and congestion status."""
    res = []
    for seg in state.segments:
        speed = state.traffic_model.get_segment_speed(seg.segment_id)
        level = state.traffic_model.get_congestion_level(seg.segment_id)
        res.append({
            "segment_id": seg.segment_id,
            "road_name": seg.road_name,
            "road_type": seg.road_type,
            "length_m": round(seg.length_m, 1),
            "speed_kmh": round(speed, 1),
            "congestion_level": level,
            "coordinates": [
                [seg.start_lat, seg.start_lon],
                [seg.end_lat, seg.end_lon],
            ],
        })
    return res


METRO_INTERCHANGES = {
    "S01": ["Blue Line", "Yellow Line"],
    "S02": ["Blue Line", "Yellow Line"],
    "S03": ["Yellow Line", "Violet Line"],
    "S04": ["Blue Line", "Violet Line"],
    "S05": ["Yellow Line"],
    "S06": ["Red Line", "Yellow Line", "Violet Line"],
    "S07": ["Yellow Line"],
    "S08": ["Violet Line"],
    "S09": ["Violet Line"],
    "S10": ["Violet Line"],
    "S11": ["Yellow Line"],
    "S12": ["Yellow Line", "Pink Line"],
    "S13": ["Pink Line"],
    "S14": ["Violet Line", "Pink Line"],
    "S15": ["Violet Line"],
    "S16": ["Violet Line", "Magenta Line"],
    "S17": ["Violet Line"],
    "S18": ["Yellow Line"],
    "S19": ["Yellow Line", "Magenta Line"],
    "S20": ["Yellow Line"],
    "S21": ["Airport Express", "Pink Line"],
    "S22": ["Blue Line"],
    "S23": ["Blue Line"],
    "S24": ["Blue Line"],
    "S25": ["Blue Line"],
    "S26": ["Red Line"],
    "S27": ["Red Line"],
    "S28": ["Red Line"],
    "S29": ["Red Line"],
    "S30": ["Red Line", "Pink Line"],
    "S31": ["Red Line"],
    "S32": ["Red Line"],
    "S33": ["Red Line"],
    "S34": ["Red Line"],
    "S35": ["Yellow Line", "Pink Line"],
    "S36": ["Yellow Line"],
    "S37": ["Yellow Line"],
    "S38": ["Yellow Line"],
    "S39": ["Yellow Line"],
    "S40": ["Yellow Line"],
    "S41": ["Blue Line"],
    "S42": ["Blue Line"],
    "S43": ["Blue Line"],
    "S44": ["Blue Line", "Pink Line", "RRTS"],
    "S45": ["Blue Line", "Pink Line"],
    "S46": ["Blue Line", "Magenta Line"],
    "S47": ["Blue Line"],
    "S48": ["Blue Line"],
    "S49": ["Blue Line", "Magenta Line"],
    "S50": ["Blue Line", "Airport Express"],
}

@app.get("/api/stops")
def get_bus_stops():
    """Return all bus stops with geographic coordinates, served route IDs, and Metro connectivity."""
    try:
        stop_route_map = {}
        for route in BUS_ROUTES:
            for sid in route.get("stop_ids", []):
                if sid not in stop_route_map:
                    stop_route_map[sid] = []
                stop_route_map[sid].append(route.get("name", route.get("route_id", "?")))
    except Exception:
        stop_route_map = {}

    stops_data = []
    for s in BUS_STOPS:
        sid = s.get("stop_id", "")
        stops_data.append({
            "stop_id": sid,
            "name": s["name"],
            "lat": s["lat"],
            "lon": s["lon"],
            "routes": stop_route_map.get(sid, []),
            "metro_lines": METRO_INTERCHANGES.get(sid, []),
        })
    return stops_data


@app.get("/api/heatmap")
def get_heatmap():
    """Return normalized congestion intensity coordinates for rendering heatmaps."""
    return state.traffic_model.get_heatmap_data()


@app.get("/api/predictions")
def get_traffic_predictions():
    """Return ML forecasting (+30m, +60m) for Delhi road corridors."""
    if state.predictor is None:
        state.predictor = TrafficPredictor()
        if state.raw_df is not None and not state.raw_df.empty:
            train_rows = []
            for _, row in state.raw_df.head(300).iterrows():
                if pd.notna(row.get("lat")) and pd.notna(row.get("lon")) and pd.notna(row.get("speed")):
                    seg = snap_to_segment(float(row["lat"]), float(row["lon"]), state.segments)
                    train_rows.append({
                        "segment_id": seg.segment_id,
                        "speed": float(row["speed"]),
                        "timestamp": row.get("timestamp", "2026-11-21 09:00:00"),
                    })
            if train_rows:
                state.predictor.train(pd.DataFrame(train_rows))

    pred_rows = []
    for seg in state.segments[:25]:
        cur_spd = state.traffic_model.get_segment_speed(seg.segment_id)
        try:
            speed_30 = state.predictor.predict(seg.segment_id, future_minutes=30)
            speed_60 = state.predictor.predict(seg.segment_id, future_minutes=60)
        except Exception:
            speed_30 = speed_60 = cur_spd

        diff_30 = speed_30 - cur_spd
        trend = "Speeding Up" if diff_30 >= 1.5 else ("Slowing Down" if diff_30 <= -1.5 else "Steady")

        pred_rows.append({
            "road_name": seg.road_name,
            "road_type": seg.road_type.title(),
            "current_speed_kmh": round(cur_spd, 1),
            "forecast_30m_kmh": round(speed_30, 1),
            "forecast_60m_kmh": round(speed_60, 1),
            "trend": trend,
        })
    return pred_rows


@app.post("/api/route")
def calculate_optimal_route(req: RouteRequest):
    """Calculate the fastest dynamic A* route between two GPS coordinates."""
    try:
        route = plan_route(
            state.routing_graph,
            req.start_lat,
            req.start_lon,
            req.end_lat,
            req.end_lon,
        )
        geojson = get_route_geojson(route)

        eta = route.get("eta_minutes", 0.0)
        dist = route.get("distance_km", 0.0)
        eff_spd = (dist / (eta / 60.0)) if eta > 0 else 30.0

        # DTC standard transit fare calculation (<4km: Rs.10, 4-10km: Rs.15, >10km: Rs.25)
        fare = 10 if dist < 4.0 else (15 if dist <= 10.0 else 25)

        # Carbon footprint offset (avg car emits ~140g CO2/km vs ~30g/passenger-km on DTC CNG/EV bus)
        carbon_saved = round(dist * 0.11, 2)

        # Generate turn-by-turn commuter itinerary
        segs_list = route.get("segments", [])
        itinerary = []
        if segs_list:
            itinerary.append({
                "step": 1,
                "icon": "🚶",
                "type": "walk",
                "instruction": f"Proceed to nearest corridor at {segs_list[0]}",
                "meta": "Walk ~2 mins",
            })
            for idx, s_name in enumerate(segs_list, start=2):
                itinerary.append({
                    "step": idx,
                    "icon": "🚌",
                    "type": "transit",
                    "instruction": f"Transit via {s_name}",
                    "meta": "In Transit",
                })
            itinerary.append({
                "step": len(segs_list) + 2,
                "icon": "🏁",
                "type": "arrive",
                "instruction": f"Arrive at destination ({dist:.1f} km total)",
                "meta": f"ETA ~{eta:.0f} mins",
            })

        # Extract ordered [lat, lon] waypoints for smooth frontend animation and HUD
        route_latlngs = []
        if geojson and "features" in geojson and len(geojson["features"]) > 0:
            coords = geojson["features"][0].get("geometry", {}).get("coordinates", [])
            route_latlngs = [[round(float(c[1]), 5), round(float(c[0]), 5)] for c in coords]

        return {
            "success": True,
            "distance_km": round(dist, 2),
            "eta_minutes": round(eta, 1),
            "effective_speed_kmh": round(eff_spd, 1),
            "fare_inr": fare,
            "carbon_saved_kg": carbon_saved,
            "itinerary": itinerary,
            "segments_count": len(route.get("segments", [])),
            "segments": route.get("segments", []),
            "geojson": geojson,
            "route_latlngs": route_latlngs,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Routing failed: {str(e)}")


@app.get("/api/stop-arrivals/{stop_id}")
def get_stop_live_arrivals(stop_id: str):
    """
    Calculate real-time upcoming bus arrivals for a specific bus stop
    based on live GPS positions, route assignments, and current segment speeds.
    """
    target_stop = next((s for s in BUS_STOPS if s["stop_id"].upper() == stop_id.upper()), None)
    if not target_stop:
        raise HTTPException(status_code=404, detail="Stop not found")

    arrivals = []
    if state.raw_df is not None and not state.raw_df.empty:
        df = state.raw_df.copy()
        lat_col = "lat" if "lat" in df.columns else "latitude"
        lon_col = "lon" if "lon" in df.columns else "longitude"

        for _, row in df.iterrows():
            blat = float(row[lat_col])
            blon = float(row[lon_col])
            dist_m = haversine(blat, blon, target_stop["lat"], target_stop["lon"])
            dist_km = dist_m / 1000.0

            if dist_km <= 7.5:
                speed = float(row.get("speed", 18.0))
                eff_speed = max(speed, 12.0)
                eta_minutes = round((dist_km / eff_speed) * 60.0)

                arrivals.append({
                    "bus_id": str(row.get("bus_id", "Bus")),
                    "route_id": str(row.get("route_id", "DTC")),
                    "distance_km": round(dist_km, 2),
                    "current_speed_kmh": round(speed, 1),
                    "eta_minutes": max(1, eta_minutes),
                    "status": "Arriving Now" if eta_minutes <= 2 else ("Approaching" if eta_minutes <= 5 else "In Transit"),
                })

    arrivals.sort(key=lambda x: x["eta_minutes"])
    return {
        "stop_id": target_stop["stop_id"],
        "stop_name": target_stop["name"],
        "coordinates": [target_stop["lat"], target_stop["lon"]],
        "total_incoming_buses": len(arrivals),
        "arrivals": arrivals[:10],
    }


@app.get("/api/alerts")
def get_live_traffic_and_fleet_alerts():
    """
    Generate real-time road choke points and fleet bunching (bus clumping) alerts.
    """
    alerts = {
        "bottlenecks": [],
        "bunching": [],
        "timestamp": datetime.now().strftime("%I:%M:%S %p"),
    }

    # 1. Congestion Choke Points
    for seg in state.segments:
        speed = state.traffic_model.get_segment_speed(seg.segment_id)
        level = state.traffic_model.get_congestion_level(seg.segment_id)
        if level in ["heavy", "gridlock", "severe"] or speed < 14.0:
            severity = "CRITICAL" if speed < 10.0 else "WARNING"
            alerts["bottlenecks"].append({
                "segment_id": seg.segment_id,
                "road_name": seg.road_name,
                "road_type": seg.road_type,
                "speed_kmh": round(speed, 1),
                "congestion_level": level,
                "severity": severity,
                "delay_factor": round(35.0 / max(speed, 4.0), 1),
                "message": f"{seg.road_name}: Velocity dropped to {speed:.1f} km/h ({level.upper()})",
            })

    alerts["bottlenecks"].sort(key=lambda x: x["speed_kmh"])

    # 2. Fleet Bunching Detection (< 350m headway between buses on same route)
    if state.raw_df is not None and not state.raw_df.empty:
        df = state.raw_df.copy()
        lat_col = "lat" if "lat" in df.columns else "latitude"
        lon_col = "lon" if "lon" in df.columns else "longitude"
        route_col = "route_id" if "route_id" in df.columns else None

        if route_col:
            grouped = df.groupby(route_col)
            for r_id, group in grouped:
                if len(group) >= 2:
                    rows = group.to_dict("records")
                    for i in range(len(rows)):
                        for j in range(i + 1, min(len(rows), i + 4)):
                            p1 = (float(rows[i][lat_col]), float(rows[i][lon_col]))
                            p2 = (float(rows[j][lat_col]), float(rows[j][lon_col]))
                            dist_m = haversine(p1[0], p1[1], p2[0], p2[1])
                            if dist_m < 350.0:
                                b1_id = str(rows[i].get("bus_id", "Bus1"))
                                b2_id = str(rows[j].get("bus_id", "Bus2"))
                                alerts["bunching"].append({
                                    "route_id": str(r_id),
                                    "bus_1": b1_id,
                                    "bus_2": b2_id,
                                    "gap_meters": round(dist_m),
                                    "message": f"Route {r_id}: Buses #{b1_id} and #{b2_id} clumped together ({dist_m:.0f}m gap)",
                                    "recommendation": "Hold trailing bus at next stop to restore headway",
                                })

    return alerts


@app.get("/api/corridor-branches")
def get_corridor_branches_endpoint(origin: str = "Connaught Place", destination: str = "AIIMS"):
    """
    Analyze multi-route corridor branching and bus distributions between 2 stops.
    """
    fleet_data = get_fleet_telemetry(limit=1000)
    return get_corridor_branches(origin, destination, fleet_data)


@app.post("/api/resolve-bunching")
def resolve_bunching_dispatch(route_id: str, hold_minutes: int = 4):
    """
    Simulated dispatch instruction to hold a clumping bus and rebalance headway.
    """
    return {
        "status": "DISPATCH_COMMAND_ISSUED",
        "route_id": route_id,
        "hold_duration_minutes": hold_minutes,
        "action": f"Holding trailing bus on Route {route_id} for {hold_minutes} minutes at upcoming terminal",
        "projected_headway_recovery": "8.5 minutes (Standard Timetable)",
        "timestamp": datetime.now().strftime("%I:%M:%S %p"),
    }


@app.post("/api/refresh")
async def force_refresh(bg: BackgroundTasks):
    """Trigger an immediate live telemetry sync in the background."""
    bg.add_task(sync_delhi_otd_telemetry)
    return {"message": "Live sync initiated in background.", "timestamp": time.time()}


# ---------------------------------------------------------------------------
# Static frontend mounting (Unified Full-Stack Mode)
# ---------------------------------------------------------------------------
FRONTEND_DIST = os.path.join(PROJECT_ROOT, "frontend-react", "dist")
STATIC_DIR = os.path.join(PROJECT_ROOT, "static")


@app.get("/", include_in_schema=False)
async def serve_root():
    """Serve the unified single-page application entrypoint."""
    static_index = os.path.join(STATIC_DIR, "index.html")
    dist_index = os.path.join(FRONTEND_DIST, "index.html")
    if os.path.exists(static_index):
        return FileResponse(static_index)
    if os.path.exists(dist_index):
        return FileResponse(dist_index)
    return {"status": "ok", "message": "Delhi Bus Traffic Engine API is active. Static frontend not found."}


# Mount assets directory if React Vite build is present
if os.path.exists(os.path.join(FRONTEND_DIST, "assets")):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")

# Mount static folder for auxiliary files
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Catch-all fallback for client-side single page apps
if os.path.exists(FRONTEND_DIST):
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend_dist")
elif os.path.exists(STATIC_DIR):
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="frontend_static")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    print("\n" + "=" * 65)
    print(" 🚀 DELHI BUS TRAFFIC MODEL & JOURNEY PLANNER")
    print(" 🌐 Unified Full-Stack Service Active (Frontend + Backend Merged)")
    print(f" 📍 App Interface:  http://localhost:{port}")
    print(f" 📖 Interactive Docs: http://localhost:{port}/docs")
    print("=" * 65 + "\n")
    uvicorn.run("server:app", host=host, port=port, reload=True)

