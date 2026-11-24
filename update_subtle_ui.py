# Script to update static/index.html with subtle, elegant styling and effortless search locator
import os

html_code = r'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Delhi Transit Intelligence & Dynamic Journey Planner</title>
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚌</text></svg>" />

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">

  <!-- Leaflet GIS CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

  <!-- React 18, ReactDOM & Babel -->
  <script src="https://unpkg.com/react@18/umd/react.production.min.js" crossorigin></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

  <style>
    :root {
      --bg-base: #0b0f19;
      --bg-card: rgba(17, 24, 39, 0.82);
      --bg-card-hover: rgba(31, 41, 55, 0.9);
      --bg-elevated: #161f30;
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-accent: rgba(249, 115, 22, 0.5);
      --border-focus: #f97316;
      --text-main: #f9fafb;
      --text-muted: #9ca3af;
      --text-dim: #6b7280;
      --primary: #f97316;
      --primary-subtle: rgba(249, 115, 22, 0.12);
      --accent-cyan: #38bdf8;
      --accent-emerald: #10b981;
      --accent-amber: #f59e0b;
      --accent-rose: #f43f5e;
      --card-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4);
    }

    [data-theme="light"] {
      --bg-base: #f8fafc;
      --bg-card: rgba(255, 255, 255, 0.92);
      --bg-card-hover: rgba(241, 245, 249, 0.95);
      --bg-elevated: #f1f5f9;
      --border-subtle: rgba(0, 0, 0, 0.08);
      --border-accent: rgba(249, 115, 22, 0.6);
      --border-focus: #ea580c;
      --text-main: #0f172a;
      --text-muted: #64748b;
      --text-dim: #94a3b8;
      --primary: #ea580c;
      --primary-subtle: rgba(234, 88, 12, 0.08);
      --accent-cyan: #0284c7;
      --accent-emerald: #059669;
      --accent-amber: #d97706;
      --accent-rose: #e11d48;
      --card-shadow: 0 4px 18px -2px rgba(0, 0, 0, 0.06);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: var(--bg-base);
      color: var(--text-main);
      min-height: 100vh;
      overflow-x: hidden;
      transition: background-color 0.25s ease, color 0.25s ease;
      -webkit-font-smoothing: antialiased;
    }

    .top-tricolor-bar {
      height: 3px;
      background: linear-gradient(90deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
      width: 100%;
      opacity: 0.9;
    }

    .glass-panel {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      box-shadow: var(--card-shadow);
      transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }

    .glass-panel:hover {
      border-color: rgba(255, 255, 255, 0.14);
    }

    /* Leaflet Clean Styling */
    .leaflet-container {
      font-family: inherit;
      background: #0b0f19 !important;
    }

    .leaflet-popup-content-wrapper {
      background: var(--bg-card) !important;
      color: var(--text-main) !important;
      border: 1px solid var(--border-subtle) !important;
      border-radius: 10px !important;
      box-shadow: 0 8px 24px rgba(0,0,0,0.5) !important;
      backdrop-filter: blur(16px) !important;
      padding: 2px !important;
    }
    .leaflet-popup-tip {
      background: var(--bg-card) !important;
      border: 1px solid var(--border-subtle) !important;
    }

    .leaflet-control-layers {
      background: var(--bg-card) !important;
      border: 1px solid var(--border-subtle) !important;
      border-radius: 10px !important;
      color: var(--text-main) !important;
      backdrop-filter: blur(16px) !important;
      box-shadow: 0 4px 16px rgba(0,0,0,0.3) !important;
      padding: 8px 12px !important;
    }
    .leaflet-control-layers label {
      color: var(--text-main) !important;
      font-size: 11.5px !important;
      font-weight: 600 !important;
      margin-bottom: 5px !important;
      cursor: pointer !important;
      display: flex !important;
      align-items: center !important;
      gap: 6px !important;
    }

    .leaflet-control-zoom {
      border: 1px solid var(--border-subtle) !important;
      border-radius: 8px !important;
      overflow: hidden !important;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3) !important;
    }
    .leaflet-control-zoom a {
      background: var(--bg-card) !important;
      color: var(--text-main) !important;
      border-color: var(--border-subtle) !important;
      transition: background 0.15s ease !important;
    }
    .leaflet-control-zoom a:hover {
      background: var(--bg-elevated) !important;
      color: var(--primary) !important;
    }

    @keyframes subtlePulse {
      0% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.7; transform: scale(1.1); }
      100% { opacity: 1; transform: scale(1); }
    }

    .pulse-dot-green {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background-color: #10b981;
      display: inline-block;
      animation: subtlePulse 2s infinite ease-in-out;
    }

    .pulse-dot-orange {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background-color: #f97316;
      display: inline-block;
      animation: subtlePulse 2s infinite ease-in-out;
    }

    .pulse-dot-cyan {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background-color: #38bdf8;
      display: inline-block;
      animation: subtlePulse 1.6s infinite ease-in-out;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #374151; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #4b5563; }

    .metro-badge {
      display: inline-flex;
      align-items: center;
      gap: 3px;
      background: rgba(99, 102, 241, 0.12);
      border: 1px solid rgba(99, 102, 241, 0.3);
      color: #a5b4fc;
      padding: 1px 6px;
      border-radius: 10px;
      font-size: 0.66rem;
      font-weight: 600;
      white-space: nowrap;
    }

    .toast-container {
      position: fixed;
      bottom: 20px;
      right: 20px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      gap: 8px;
      pointer-events: none;
    }

    .toast-item {
      pointer-events: auto;
      background: var(--bg-card);
      color: var(--text-main);
      border: 1px solid var(--border-accent);
      border-radius: 8px;
      padding: 10px 16px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.5);
      backdrop-filter: blur(12px);
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 0.82rem;
      font-weight: 600;
      animation: slideInRight 0.25s ease;
      min-width: 260px;
    }

    @keyframes slideInRight {
      from { transform: translateX(100%); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }

    .hud-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 10px 14px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
      backdrop-filter: blur(14px);
    }
  </style>
</head>
<body>
  <div id="root"></div>

  <script type="text/babel">
    const { useState, useEffect, useRef, useMemo, useCallback } = React;

    const CONGESTION_COLORS = {
      free_flow: '#10b981',
      moderate: '#f59e0b',
      heavy: '#f97316',
      gridlock: '#f43f5e',
      severe: '#f43f5e',
    };

    function speakText(text) {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(text);
        u.lang = 'en-IN';
        u.rate = 1.0;
        window.speechSynthesis.speak(u);
      }
    }

    // --- Search & Autocomplete Stop Input Component ---
    function StopAutocomplete({ label, value, onChange, stops, placeholder, icon, autoFocus }) {
      const [isOpen, setIsOpen] = useState(false);
      const [search, setSearch] = useState('');
      const wrapperRef = useRef(null);

      useEffect(() => {
        setSearch(value || '');
      }, [value]);

      useEffect(() => {
        function handleClickOutside(event) {
          if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
            setIsOpen(false);
          }
        }
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
      }, []);

      const filteredStops = useMemo(() => {
        const q = search.trim().toLowerCase();
        if (!q) return stops.slice(0, 8);
        return stops.filter(s =>
          s.name.toLowerCase().includes(q) ||
          s.stop_id.toLowerCase().includes(q) ||
          (s.metro_lines || []).some(m => m.toLowerCase().includes(q))
        ).slice(0, 8);
      }, [search, stops]);

      return (
        <div ref={wrapperRef} style={{ position: 'relative', width: '100%' }}>
          {label && (
            <label style={{ fontSize: '0.72rem', color: 'var(--text-muted)', display: 'block', marginBottom: '4px', fontWeight: 600 }}>
              {label}
            </label>
          )}
          <div style={{ position: 'relative' }}>
            <span style={{ position: 'absolute', left: '10px', top: '50%', transform: 'translateY(-50%)', fontSize: '0.9rem', pointerEvents: 'none' }}>
              {icon}
            </span>
            <input
              type="text"
              value={search}
              autoFocus={autoFocus}
              placeholder={placeholder || 'Search stop or metro interchange...'}
              onFocus={() => setIsOpen(true)}
              onChange={e => {
                setSearch(e.target.value);
                setIsOpen(true);
              }}
              style={{
                width: '100%',
                background: 'var(--bg-elevated)',
                color: 'var(--text-main)',
                border: '1px solid var(--border-subtle)',
                borderRadius: '8px',
                padding: '8px 12px 8px 32px',
                fontSize: '0.82rem',
                fontWeight: 600,
                outline: 'none',
                transition: 'border-color 0.15s ease',
              }}
              onFocusCapture={e => e.target.style.borderColor = 'var(--border-accent)'}
              onBlurCapture={e => e.target.style.borderColor = 'var(--border-subtle)'}
            />
            {search && (
              <button
                type="button"
                onClick={() => { setSearch(''); onChange(''); setIsOpen(true); }}
                style={{
                  position: 'absolute', right: '8px', top: '50%', transform: 'translateY(-50%)',
                  background: 'transparent', border: 'none', color: 'var(--text-dim)', cursor: 'pointer', fontSize: '0.75rem'
                }}
              >
                ✕
              </button>
            )}
          </div>

          {isOpen && (
            <div style={{
              position: 'absolute', top: '100%', left: 0, right: 0, zIndex: 1200,
              background: 'var(--bg-card)', border: '1px solid var(--border-subtle)',
              borderRadius: '8px', marginTop: '4px', maxHeight: '220px', overflowY: 'auto',
              boxShadow: '0 8px 24px rgba(0,0,0,0.5)', backdropFilter: 'blur(16px)'
            }}>
              {filteredStops.length > 0 ? (
                filteredStops.map(s => (
                  <div
                    key={s.stop_id}
                    onClick={() => {
                      onChange(s.name);
                      setSearch(s.name);
                      setIsOpen(false);
                    }}
                    style={{
                      padding: '7px 12px', borderBottom: '1px solid var(--border-subtle)',
                      cursor: 'pointer', transition: 'background 0.15s ease',
                    }}
                    onMouseEnter={e => e.currentTarget.style.background = 'var(--bg-card-hover)'}
                    onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <strong style={{ fontSize: '0.82rem', color: 'var(--text-main)' }}>{s.name}</strong>
                      <span style={{ fontSize: '0.68rem', color: 'var(--text-dim)', fontFamily: "'JetBrains Mono', monospace" }}>{s.stop_id}</span>
                    </div>
                    {s.metro_lines && s.metro_lines.length > 0 && (
                      <div style={{ display: 'flex', gap: '3px', flexWrap: 'wrap', marginTop: '2px' }}>
                        {s.metro_lines.map((m, mIdx) => (
                          <span key={mIdx} className="metro-badge">🚇 {m}</span>
                        ))}
                      </div>
                    )}
                  </div>
                ))
              ) : (
                <div style={{ padding: '8px', fontSize: '0.76rem', color: 'var(--text-dim)', textAlign: 'center' }}>
                  No stops found matching "{search}"
                </div>
              )}
            </div>
          )}
        </div>
      );
    }

    // --- Main App Component ---
    function App() {
      const [theme, setTheme] = useState('dark');
      const [status, setStatus] = useState({});
      const [fleet, setFleet] = useState([]);
      const [segments, setSegments] = useState([]);
      const [stops, setStops] = useState([]);
      const [predictions, setPredictions] = useState([]);
      const [activeTab, setActiveTab] = useState('map');

      // Journey Planning State
      const [selectedSrc, setSelectedSrc] = useState('Connaught Place');
      const [selectedDst, setSelectedDst] = useState('AIIMS');
      const [route, setRoute] = useState(null);
      const [clickPoints, setClickPoints] = useState({ start: null, end: null });

      // Quick Locator state (Global Quick Search)
      const [quickSearch, setQuickSearch] = useState('');
      const [quickSearchResults, setQuickSearchResults] = useState([]);
      const [isQuickOpen, setIsQuickOpen] = useState(false);

      // Map Viewport and Layer Controls
      const [corridorFocus, setCorridorFocus] = useState('all');
      const [layerVisibility, setLayerVisibility] = useState({
        segments: true,
        fleet: true,
        stops: true,
        walkshed: false,
      });

      // Alerts & Branching
      const [alerts, setAlerts] = useState({ bottlenecks: [], bunching: [], timestamp: '' });
      const [branchOrigin, setBranchOrigin] = useState('Connaught Place');
      const [branchDest, setBranchDest] = useState('AIIMS');
      const [branchData, setBranchData] = useState(null);
      const [branchLoading, setBranchLoading] = useState(false);

      // Interactive States
      const [selectedStopData, setSelectedStopData] = useState(null);
      const [trackingBus, setTrackingBus] = useState(null);
      const [isSimulating, setIsSimulating] = useState(false);
      const [simProgress, setSimProgress] = useState(0);
      const [timeOffsetMinutes, setTimeOffsetMinutes] = useState(0);
      const [speechEnabled, setSpeechEnabled] = useState(false);
      const [isListening, setIsListening] = useState(false);
      const [showItinerary, setShowItinerary] = useState(true);
      const [showTransitPass, setShowTransitPass] = useState(false);
      const [refreshing, setRefreshing] = useState(false);
      const [toasts, setToasts] = useState([]);

      const addToast = (msg, icon = 'ℹ️') => {
        const id = Date.now() + Math.random();
        setToasts(prev => [...prev, { id, msg, icon }]);
        setTimeout(() => {
          setToasts(prev => prev.filter(t => t.id !== id));
        }, 3200);
      };

      const toggleTheme = () => {
        const newTheme = theme === 'dark' ? 'light' : 'dark';
        setTheme(newTheme);
        document.documentElement.setAttribute('data-theme', newTheme);
      };

      // Base Data Fetch
      const fetchBaseData = async () => {
        try {
          const [segRes, stopRes, predRes] = await Promise.all([
            fetch('/api/segments'),
            fetch('/api/stops'),
            fetch('/api/predictions'),
          ]);
          if (segRes.ok) setSegments(await segRes.json());
          if (stopRes.ok) setStops(await stopRes.json());
          if (predRes.ok) setPredictions(await predRes.json());
        } catch (err) {
          console.error('Base data error:', err);
        }
      };

      // Telemetry Polling
      const fetchLiveTelemetry = async () => {
        try {
          const [statusRes, fleetRes, alertsRes] = await Promise.all([
            fetch('/api/status'),
            fetch('/api/fleet?limit=550'),
            fetch('/api/alerts'),
          ]);
          if (statusRes.ok) setStatus(await statusRes.json());
          if (fleetRes.ok) setFleet(await fleetRes.json());
          if (alertsRes.ok) setAlerts(await alertsRes.json());
        } catch (err) {
          console.error('Telemetry poll error:', err);
        }
      };

      // Corridor Branches Fetch
      const fetchBranches = async (o = branchOrigin, d = branchDest) => {
        setBranchLoading(true);
        try {
          const res = await fetch(`/api/corridor-branches?origin=${encodeURIComponent(o)}&destination=${encodeURIComponent(d)}`);
          if (res.ok) {
            setBranchData(await res.json());
          }
        } catch (err) {
          console.error('Branching error:', err);
        } finally {
          setBranchLoading(false);
        }
      };

      // Stop Arrivals Fetch
      const fetchStopArrivals = async (stopId) => {
        try {
          const res = await fetch(`/api/stop-arrivals/${stopId}`);
          if (res.ok) {
            const data = await res.json();
            setSelectedStopData(data);
          }
        } catch (err) {
          console.error('Stop arrivals error:', err);
        }
      };

      // Plan Route
      const handlePlanRoute = async (sLat, sLon, eLat, eLon, sName = selectedSrc, dName = selectedDst) => {
        setClickPoints({ start: [sLat, sLon], end: [eLat, eLon] });
        setIsSimulating(false);
        setSimProgress(0);
        try {
          const res = await fetch('/api/route', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ start_lat: sLat, start_lon: sLon, end_lat: eLat, end_lon: eLon }),
          });
          if (res.ok) {
            const data = await res.json();
            setRoute(data);
            addToast(`Optimal route found: ~${data.eta_minutes} mins`, '⚡');
            if (speechEnabled) {
              speakText(`Route calculated: travel time is ${Math.round(data.eta_minutes)} minutes.`);
            }
          }
        } catch (err) {
          console.error('Routing failed:', err);
          addToast('Routing computation failed.', '⚠️');
        }
      };

      // Global Quick Locator Filter
      useEffect(() => {
        const q = quickSearch.trim().toLowerCase();
        if (!q) {
          setQuickSearchResults([]);
          setIsQuickOpen(false);
          return;
        }

        const matchStops = (stops || []).filter(s =>
          s.name.toLowerCase().includes(q) ||
          s.stop_id.toLowerCase().includes(q) ||
          (s.metro_lines || []).some(m => m.toLowerCase().includes(q))
        ).slice(0, 5).map(s => ({ type: 'stop', data: s, title: s.name, subtitle: `Stop ID: ${s.stop_id}`, metro: s.metro_lines }));

        const matchBuses = (fleet || []).filter(b =>
          b.bus_id.toLowerCase().includes(q) ||
          b.route_id.toLowerCase().includes(q)
        ).slice(0, 4).map(b => ({ type: 'bus', data: b, title: `Bus #${b.bus_id}`, subtitle: `Route ${b.route_id} • ${b.speed} km/h` }));

        const matchSegments = (segments || []).filter(seg =>
          seg.road_name.toLowerCase().includes(q)
        ).slice(0, 3).map(seg => ({ type: 'road', data: seg, title: seg.road_name, subtitle: `${seg.road_type} • ${seg.speed_kmh} km/h` }));

        setQuickSearchResults([...matchStops, ...matchBuses, ...matchSegments]);
        setIsQuickOpen(true);
      }, [quickSearch, stops, fleet, segments]);

      // Swap Origin and Destination
      const handleSwapLocations = () => {
        const temp = selectedSrc;
        setSelectedSrc(selectedDst);
        setSelectedDst(temp);
        const sObj = stops.find(s => s.name === selectedDst);
        const dObj = stops.find(s => s.name === temp);
        if (sObj && dObj) {
          handlePlanRoute(sObj.lat, sObj.lon, dObj.lat, dObj.lon, sObj.name, dObj.name);
        }
      };

      // Initial Mount & Handlers
      useEffect(() => {
        fetchBaseData();
        fetchLiveTelemetry();
        fetchBranches(branchOrigin, branchDest);

        const timer = setInterval(() => {
          fetchLiveTelemetry();
          fetchBranches(branchOrigin, branchDest);
        }, 16000);

        window.__setOrigin = (lat, lon, name) => {
          setSelectedSrc(name);
          setRoute(null);
          setClickPoints({ start: [lat, lon], end: null });
          addToast(`Origin: ${name}`, '🟢');
        };
        window.__setDest = (lat, lon, name) => {
          setSelectedDst(name);
          setClickPoints(prev => {
            const startPt = prev.start || [28.6315, 77.2167];
            handlePlanRoute(startPt[0], startPt[1], lat, lon, selectedSrc, name);
            return { start: startPt, end: [lat, lon] };
          });
        };
        window.__viewStopArrivals = (stopId) => {
          fetchStopArrivals(stopId);
        };
        window.__trackBus = (busId) => {
          setTrackingBus(busId);
          setActiveTab('map');
          addToast(`Tracking Bus #${busId}`, '🛰️');
        };

        return () => clearInterval(timer);
      }, []);

      const handleMapClick = (lat, lon) => {
        setClickPoints(prev => {
          if (!prev.start || (prev.start && prev.end)) {
            setRoute(null);
            setSelectedSrc(`Point (${lat.toFixed(4)}, ${lon.toFixed(4)})`);
            addToast('Origin set! Now click destination.', '🟢');
            return { start: [lat, lon], end: null };
          } else {
            setSelectedDst(`Point (${lat.toFixed(4)}, ${lon.toFixed(4)})`);
            handlePlanRoute(prev.start[0], prev.start[1], lat, lon);
            return { start: prev.start, end: [lat, lon] };
          }
        });
      };

      return (
        <div style={{ maxWidth: '1440px', margin: '0 auto', padding: '0 20px 40px 20px' }}>
          {/* Subtle Tricolor Line */}
          <div className="top-tricolor-bar" />

          {/* Header */}
          <header style={{ marginBottom: '16px' }}>
            <div className="glass-panel" style={{ padding: '16px 24px', marginTop: '10px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '14px' }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ fontSize: '1.6rem' }}>🚌</span>
                    <div>
                      <h1 style={{
                        fontSize: '1.45rem',
                        fontWeight: 800,
                        color: 'var(--text-main)',
                        letterSpacing: '-0.02em',
                      }}>
                        Delhi Transit Intelligence & Journey Planner
                      </h1>
                      <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', marginTop: '1px', fontWeight: 500 }}>
                        Real-Time Fleet Telemetry • Dynamic A* Congestion Routing • Speed Forecasting
                      </p>
                    </div>
                  </div>
                </div>

                {/* Header Controls */}
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
                  <div style={{
                    display: 'flex', alignItems: 'center', gap: '6px', padding: '5px 12px', borderRadius: '16px',
                    background: status.is_live ? 'rgba(16, 185, 129, 0.1)' : 'rgba(245, 158, 11, 0.1)',
                    border: `1px solid ${status.is_live ? 'rgba(16, 185, 129, 0.3)' : 'rgba(245, 158, 11, 0.3)'}`,
                    fontSize: '0.76rem', fontWeight: 700,
                    color: status.is_live ? '#10b981' : '#f59e0b'
                  }}>
                    <span className={status.is_live ? "pulse-dot-green" : "pulse-dot-orange"} />
                    {status.is_live ? "Live OTD Connected" : "Synthetic Baseline"}
                  </div>

                  <button
                    onClick={async () => {
                      setRefreshing(true);
                      try {
                        await fetch('/api/refresh', { method: 'POST' });
                        await fetchLiveTelemetry();
                        addToast('Telemetry synchronized', '🔄');
                      } finally { setRefreshing(false); }
                    }}
                    disabled={refreshing}
                    title="Poll Delhi Open Transit Data API"
                    style={{
                      background: 'var(--bg-elevated)', color: 'var(--text-main)',
                      border: '1px solid var(--border-subtle)', padding: '7px 12px', borderRadius: '8px',
                      fontWeight: 600, fontSize: '0.78rem', cursor: refreshing ? 'not-allowed' : 'pointer',
                      display: 'flex', alignItems: 'center', gap: '5px',
                    }}
                  >
                    <span>🔄</span>
                    {refreshing ? 'Syncing...' : 'Sync'}
                  </button>

                  <button
                    onClick={toggleTheme}
                    title="Toggle Dark / Light Theme"
                    style={{
                      background: 'var(--bg-elevated)', color: 'var(--text-main)',
                      border: '1px solid var(--border-subtle)', padding: '7px 11px',
                      borderRadius: '8px', fontWeight: 600, fontSize: '0.78rem', cursor: 'pointer',
                    }}
                  >
                    {theme === 'dark' ? '☀️ Light' : '🌙 Dark'}
                  </button>

                  {route && (
                    <button
                      onClick={() => setShowTransitPass(true)}
                      style={{
                        background: 'var(--primary-subtle)', color: 'var(--primary)',
                        border: '1px solid var(--border-accent)', padding: '7px 12px',
                        borderRadius: '8px', fontWeight: 700, fontSize: '0.78rem', cursor: 'pointer',
                      }}
                    >
                      🎫 Pass
                    </button>
                  )}
                </div>
              </div>

              {/* Sub-bar Status */}
              <div style={{
                display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                marginTop: '10px', paddingTop: '10px', borderTop: '1px solid var(--border-subtle)',
                fontSize: '0.78rem', color: 'var(--text-muted)', flexWrap: 'wrap', gap: '8px'
              }}>
                <div>Connected: <strong style={{ color: 'var(--text-main)' }}>{status.total_active_fleet?.toLocaleString() || '0'} buses</strong> across 113 road segments</div>
                <div>Last Sync: <strong style={{ color: 'var(--accent-cyan)' }}>{status.last_sync_time || 'Just now'}</strong></div>
              </div>
            </div>
          </header>

          {/* Quick Metrics (Subtle, Clean) */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '10px', marginBottom: '16px' }}>
            <div className="glass-panel" style={{ padding: '12px 16px' }}>
              <span style={{ fontSize: '0.68rem', fontWeight: 600, color: 'var(--text-dim)', letterSpacing: '0.04em' }}>FLEET IN SERVICE</span>
              <div style={{ fontSize: '1.45rem', fontWeight: 700, color: 'var(--text-main)', fontFamily: "'JetBrains Mono', monospace", marginTop: '2px' }}>
                {status.total_active_fleet?.toLocaleString() || '0'}
              </div>
            </div>

            <div className="glass-panel" style={{ padding: '12px 16px' }}>
              <span style={{ fontSize: '0.68rem', fontWeight: 600, color: 'var(--text-dim)', letterSpacing: '0.04em' }}>IN MOTION</span>
              <div style={{ fontSize: '1.45rem', fontWeight: 700, color: 'var(--accent-emerald)', fontFamily: "'JetBrains Mono', monospace", marginTop: '2px' }}>
                {status.moving_buses?.toLocaleString() || '0'}
              </div>
            </div>

            <div className="glass-panel" style={{ padding: '12px 16px' }}>
              <span style={{ fontSize: '0.68rem', fontWeight: 600, color: 'var(--text-dim)', letterSpacing: '0.04em' }}>IDLE / AT TERMINALS</span>
              <div style={{ fontSize: '1.45rem', fontWeight: 700, color: 'var(--accent-amber)', fontFamily: "'JetBrains Mono', monospace", marginTop: '2px' }}>
                {status.idle_buses?.toLocaleString() || '0'}
              </div>
            </div>

            <div className="glass-panel" style={{ padding: '12px 16px' }}>
              <span style={{ fontSize: '0.68rem', fontWeight: 600, color: 'var(--text-dim)', letterSpacing: '0.04em' }}>NETWORK SPEED</span>
              <div style={{ fontSize: '1.45rem', fontWeight: 700, color: 'var(--accent-cyan)', fontFamily: "'JetBrains Mono', monospace", marginTop: '2px' }}>
                {status.fleet_avg_speed_kmh || 0} km/h
              </div>
            </div>
          </div>

          {/* Global Quick Locator Bar (Makes it effortless to find any stop, bus or corridor) */}
          <div style={{ position: 'relative', marginBottom: '16px' }}>
            <div style={{ position: 'relative' }}>
              <span style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', fontSize: '1.1rem', pointerEvents: 'none' }}>
                🔍
              </span>
              <input
                type="text"
                placeholder="Locate any stop, metro interchange, route or bus (e.g. Connaught Place, AIIMS, Rohini, R01)..."
                value={quickSearch}
                onChange={e => setQuickSearch(e.target.value)}
                style={{
                  width: '100%',
                  background: 'var(--bg-card)',
                  color: 'var(--text-main)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '10px',
                  padding: '12px 16px 12px 42px',
                  fontSize: '0.88rem',
                  fontWeight: 600,
                  outline: 'none',
                  boxShadow: '0 2px 12px rgba(0, 0, 0, 0.15)',
                  transition: 'border-color 0.15s ease',
                }}
                onFocus={e => e.target.style.borderColor = 'var(--border-accent)'}
                onBlur={e => e.target.style.borderColor = 'var(--border-subtle)'}
              />
              {quickSearch && (
                <button
                  onClick={() => { setQuickSearch(''); setIsQuickOpen(false); }}
                  style={{
                    position: 'absolute', right: '14px', top: '50%', transform: 'translateY(-50%)',
                    background: 'transparent', border: 'none', color: 'var(--text-dim)', cursor: 'pointer', fontSize: '0.85rem'
                  }}
                >
                  ✕ Clear
                </button>
              )}
            </div>

            {/* Quick Search Dropdown Results */}
            {isQuickOpen && quickSearchResults.length > 0 && (
              <div style={{
                position: 'absolute', top: '100%', left: 0, right: 0, zIndex: 2000,
                background: 'var(--bg-card)', border: '1px solid var(--border-accent)',
                borderRadius: '10px', marginTop: '6px', maxHeight: '320px', overflowY: 'auto',
                boxShadow: '0 12px 36px rgba(0,0,0,0.6)', backdropFilter: 'blur(20px)'
              }}>
                <div style={{ padding: '6px 12px', fontSize: '0.7rem', fontWeight: 700, color: 'var(--text-dim)', borderBottom: '1px solid var(--border-subtle)' }}>
                  MATCHING LOCATIONS ({quickSearchResults.length})
                </div>
                {quickSearchResults.map((res, i) => (
                  <div
                    key={i}
                    onClick={() => {
                      if (res.type === 'stop') {
                        setSelectedDst(res.title);
                        const sObj = stops.find(s => s.name === selectedSrc);
                        if (sObj) handlePlanRoute(sObj.lat, sObj.lon, res.data.lat, res.data.lon, selectedSrc, res.title);
                        addToast(`Selected destination: ${res.title}`, '🚏');
                      } else if (res.type === 'bus') {
                        setTrackingBus(res.data.bus_id);
                        setActiveTab('map');
                        addToast(`Focusing on Bus #${res.data.bus_id}`, '🚌');
                      }
                      setIsQuickOpen(false);
                      setQuickSearch('');
                    }}
                    style={{
                      padding: '9px 14px', borderBottom: '1px solid var(--border-subtle)',
                      cursor: 'pointer', transition: 'background 0.15s ease',
                      display: 'flex', justifyContent: 'space-between', alignItems: 'center'
                    }}
                    onMouseEnter={e => e.currentTarget.style.background = 'var(--bg-card-hover)'}
                    onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
                  >
                    <div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                        <span>{res.type === 'stop' ? '🚏' : (res.type === 'bus' ? '🚌' : '🛣️')}</span>
                        <strong style={{ fontSize: '0.84rem', color: 'var(--text-main)' }}>{res.title}</strong>
                        {res.metro && res.metro.map((m, mIdx) => (
                          <span key={mIdx} className="metro-badge">🚇 {m}</span>
                        ))}
                      </div>
                      <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                        {res.subtitle}
                      </div>
                    </div>
                    <span style={{ fontSize: '0.74rem', color: 'var(--primary)', fontWeight: 700 }}>
                      {res.type === 'stop' ? 'Set Dest ➔' : 'Locate ➔'}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Active Route Summary Banner (Subtle & Informative) */}
          {route && (
            <div className="glass-panel" style={{ marginBottom: '16px', padding: '14px 20px', borderLeft: '4px solid var(--primary)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px' }}>
                <div>
                  <span style={{ fontSize: '0.7rem', fontWeight: 700, color: 'var(--primary)', letterSpacing: '0.04em', textTransform: 'uppercase' }}>
                    DYNAMIC ROUTE CALCULATED
                  </span>
                  <div style={{ fontSize: '0.92rem', color: 'var(--text-main)', fontWeight: 700 }}>
                    {selectedSrc} ➔ {selectedDst}
                  </div>
                </div>

                <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap', alignItems: 'center' }}>
                  <div><span style={{ fontSize: '0.68rem', color: 'var(--text-muted)' }}>DISTANCE</span><div style={{ fontSize: '1.05rem', fontWeight: 700 }}>{route.distance_km} km</div></div>
                  <div><span style={{ fontSize: '0.68rem', color: 'var(--text-muted)' }}>EST. TIME</span><div style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--accent-emerald)' }}>{route.eta_minutes} mins</div></div>
                  <div><span style={{ fontSize: '0.68rem', color: 'var(--text-muted)' }}>DTC FARE</span><div style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--accent-cyan)' }}>₹{route.fare_inr || 15}</div></div>
                  <div><span style={{ fontSize: '0.68rem', color: 'var(--text-muted)' }}>CO₂ SAVED</span><div style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--accent-emerald)' }}>{route.carbon_saved_kg || 0.8} kg</div></div>

                  <button
                    onClick={() => {
                      setIsSimulating(!isSimulating);
                      setActiveTab('map');
                    }}
                    style={{
                      background: isSimulating ? 'var(--accent-rose)' : 'var(--primary)',
                      color: '#fff', border: 'none', padding: '7px 14px', borderRadius: '7px', fontSize: '0.78rem',
                      fontWeight: 700, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '5px',
                    }}
                  >
                    {isSimulating ? '⏸ Pause Sim' : '▶ Simulate Journey'}
                  </button>

                  <button
                    onClick={() => setShowItinerary(!showItinerary)}
                    style={{
                      background: 'var(--bg-elevated)', border: '1px solid var(--border-subtle)',
                      color: 'var(--text-main)', padding: '7px 12px', borderRadius: '7px', fontSize: '0.78rem',
                      fontWeight: 600, cursor: 'pointer',
                    }}
                  >
                    {showItinerary ? '▲ Hide Steps' : `🧭 Steps (${route.itinerary ? route.itinerary.length : 0})`}
                  </button>
                </div>
              </div>

              {/* Collapsible Steps */}
              {showItinerary && route.itinerary && route.itinerary.length > 0 && (
                <div style={{ marginTop: '12px', paddingTop: '10px', borderTop: '1px solid var(--border-subtle)' }}>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '8px' }}>
                    {route.itinerary.map((step, idx) => (
                      <div key={idx} style={{
                        background: 'var(--bg-elevated)', border: '1px solid var(--border-subtle)',
                        borderRadius: '6px', padding: '8px 12px', display: 'flex', gap: '10px', alignItems: 'center'
                      }}>
                        <span style={{ fontSize: '1.1rem' }}>{step.icon || '🚌'}</span>
                        <div style={{ flex: 1 }}>
                          <div style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-main)' }}>{step.instruction}</div>
                          <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)', marginTop: '1px' }}>{step.meta}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Navigation Tabs (Subtle & Refined) */}
          <div style={{ display: 'flex', gap: '6px', marginBottom: '14px', flexWrap: 'wrap' }}>
            {[
              { id: 'map', label: '🗺️ Map & Simulator' },
              { id: 'fleet', label: `🚌 Fleet Explorer (${fleet.length})` },
              { id: 'ml', label: '🔮 Congestion Forecast' },
              { id: 'alerts', label: `🚨 Alerts (${(alerts.bottlenecks?.length || 0) + (alerts.bunching?.length || 0)})` },
              { id: 'branching', label: '🔀 Corridor Alternatives' },
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                style={{
                  background: activeTab === tab.id ? 'var(--primary-subtle)' : 'var(--bg-card)',
                  color: activeTab === tab.id ? 'var(--primary)' : 'var(--text-muted)',
                  border: `1px solid ${activeTab === tab.id ? 'var(--border-accent)' : 'var(--border-subtle)'}`,
                  padding: '8px 16px', borderRadius: '8px', fontWeight: 600, fontSize: '0.84rem',
                  cursor: 'pointer', transition: 'all 0.15s ease',
                }}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* TAB 1: INTERACTIVE MAP & ROUTE PLANNER */}
          {activeTab === 'map' && (
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 340px', gap: '16px', alignItems: 'start' }}>
              <LeafletMapContainer
                fleet={fleet}
                segments={segments}
                stops={stops}
                route={route}
                corridorFocus={corridorFocus}
                layerVisibility={layerVisibility}
                onMapClick={handleMapClick}
                clickPoints={clickPoints}
                trackingBus={trackingBus}
                onStopTracking={() => setTrackingBus(null)}
                isSimulating={isSimulating}
                simProgress={simProgress}
                setSimProgress={setSimProgress}
                timeOffsetMinutes={timeOffsetMinutes}
              />

              {/* Sidebar Controls (Clean, Top-First Hierarchy) */}
              <div className="glass-panel" style={{ padding: '16px', display: 'flex', flexDirection: 'column', gap: '14px' }}>

                {/* Primary Route Planner Card */}
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                    <h3 style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-main)', letterSpacing: '0.03em' }}>
                      📍 JOURNEY ROUTE PLANNER
                    </h3>
                    <button
                      onClick={handleSwapLocations}
                      title="Swap Origin & Destination"
                      style={{
                        background: 'transparent', border: '1px solid var(--border-subtle)', color: 'var(--primary)',
                        borderRadius: '6px', padding: '2px 7px', fontSize: '0.72rem', fontWeight: 700, cursor: 'pointer'
                      }}
                    >
                      ⇄ Swap
                    </button>
                  </div>

                  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    <StopAutocomplete
                      label="From (Origin)"
                      value={selectedSrc}
                      onChange={val => setSelectedSrc(val)}
                      stops={stops}
                      placeholder="Boarding stop..."
                      icon="🟢"
                    />

                    <StopAutocomplete
                      label="To (Destination)"
                      value={selectedDst}
                      onChange={val => setSelectedDst(val)}
                      stops={stops}
                      placeholder="Destination stop..."
                      icon="🔴"
                    />
                  </div>

                  <div style={{ display: 'flex', gap: '6px', marginTop: '10px' }}>
                    <button
                      onClick={() => {
                        const sObj = stops.find(s => s.name === selectedSrc);
                        const dObj = stops.find(s => s.name === selectedDst);
                        if (sObj && dObj) {
                          handlePlanRoute(sObj.lat, sObj.lon, dObj.lat, dObj.lon, sObj.name, dObj.name);
                        } else {
                          addToast('Please choose valid stops from list', '⚠️');
                        }
                      }}
                      style={{
                        flex: 1, background: 'var(--primary)',
                        color: '#fff', border: 'none', padding: '9px 12px', borderRadius: '7px',
                        fontWeight: 700, fontSize: '0.82rem', cursor: 'pointer',
                      }}
                    >
                      Find Fastest Route
                    </button>
                    <button
                      onClick={() => {
                        setRoute(null);
                        setClickPoints({ start: null, end: null });
                        setIsSimulating(false);
                      }}
                      style={{
                        background: 'var(--bg-elevated)', color: 'var(--text-muted)',
                        border: '1px solid var(--border-subtle)', padding: '9px 12px',
                        borderRadius: '7px', cursor: 'pointer', fontWeight: 600, fontSize: '0.78rem'
                      }}
                    >
                      Reset
                    </button>
                  </div>
                </div>

                <hr style={{ border: 'none', borderTop: '1px solid var(--border-subtle)' }} />

                {/* Popular Corridors Shortcuts */}
                <div>
                  <h4 style={{ fontSize: '0.74rem', fontWeight: 700, color: 'var(--text-dim)', marginBottom: '6px' }}>
                    POPULAR DELPHI CORRIDORS
                  </h4>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px' }}>
                    {[
                      { name: 'Rohini ➔ CP', src: 'Rohini Sec-3', dst: 'Connaught Place' },
                      { name: 'KG ➔ AIIMS', src: 'ISBT Kashmere Gate', dst: 'AIIMS' },
                      { name: 'Dwarka ➔ CP', src: 'Dwarka Sec-21', dst: 'Connaught Place' },
                      { name: 'Janakpuri ➔ ITO', src: 'Janakpuri', dst: 'ITO' },
                    ].map((p, idx) => (
                      <button
                        key={idx}
                        onClick={() => {
                          setSelectedSrc(p.src);
                          setSelectedDst(p.dst);
                          const sObj = stops.find(s => s.name === p.src);
                          const dObj = stops.find(s => s.name === p.dst);
                          if (sObj && dObj) handlePlanRoute(sObj.lat, sObj.lon, dObj.lat, dObj.lon, p.src, p.dst);
                        }}
                        style={{
                          background: 'var(--bg-elevated)', border: '1px solid var(--border-subtle)',
                          color: 'var(--text-main)', padding: '6px 8px', borderRadius: '6px',
                          fontSize: '0.74rem', fontWeight: 600, cursor: 'pointer', textAlign: 'left',
                        }}
                      >
                        {p.name}
                      </button>
                    ))}
                  </div>
                </div>

                <hr style={{ border: 'none', borderTop: '1px solid var(--border-subtle)' }} />

                {/* Region Focus Selector */}
                <div>
                  <label style={{ fontSize: '0.72rem', color: 'var(--text-dim)', fontWeight: 600, display: 'block', marginBottom: '4px' }}>
                    FOCUS REGION
                  </label>
                  <select
                    value={corridorFocus}
                    onChange={e => setCorridorFocus(e.target.value)}
                    style={{
                      width: '100%', background: 'var(--bg-elevated)', color: 'var(--text-main)',
                      border: '1px solid var(--border-subtle)', borderRadius: '6px', padding: '7px 10px',
                      fontSize: '0.78rem', fontWeight: 600, outline: 'none'
                    }}
                  >
                    <option value="all">🗺️ Entire Delhi NCT</option>
                    <option value="central">🏛️ Central (CP / Rajiv Chowk)</option>
                    <option value="north">🏰 North (ISBT / Kashmere Gate)</option>
                    <option value="south">🏥 South (AIIMS / Ring Road)</option>
                    <option value="east">🌉 East (Vikas Marg / Anand Vihar)</option>
                    <option value="west">✈️ West (Dwarka / Janakpuri)</option>
                  </select>
                </div>

                {/* Map Layers */}
                <div>
                  <label style={{ fontSize: '0.72rem', color: 'var(--text-dim)', fontWeight: 600, display: 'block', marginBottom: '4px' }}>
                    LAYERS
                  </label>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px', fontSize: '0.76rem' }}>
                    <label style={{ display: 'flex', alignItems: 'center', gap: '6px', cursor: 'pointer' }}>
                      <input type="checkbox" checked={layerVisibility.segments} onChange={() => setLayerVisibility(p => ({...p, segments: !p.segments}))} style={{ accentColor: '#f97316' }} />
                      Road Speeds
                    </label>
                    <label style={{ display: 'flex', alignItems: 'center', gap: '6px', cursor: 'pointer' }}>
                      <input type="checkbox" checked={layerVisibility.fleet} onChange={() => setLayerVisibility(p => ({...p, fleet: !p.fleet}))} style={{ accentColor: '#f97316' }} />
                      Live Fleet
                    </label>
                    <label style={{ display: 'flex', alignItems: 'center', gap: '6px', cursor: 'pointer' }}>
                      <input type="checkbox" checked={layerVisibility.stops} onChange={() => setLayerVisibility(p => ({...p, stops: !p.stops}))} style={{ accentColor: '#f97316' }} />
                      Bus Stops
                    </label>
                    <label style={{ display: 'flex', alignItems: 'center', gap: '6px', cursor: 'pointer' }}>
                      <input type="checkbox" checked={layerVisibility.walkshed} onChange={() => setLayerVisibility(p => ({...p, walkshed: !p.walkshed}))} style={{ accentColor: '#f97316' }} />
                      500m Access
                    </label>
                  </div>
                </div>

                {/* Stop Live Arrival Countdown Card (if opened) */}
                {selectedStopData && (
                  <div style={{
                    background: 'var(--bg-elevated)', border: '1px solid var(--border-subtle)',
                    borderRadius: '8px', padding: '10px 12px', marginTop: '4px'
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                      <div style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--accent-cyan)' }}>
                        🚏 {selectedStopData.stop_name}
                      </div>
                      <button
                        onClick={() => setSelectedStopData(null)}
                        style={{ background: 'transparent', border: 'none', color: 'var(--text-dim)', fontSize: '0.75rem', cursor: 'pointer' }}
                      >
                        ✕
                      </button>
                    </div>
                    <div style={{ fontSize: '0.68rem', color: 'var(--text-muted)', marginBottom: '6px' }}>
                      Live arrivals within 7.5 km:
                    </div>
                    {selectedStopData.arrivals && selectedStopData.arrivals.length > 0 ? (
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', maxHeight: '140px', overflowY: 'auto' }}>
                        {selectedStopData.arrivals.slice(0, 5).map((arr, i) => (
                          <div key={i} style={{
                            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                            background: 'var(--bg-card)', padding: '5px 8px', borderRadius: '5px', fontSize: '0.74rem'
                          }}>
                            <div>
                              <strong style={{ color: 'var(--text-main)' }}>R{arr.route_id}</strong>
                              <span style={{ fontSize: '0.68rem', color: 'var(--text-dim)', marginLeft: '4px' }}>#{arr.bus_id}</span>
                            </div>
                            <span style={{ fontWeight: 700, color: arr.eta_minutes <= 4 ? 'var(--accent-emerald)' : 'var(--accent-amber)' }}>
                              ~{arr.eta_minutes}m ({arr.distance_km}km)
                            </span>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div style={{ fontSize: '0.72rem', color: 'var(--accent-amber)' }}>
                        No incoming buses in radius.
                      </div>
                    )}
                  </div>
                )}

              </div>
            </div>
          )}

          {/* TAB 2: ACTIVE BUS FLEET EXPLORER */}
          {activeTab === 'fleet' && (
            <BusTableComponent
              fleet={fleet}
              onTrackBus={(bId) => {
                setTrackingBus(bId);
                setActiveTab('map');
                addToast(`Locating Bus #${bId}`, '🛰️');
              }}
            />
          )}

          {/* TAB 3: AI TRAFFIC FORECASTING */}
          {activeTab === 'ml' && (
            <PredictionsComponent
              predictions={predictions}
              timeOffsetMinutes={timeOffsetMinutes}
              setTimeOffsetMinutes={setTimeOffsetMinutes}
            />
          )}

          {/* TAB 4: TRANSIT ALERTS & BUNCHING */}
          {activeTab === 'alerts' && (
            <AlertsComponent alerts={alerts} />
          )}

          {/* TAB 5: MULTI-ROUTE CORRIDOR & BUS BRANCHING */}
          {activeTab === 'branching' && (
            <CorridorBranchingComponent
              stops={stops}
              origin={branchOrigin}
              destination={branchDest}
              setOrigin={setBranchOrigin}
              setDestination={setBranchDest}
              branchData={branchData}
              loading={branchLoading}
              onRefresh={() => fetchBranches(branchOrigin, branchDest)}
            />
          )}

          {/* Toast Notification Container */}
          <div className="toast-container">
            {toasts.map(t => (
              <div key={t.id} className="toast-item">
                <span>{t.icon}</span>
                <span>{t.msg}</span>
              </div>
            ))}
          </div>

          {/* Transit Pass Modal */}
          {showTransitPass && route && (
            <div style={{
              position: 'fixed', inset: 0, zIndex: 10000,
              background: 'rgba(0, 0, 0, 0.7)', backdropFilter: 'blur(6px)',
              display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '16px'
            }}>
              <div className="glass-panel" style={{ maxWidth: '440px', width: '100%', padding: '24px', position: 'relative' }}>
                <button
                  onClick={() => setShowTransitPass(false)}
                  style={{
                    position: 'absolute', top: '14px', right: '14px',
                    background: 'transparent', border: 'none', color: 'var(--text-dim)', fontSize: '1rem', cursor: 'pointer'
                  }}
                >
                  ✕
                </button>
                <div style={{ textAlign: 'center', borderBottom: '1px dashed var(--border-subtle)', paddingBottom: '12px', marginBottom: '14px' }}>
                  <div style={{ fontSize: '1.2rem' }}>🚌 🇮🇳</div>
                  <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--primary)', marginTop: '2px' }}>
                    DELHI TRANSPORT CORPORATION
                  </h3>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                    Digital Commuter Transit Boarding Pass
                  </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', fontSize: '0.8rem', marginBottom: '14px' }}>
                  <div><span style={{ fontSize: '0.68rem', color: 'var(--text-dim)' }}>FROM</span><div style={{ fontWeight: 700 }}>{selectedSrc}</div></div>
                  <div><span style={{ fontSize: '0.68rem', color: 'var(--text-dim)' }}>TO</span><div style={{ fontWeight: 700 }}>{selectedDst}</div></div>
                  <div><span style={{ fontSize: '0.68rem', color: 'var(--text-dim)' }}>DISTANCE</span><div style={{ fontWeight: 700 }}>{route.distance_km} km</div></div>
                  <div><span style={{ fontSize: '0.68rem', color: 'var(--text-dim)' }}>ETA</span><div style={{ fontWeight: 700, color: 'var(--accent-emerald)' }}>{route.eta_minutes} mins</div></div>
                  <div><span style={{ fontSize: '0.68rem', color: 'var(--text-dim)' }}>FARE</span><div style={{ fontWeight: 800, color: 'var(--accent-cyan)' }}>₹{route.fare_inr || 15}</div></div>
                  <div><span style={{ fontSize: '0.68rem', color: 'var(--text-dim)' }}>CO₂ SAVED</span><div style={{ fontWeight: 700, color: 'var(--accent-emerald)' }}>{route.carbon_saved_kg || 0.8} kg</div></div>
                </div>

                <div style={{ display: 'flex', gap: '8px' }}>
                  <button
                    onClick={() => window.print()}
                    style={{ flex: 1, background: 'var(--primary)', color: '#fff', border: 'none', padding: '9px', borderRadius: '6px', fontWeight: 700, fontSize: '0.8rem', cursor: 'pointer' }}
                  >
                    Print Pass
                  </button>
                  <button
                    onClick={() => setShowTransitPass(false)}
                    style={{ background: 'var(--bg-elevated)', color: 'var(--text-main)', border: '1px solid var(--border-subtle)', padding: '9px 14px', borderRadius: '6px', fontWeight: 600, fontSize: '0.8rem', cursor: 'pointer' }}
                  >
                    Close
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      );
    }

    // --- Enhanced Leaflet Map Component ---
    function LeafletMapContainer({
      fleet, segments, stops, route, corridorFocus, layerVisibility,
      onMapClick, clickPoints, trackingBus, onStopTracking,
      isSimulating, simProgress, setSimProgress, timeOffsetMinutes
    }) {
      const mapRef = useRef(null);
      const instanceRef = useRef(null);
      const roadGroup = useRef(null);
      const fleetGroup = useRef(null);
      const stopsGroup = useRef(null);
      const walkshedGroup = useRef(null);
      const routeGroup = useRef(null);
      const clickGroup = useRef(null);
      const simBusMarker = useRef(null);
      const [mapReady, setMapReady] = useState(false);

      const onMapClickRef = useRef(onMapClick);
      useEffect(() => {
        onMapClickRef.current = onMapClick;
      }, [onMapClick]);

      // Initialize map
      useEffect(() => {
        if (!mapRef.current || instanceRef.current) return;
        const map = L.map(mapRef.current, { center: [28.6139, 77.2090], zoom: 12, zoomControl: true });
        instanceRef.current = map;

        const dark = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
          maxZoom: 19,
          attribution: '&copy; CARTO & OpenStreetMap',
        }).addTo(map);

        const osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
          maxZoom: 19,
          attribution: '&copy; OpenStreetMap',
        });

        const light = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
          maxZoom: 19,
          attribution: '&copy; CARTO',
        });

        L.control.layers({
          '🌙 Dark Basemap': dark,
          '🗺️ OpenStreetMap': osm,
          '☀️ Light Basemap': light,
        }, null, { position: 'topright' }).addTo(map);

        roadGroup.current = L.layerGroup().addTo(map);
        fleetGroup.current = L.layerGroup().addTo(map);
        stopsGroup.current = L.layerGroup().addTo(map);
        walkshedGroup.current = L.layerGroup().addTo(map);
        routeGroup.current = L.layerGroup().addTo(map);
        clickGroup.current = L.layerGroup().addTo(map);

        map.on('click', e => {
          if (onMapClickRef.current) onMapClickRef.current(e.latlng.lat, e.latlng.lng);
        });

        setTimeout(() => { if (map) map.invalidateSize(); }, 200);
        setMapReady(true);

        return () => {
          map.remove();
          instanceRef.current = null;
          roadGroup.current = null;
          fleetGroup.current = null;
          stopsGroup.current = null;
          walkshedGroup.current = null;
          routeGroup.current = null;
          clickGroup.current = null;
          setMapReady(false);
        };
      }, []);

      // Focus Region Fly-to
      useEffect(() => {
        const map = instanceRef.current;
        if (!map) return;
        const coords = {
          'all': [[28.6139, 77.2090], 12],
          'central': [[28.6250, 77.2180], 13.5],
          'north': [[28.6672, 77.2284], 14],
          'south': [[28.5672, 77.2100], 13.5],
          'east': [[28.6364, 77.2956], 13.5],
          'west': [[28.5950, 77.0700], 13.5],
        };
        const t = coords[corridorFocus] || coords['all'];
        map.flyTo(t[0], t[1], { duration: 1.0 });
      }, [corridorFocus]);

      // Render Roads
      useEffect(() => {
        if (!mapReady || !roadGroup.current) return;
        roadGroup.current.clearLayers();
        if (!layerVisibility.segments || !segments) return;

        segments.forEach(seg => {
          const color = CONGESTION_COLORS[seg.congestion_level] || '#10b981';
          const p = L.polyline(seg.coordinates, { color, weight: 3.5, opacity: 0.85 });
          p.bindPopup(`
            <div style="font-family: inherit; padding: 2px;">
              <strong style="color: var(--primary); font-size: 12px;">🛣️ ${seg.road_name}</strong>
              <div style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">
                Speed: <b>${seg.speed_kmh} km/h</b> • Status: <b>${seg.congestion_level}</b>
              </div>
            </div>
          `);
          p.addTo(roadGroup.current);
        });
      }, [segments, layerVisibility.segments, mapReady]);

      // Render Fleet Markers
      useEffect(() => {
        if (!mapReady || !fleetGroup.current) return;
        fleetGroup.current.clearLayers();
        if (!layerVisibility.fleet || !fleet) return;

        fleet.slice(0, 450).forEach(bus => {
          const spd = bus.speed || 0;
          const isTarget = trackingBus === bus.bus_id;
          const color = isTarget ? '#38bdf8' : (spd >= 20 ? '#10b981' : (spd >= 5 ? '#f59e0b' : '#f43f5e'));

          const busHtml = `
            <div style="transform: translate(-50%, -50%); display: flex; align-items: center; justify-content: center; cursor: pointer;">
              <div style="
                width: ${isTarget ? '18px' : '12px'}; height: ${isTarget ? '18px' : '12px'};
                border-radius: 50%; background: ${color}; border: 2px solid #ffffff;
                box-shadow: 0 0 ${isTarget ? '10px #38bdf8' : '4px ' + color};
              "></div>
            </div>`;

          const m = L.marker([bus.lat, bus.lon], {
            icon: L.divIcon({ className: 'bus-marker-div', html: busHtml, iconSize: [0, 0] }),
            zIndexOffset: isTarget ? 3000 : 500
          });

          m.bindPopup(`
            <div style="font-family: inherit; min-width: 150px; padding: 2px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
                <strong style="color: var(--primary); font-size: 12px;">🚌 #${bus.bus_id}</strong>
                <span style="font-size: 10px; background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 1px 5px; border-radius: 4px; font-weight: 700;">
                  Route ${bus.route_id}
                </span>
              </div>
              <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 6px;">
                Speed: <b>${spd.toFixed(1)} km/h</b>
              </div>
              <button
                onclick="window.__trackBus('${bus.bus_id}')"
                style="width: 100%; background: var(--primary); color: #fff; border: none; padding: 5px; border-radius: 5px; font-size: 10px; font-weight: 700; cursor: pointer;"
              >
                🛰️ Track & Follow
              </button>
            </div>
          `);

          m.addTo(fleetGroup.current);

          if (isTarget && instanceRef.current) {
            instanceRef.current.panTo([bus.lat, bus.lon], { animate: true, duration: 0.8 });
          }
        });
      }, [fleet, layerVisibility.fleet, trackingBus, mapReady]);

      // Render Bus Stops
      useEffect(() => {
        if (!mapReady || !stopsGroup.current || !walkshedGroup.current) return;
        stopsGroup.current.clearLayers();
        walkshedGroup.current.clearLayers();
        if (!stops) return;

        if (layerVisibility.stops) {
          stops.forEach(s => {
            const stopHtml = `
              <div style="transform: translate(-50%, -50%); cursor: pointer;">
                <div style="width: 11px; height: 11px; border-radius: 50%; background: #0284c7; border: 1.5px solid #ffffff;"></div>
              </div>`;

            const m = L.marker([s.lat, s.lon], {
              icon: L.divIcon({ className: 'stop-pin', html: stopHtml, iconSize: [0, 0] })
            });

            const metroList = (s.metro_lines || []).map(m => `<span class="metro-badge" style="font-size: 9px; margin: 1px 2px;">🚇 ${m}</span>`).join('');

            const popupContent = `
              <div style="font-family: inherit; min-width: 170px; padding: 2px;">
                <div style="font-weight: 700; color: #38bdf8; font-size: 12px; margin-bottom: 2px;">🚏 ${s.name}</div>
                <div style="font-size: 10px; color: var(--text-dim); margin-bottom: 4px;">ID: ${s.stop_id}</div>
                ${metroList ? `<div style="margin-bottom: 6px; display: flex; flex-wrap: wrap;">${metroList}</div>` : ''}
                <div style="display: flex; gap: 4px; margin-top: 6px;">
                  <button onclick="window.__setOrigin(${s.lat}, ${s.lon}, '${s.name.replace(/'/g, "\\'")}')" style="flex: 1; background: #10b981; color: #fff; border: none; padding: 4px 6px; border-radius: 4px; font-size: 10px; font-weight: 700; cursor: pointer;">🟢 Origin</button>
                  <button onclick="window.__setDest(${s.lat}, ${s.lon}, '${s.name.replace(/'/g, "\\'")}')" style="flex: 1; background: #f43f5e; color: #fff; border: none; padding: 4px 6px; border-radius: 4px; font-size: 10px; font-weight: 700; cursor: pointer;">🔴 Dest</button>
                </div>
                <button onclick="window.__viewStopArrivals('${s.stop_id}')" style="width: 100%; margin-top: 4px; background: var(--bg-elevated); color: var(--text-main); border: 1px solid var(--border-subtle); padding: 5px; border-radius: 4px; font-size: 10px; font-weight: 600; cursor: pointer;">⏱️ Live Arrivals</button>
              </div>
            `;
            m.bindPopup(popupContent);
            m.addTo(stopsGroup.current);
          });
        }

        if (layerVisibility.walkshed) {
          stops.forEach(s => {
            L.circle([s.lat, s.lon], {
              radius: 500,
              color: '#0ea5e9',
              fillColor: '#0ea5e9',
              fillOpacity: 0.05,
              weight: 1,
              dashArray: '3 3',
            }).addTo(walkshedGroup.current);
          });
        }
      }, [stops, layerVisibility.stops, layerVisibility.walkshed, mapReady]);

      // Render Planned Route
      useEffect(() => {
        if (!mapReady || !routeGroup.current) return;
        routeGroup.current.clearLayers();

        if (route && route.geojson) {
          const l = L.geoJSON(route.geojson, {
            style: { color: '#38bdf8', weight: 5, opacity: 0.9, dashArray: '6 4' }
          }).addTo(routeGroup.current);

          if (instanceRef.current && l.getBounds().isValid()) {
            instanceRef.current.fitBounds(l.getBounds(), { padding: [40, 40] });
          }
        }
      }, [route, mapReady]);

      // Origin & Destination Pins
      useEffect(() => {
        if (!mapReady || !clickGroup.current) return;
        clickGroup.current.clearLayers();

        if (clickPoints.start) {
          const oHtml = `
            <div style="transform: translate(-50%, -100%); display: flex; flex-direction: column; align-items: center;">
              <div style="background: #10b981; color: #ffffff; padding: 3px 8px; border-radius: 12px; font-weight: 700; font-size: 10px; border: 1.5px solid #fff; white-space: nowrap;">
                🟢 Origin
              </div>
              <div style="width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent; border-top: 6px solid #10b981;"></div>
            </div>`;
          L.marker(clickPoints.start, { icon: L.divIcon({ className: 'o-pin', html: oHtml, iconSize: [0, 0] }), zIndexOffset: 2000 })
            .addTo(clickGroup.current);
        }

        if (clickPoints.end) {
          const dHtml = `
            <div style="transform: translate(-50%, -100%); display: flex; flex-direction: column; align-items: center;">
              <div style="background: #f43f5e; color: #ffffff; padding: 3px 8px; border-radius: 12px; font-weight: 700; font-size: 10px; border: 1.5px solid #fff; white-space: nowrap;">
                🔴 Destination
              </div>
              <div style="width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent; border-top: 6px solid #f43f5e;"></div>
            </div>`;
          L.marker(clickPoints.end, { icon: L.divIcon({ className: 'd-pin', html: dHtml, iconSize: [0, 0] }), zIndexOffset: 2000 })
            .addTo(clickGroup.current);
        }
      }, [clickPoints, mapReady]);

      // Simulation Animation
      useEffect(() => {
        if (!isSimulating || !route || !route.route_latlngs || route.route_latlngs.length < 2) {
          if (simBusMarker.current && routeGroup.current) {
            routeGroup.current.removeLayer(simBusMarker.current);
            simBusMarker.current = null;
          }
          return;
        }

        const interval = setInterval(() => {
          setSimProgress(prev => {
            const next = prev + 0.5;
            if (next >= 100) {
              clearInterval(interval);
              return 100;
            }
            return next;
          });
        }, 100);

        return () => clearInterval(interval);
      }, [isSimulating, route]);

      useEffect(() => {
        if (!route || !route.route_latlngs || route.route_latlngs.length < 2 || !routeGroup.current) return;
        const waypoints = route.route_latlngs;
        const total = waypoints.length;
        const floatIndex = (simProgress / 100) * (total - 1);
        const idx1 = Math.floor(floatIndex);
        const idx2 = Math.min(idx1 + 1, total - 1);
        const frac = floatIndex - idx1;

        const p1 = waypoints[idx1];
        const p2 = waypoints[idx2];
        const curLat = p1[0] + (p2[0] - p1[0]) * frac;
        const curLon = p1[1] + (p2[1] - p1[1]) * frac;

        const simHtml = `
          <div style="transform: translate(-50%, -50%); display: flex; flex-direction: column; align-items: center; pointer-events: none;">
            <div style="background: var(--primary); color: #fff; padding: 2px 7px; border-radius: 10px; font-weight: 700; font-size: 10px; border: 1.5px solid #fff; white-space: nowrap;">
              🚌 Simulating
            </div>
          </div>`;

        if (!simBusMarker.current) {
          simBusMarker.current = L.marker([curLat, curLon], {
            icon: L.divIcon({ className: 'sim-bus-marker', html: simHtml, iconSize: [0, 0] }),
            zIndexOffset: 4000
          }).addTo(routeGroup.current);
        } else {
          simBusMarker.current.setLatLng([curLat, curLon]);
        }
      }, [simProgress, route]);

      // Re-center handler
      const handleCenterMap = () => {
        if (instanceRef.current) {
          instanceRef.current.flyTo([28.6139, 77.2090], 12, { duration: 0.8 });
        }
      };

      return (
        <div style={{ position: 'relative', width: '100%', height: '580px', borderRadius: '12px', overflow: 'hidden' }}>
          <div ref={mapRef} style={{ width: '100%', height: '100%' }} />

          {/* Quick Center Button */}
          <button
            onClick={handleCenterMap}
            title="Center on Delhi NCT"
            style={{
              position: 'absolute', top: '12px', left: '12px', zIndex: 900,
              background: 'var(--bg-card)', border: '1px solid var(--border-subtle)',
              borderRadius: '8px', padding: '6px 10px', fontSize: '0.74rem', fontWeight: 600,
              color: 'var(--text-main)', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '5px',
              boxShadow: '0 2px 8px rgba(0,0,0,0.3)', backdropFilter: 'blur(10px)'
            }}
          >
            <span>🎯</span> Center Delhi
          </button>

          {/* Tracking Bus Floating HUD */}
          {trackingBus && (
            <div style={{
              position: 'absolute', top: '12px', left: '120px', zIndex: 900,
            }}>
              <div className="hud-card" style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '6px 12px' }}>
                <span className="pulse-dot-cyan" />
                <span style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--accent-cyan)' }}>
                  Tracking #{trackingBus}
                </span>
                <button
                  onClick={onStopTracking}
                  style={{
                    background: 'transparent', border: 'none', color: 'var(--text-dim)',
                    cursor: 'pointer', fontSize: '0.76rem', fontWeight: 700
                  }}
                >
                  ✕
                </button>
              </div>
            </div>
          )}

          {/* Simulation Progress Floating Bar */}
          {isSimulating && route && (
            <div style={{
              position: 'absolute', bottom: '16px', left: '16px', right: '16px', zIndex: 900,
            }}>
              <div className="hud-card" style={{ padding: '8px 14px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.74rem', marginBottom: '4px' }}>
                  <span style={{ fontWeight: 700, color: 'var(--accent-emerald)' }}>Simulating ({Math.round(simProgress)}%)</span>
                  <span style={{ color: 'var(--text-muted)' }}>{route.effective_speed_kmh} km/h</span>
                </div>
                <div style={{ width: '100%', height: '4px', background: 'var(--bg-elevated)', borderRadius: '2px', overflow: 'hidden' }}>
                  <div style={{ width: `${simProgress}%`, height: '100%', background: 'var(--primary)' }} />
                </div>
              </div>
            </div>
          )}
        </div>
      );
    }

    // --- Fleet Explorer Table Component ---
    function BusTableComponent({ fleet, onTrackBus }) {
      const [search, setSearch] = useState('');
      const [statusFilter, setStatusFilter] = useState('ALL');

      const filtered = useMemo(() => {
        let list = fleet || [];
        if (search.trim()) {
          const q = search.trim().toLowerCase();
          list = list.filter(b => b.bus_id.toLowerCase().includes(q) || b.route_id.toLowerCase().includes(q));
        }
        if (statusFilter === 'FAST') list = list.filter(b => b.speed >= 20);
        else if (statusFilter === 'MODERATE') list = list.filter(b => b.speed >= 5 && b.speed < 20);
        else if (statusFilter === 'SLOW') list = list.filter(b => b.speed < 5);
        return list;
      }, [fleet, search, statusFilter]);

      return (
        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px', marginBottom: '14px' }}>
            <div>
              <h2 style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--text-main)' }}>
                🚌 Active Bus Fleet Explorer
              </h2>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                Real-time position and velocity telemetry for Delhi transit fleet
              </div>
            </div>

            <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', alignItems: 'center' }}>
              <input
                type="text"
                placeholder="Search bus or route..."
                value={search}
                onChange={e => setSearch(e.target.value)}
                style={{
                  background: 'var(--bg-elevated)', color: 'var(--text-main)',
                  border: '1px solid var(--border-subtle)', borderRadius: '6px',
                  padding: '6px 10px', fontSize: '0.78rem', outline: 'none'
                }}
              />

              <div style={{ display: 'flex', background: 'var(--bg-elevated)', borderRadius: '6px', padding: '2px', border: '1px solid var(--border-subtle)' }}>
                {[
                  { id: 'ALL', label: 'All' },
                  { id: 'FAST', label: '🟢 Fast' },
                  { id: 'MODERATE', label: '🟡 Mod' },
                  { id: 'SLOW', label: '🔴 Slow' },
                ].map(f => (
                  <button
                    key={f.id}
                    onClick={() => setStatusFilter(f.id)}
                    style={{
                      background: statusFilter === f.id ? 'var(--primary)' : 'transparent',
                      color: statusFilter === f.id ? '#fff' : 'var(--text-muted)',
                      border: 'none', padding: '4px 8px', borderRadius: '4px', fontSize: '0.72rem',
                      fontWeight: 600, cursor: 'pointer'
                    }}
                  >
                    {f.label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div style={{ overflowX: 'auto', maxHeight: '520px', border: '1px solid var(--border-subtle)', borderRadius: '8px' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.8rem' }}>
              <thead style={{ background: 'var(--bg-elevated)', position: 'sticky', top: 0 }}>
                <tr>
                  <th style={{ padding: '8px 12px', color: 'var(--text-muted)' }}>Bus Unit</th>
                  <th style={{ padding: '8px 12px', color: 'var(--text-muted)' }}>Route</th>
                  <th style={{ padding: '8px 12px', color: 'var(--text-muted)' }}>Speed</th>
                  <th style={{ padding: '8px 12px', color: 'var(--text-muted)' }}>GPS</th>
                  <th style={{ padding: '8px 12px', color: 'var(--text-muted)' }}>Status</th>
                  <th style={{ padding: '8px 12px', color: 'var(--text-muted)', textAlign: 'center' }}>Action</th>
                </tr>
              </thead>
              <tbody>
                {filtered.slice(0, 100).map((b, idx) => {
                  const spd = b.speed || 0;
                  const c = spd >= 20 ? 'var(--accent-emerald)' : (spd >= 5 ? 'var(--accent-amber)' : 'var(--accent-rose)');
                  return (
                    <tr key={b.bus_id + idx} style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                      <td style={{ padding: '8px 12px', fontWeight: 700, fontFamily: "'JetBrains Mono', monospace" }}>
                        #{b.bus_id}
                      </td>
                      <td style={{ padding: '8px 12px', color: 'var(--accent-cyan)', fontWeight: 600 }}>
                        {b.route_id}
                      </td>
                      <td style={{ padding: '8px 12px', fontWeight: 700, color: c }}>
                        {spd.toFixed(1)} km/h
                      </td>
                      <td style={{ padding: '8px 12px', color: 'var(--text-dim)', fontFamily: "'JetBrains Mono', monospace", fontSize: '0.74rem' }}>
                        {b.lat.toFixed(4)}, {b.lon.toFixed(4)}
                      </td>
                      <td style={{ padding: '8px 12px' }}>
                        <span style={{ fontSize: '0.72rem', padding: '2px 6px', borderRadius: '8px', background: `${c}15`, color: c, fontWeight: 600 }}>
                          {b.status}
                        </span>
                      </td>
                      <td style={{ padding: '8px 12px', textAlign: 'center' }}>
                        <button
                          onClick={() => onTrackBus(b.bus_id)}
                          style={{
                            background: 'var(--bg-elevated)', border: '1px solid var(--border-subtle)',
                            color: 'var(--primary)', padding: '3px 8px', borderRadius: '4px',
                            fontSize: '0.72rem', fontWeight: 700, cursor: 'pointer'
                          }}
                        >
                          📍 Track
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      );
    }

    // --- Predictions Component ---
    function PredictionsComponent({ predictions }) {
      return (
        <div className="glass-panel" style={{ padding: '20px' }}>
          <h2 style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--text-main)', marginBottom: '4px' }}>
            🔮 Congestion & Velocity Forecasting
          </h2>
          <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '14px' }}>
            Machine learning predictions for major Delhi road corridors (+30m / +60m)
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '10px' }}>
            {(predictions || []).map((p, idx) => (
              <div key={idx} className="glass-panel" style={{ padding: '12px', border: '1px solid var(--border-subtle)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                  <strong style={{ fontSize: '0.86rem', color: 'var(--text-main)' }}>{p.road_name}</strong>
                  <span style={{ fontSize: '0.68rem', color: 'var(--text-dim)' }}>{p.road_type}</span>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '6px', textAlign: 'center', margin: '8px 0' }}>
                  <div><span style={{ fontSize: '0.66rem', color: 'var(--text-dim)' }}>NOW</span><div style={{ fontWeight: 700 }}>{p.current_speed_kmh} <span style={{ fontSize: '0.66rem' }}>km/h</span></div></div>
                  <div><span style={{ fontSize: '0.66rem', color: 'var(--text-dim)' }}>+30m</span><div style={{ fontWeight: 700, color: 'var(--accent-cyan)' }}>{p.forecast_30m_kmh} <span style={{ fontSize: '0.66rem' }}>km/h</span></div></div>
                  <div><span style={{ fontSize: '0.66rem', color: 'var(--text-dim)' }}>+60m</span><div style={{ fontWeight: 700, color: 'var(--accent-amber)' }}>{p.forecast_60m_kmh} <span style={{ fontSize: '0.66rem' }}>km/h</span></div></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      );
    }

    // --- Alerts Component ---
    function AlertsComponent({ alerts }) {
      const bnecks = alerts.bottlenecks || [];
      const bunch = alerts.bunching || [];

      return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          <div className="glass-panel" style={{ padding: '20px' }}>
            <h2 style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--accent-rose)', marginBottom: '4px' }}>
              🚨 Active Bottlenecks ({bnecks.length})
            </h2>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '10px', marginTop: '10px' }}>
              {bnecks.map((b, idx) => (
                <div key={idx} style={{ background: 'var(--bg-elevated)', border: '1px solid var(--border-subtle)', borderRadius: '8px', padding: '10px 12px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <strong style={{ fontSize: '0.84rem' }}>{b.road_name}</strong>
                    <span style={{ fontSize: '0.7rem', color: 'var(--accent-rose)', fontWeight: 700 }}>{b.severity}</span>
                  </div>
                  <div style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--accent-rose)', margin: '4px 0' }}>{b.speed_kmh} km/h</div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>Delay factor: ~{b.delay_factor}x</div>
                </div>
              ))}
            </div>
          </div>

          <div className="glass-panel" style={{ padding: '20px' }}>
            <h2 style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--primary)', marginBottom: '4px' }}>
              🚌 Fleet Bunching ({bunch.length})
            </h2>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '10px', marginTop: '10px' }}>
              {bunch.map((b, idx) => (
                <div key={idx} style={{ background: 'var(--bg-elevated)', border: '1px solid var(--border-subtle)', borderRadius: '8px', padding: '10px 12px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <strong style={{ fontSize: '0.84rem' }}>Route {b.route_id}</strong>
                    <span style={{ fontSize: '0.7rem', color: 'var(--accent-amber)', fontWeight: 700 }}>Gap: {b.gap_meters}m</span>
                  </div>
                  <div style={{ fontSize: '0.76rem', color: 'var(--text-muted)', margin: '4px 0' }}>Buses #{b.bus_1} and #{b.bus_2} clumped</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      );
    }

    // --- Corridor Branching Component ---
    function CorridorBranchingComponent({ stops, origin, destination, setOrigin, setDestination, branchData, loading, onRefresh }) {
      const branches = branchData?.branches || [];

      return (
        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px', marginBottom: '16px' }}>
            <div>
              <h2 style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--text-main)' }}>
                🔀 Corridor Alternatives & Bus Branching
              </h2>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                Compare parallel corridors between two points
              </div>
            </div>
            <button
              onClick={onRefresh}
              disabled={loading}
              style={{ background: 'var(--primary)', color: '#fff', border: 'none', padding: '6px 12px', borderRadius: '6px', fontSize: '0.78rem', fontWeight: 700, cursor: 'pointer' }}
            >
              {loading ? 'Analyzing...' : 'Re-Analyze'}
            </button>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginBottom: '14px' }}>
            <StopAutocomplete label="Point A" value={origin} onChange={setOrigin} stops={stops} placeholder="Origin..." icon="🟢" />
            <StopAutocomplete label="Point B" value={destination} onChange={setDestination} stops={stops} placeholder="Destination..." icon="🔴" />
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {branches.map(b => (
              <div key={b.branch_id} style={{ background: 'var(--bg-elevated)', border: '1px solid var(--border-subtle)', borderRadius: '8px', padding: '12px 14px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '8px' }}>
                  <div>
                    <strong style={{ fontSize: '0.88rem' }}>{b.name}</strong>
                    <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: '2px' }}>Via: {b.via} • Routes: {b.routes ? b.routes.join(', ') : 'DTC'}</div>
                  </div>
                  <div style={{ display: 'flex', gap: '14px', fontSize: '0.78rem' }}>
                    <div><span style={{ color: 'var(--text-dim)' }}>Buses:</span> <b>{b.total_active_buses}</b></div>
                    <div><span style={{ color: 'var(--text-dim)' }}>Next:</span> <b style={{ color: 'var(--accent-emerald)' }}>~{b.next_bus_eta_mins}m</b></div>
                    <div><span style={{ color: 'var(--text-dim)' }}>Speed:</span> <b>{b.corridor_speed_kmh} km/h</b></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);
  </script>
</body>
</html>
'''

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("Subtle and easy-to-locate static/index.html written successfully! Size:", len(html_code))
