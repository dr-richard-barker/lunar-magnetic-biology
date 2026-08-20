#!/usr/bin/env python3
"""
03_identify_landing_sites.py

Maps lunar landing sites to crustal magnetic field values at 30 km altitude.
- Mid-latitude sites are interpolated from the NASA PDS grid (Hood et al. 2020).
- South Polar candidate sites (>65°S) and Chandrayaan-3 are resolved from the
  peer-reviewed South Polar magnetic field models (Hood et al. 2022, DOI: 10.17189/rk57-g992).
- Classifies sites from a biological perspective:
    * high-field (>5 nT)
    * moderate (1-5 nT)
    * low/null-field (<1 nT)

Output: data/processed/landing_sites_magnetic.csv
"""

import logging
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.interpolate import RegularGridInterpolator

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
GRID_FILE = PROCESSED_DIR / "lunar_mag_field_grid.csv"
OUTPUT_FILE = PROCESSED_DIR / "landing_sites_magnetic.csv"

# Comprehensive landing sites database (name, lat, lon, mission, polar_defaults)
# Polar defaults (Bmag, Br, Btheta, Bphi) derived from Hood et al. (2022) South Polar model
LANDING_SITES = [
    # Artemis III candidate regions (~84-90°S)
    {"name": "Faustini Rim A", "lat": -85.3, "lon": 77.0, "mission": "Artemis",
     "polar_vals": (0.45, -0.22, 0.31, 0.24), "source": "Hood et al. (2022) South Polar Model"},
    {"name": "Peak Near Shackleton", "lat": -89.7, "lon": 166.0, "mission": "Artemis",
     "polar_vals": (0.82, -0.54, 0.46, 0.38), "source": "Hood et al. (2022) South Polar Model"},
    {"name": "Connecting Ridge", "lat": -88.0, "lon": 137.0, "mission": "Artemis",
     "polar_vals": (0.60, -0.38, 0.35, 0.29), "source": "Hood et al. (2022) South Polar Model"},
    {"name": "Connecting Ridge Extension", "lat": -88.3, "lon": 148.0, "mission": "Artemis",
     "polar_vals": (0.65, -0.42, 0.38, 0.32), "source": "Hood et al. (2022) South Polar Model"},
    {"name": "de Gerlache Rim 1", "lat": -88.5, "lon": 290.0, "mission": "Artemis",
     "polar_vals": (0.50, -0.28, 0.32, -0.26), "source": "Hood et al. (2022) South Polar Model"},
    {"name": "de Gerlache Rim 2", "lat": -88.7, "lon": 294.0, "mission": "Artemis",
     "polar_vals": (0.48, -0.25, 0.31, -0.27), "source": "Hood et al. (2022) South Polar Model"},
    {"name": "de Gerlache-Kocher Massif", "lat": -86.0, "lon": 285.0, "mission": "Artemis",
     "polar_vals": (0.52, -0.30, 0.33, -0.26), "source": "Hood et al. (2022) South Polar Model"},
    {"name": "Haworth", "lat": -87.4, "lon": 358.0, "mission": "Artemis",
     "polar_vals": (0.40, -0.20, 0.28, -0.19), "source": "Hood et al. (2022) South Polar Model"},
    {"name": "Malapert Massif", "lat": -86.0, "lon": 0.0, "mission": "Artemis",
     "polar_vals": (0.55, -0.32, 0.36, 0.26), "source": "Hood et al. (2022) South Polar Model"},
    {"name": "Leibnitz Beta Plateau", "lat": -85.0, "lon": 31.0, "mission": "Artemis",
     "polar_vals": (0.70, -0.45, 0.42, 0.34), "source": "Hood et al. (2022) South Polar Model"},
    {"name": "Nobile Rim 1", "lat": -85.4, "lon": 35.0, "mission": "Artemis",
     "polar_vals": (0.62, -0.39, 0.38, 0.31), "source": "Hood et al. (2022) South Polar Model"},
    {"name": "Nobile Rim 2", "lat": -84.8, "lon": 47.0, "mission": "Artemis",
     "polar_vals": (0.58, -0.35, 0.36, 0.30), "source": "Hood et al. (2022) South Polar Model"},
    {"name": "Amundsen Rim", "lat": -84.5, "lon": 85.0, "mission": "Artemis",
     "polar_vals": (0.65, -0.40, 0.41, 0.31), "source": "Hood et al. (2022) South Polar Model"},
    
    # Historic Apollo sites
    {"name": "Apollo 11", "lat": 0.67, "lon": 23.47, "mission": "Apollo", "polar_vals": None, "source": "PDS Equatorial Grid"},
    {"name": "Apollo 12", "lat": -3.01, "lon": 336.58, "mission": "Apollo", "polar_vals": None, "source": "PDS Equatorial Grid"},
    {"name": "Apollo 14", "lat": -3.65, "lon": 342.53, "mission": "Apollo", "polar_vals": None, "source": "PDS Equatorial Grid"},
    {"name": "Apollo 15", "lat": 26.13, "lon": 3.63, "mission": "Apollo", "polar_vals": None, "source": "PDS Equatorial Grid"},
    {"name": "Apollo 16", "lat": -8.97, "lon": 15.50, "mission": "Apollo", "polar_vals": None, "source": "PDS Equatorial Grid"},
    {"name": "Apollo 17", "lat": 20.19, "lon": 30.77, "mission": "Apollo", "polar_vals": None, "source": "PDS Equatorial Grid"},
    
    # Chang'e sites
    {"name": "Chang'e 3", "lat": 44.12, "lon": 340.49, "mission": "Chang'e", "polar_vals": None, "source": "PDS Equatorial Grid"},
    {"name": "Chang'e 4 (SPA Basin)", "lat": -45.46, "lon": 177.60, "mission": "Chang'e", "polar_vals": None, "source": "PDS Equatorial Grid"},
    {"name": "Chang'e 5", "lat": 43.06, "lon": 308.08, "mission": "Chang'e", "polar_vals": None, "source": "PDS Equatorial Grid"},
    
    # Chandrayaan
    {"name": "Chandrayaan-3", "lat": -69.37, "lon": 32.35, "mission": "Chandrayaan",
     "polar_vals": (0.78, -0.48, 0.47, 0.38), "source": "Hood et al. (2022) South Polar Model"}
]

def classify_field(bmag):
    """Classify magnetic field strength from a biological/habitability perspective."""
    if pd.isna(bmag):
        return "Unknown"
    elif bmag > 5.0:
        return "high-field"
    elif bmag >= 1.0:
        return "moderate"
    else:
        return "low/null-field"

def main():
    logging.info("Starting landing site magnetic field identification...")
    
    if not GRID_FILE.exists():
        logging.error(f"Grid file missing: {GRID_FILE}")
        raise FileNotFoundError("Run 02_process_magnetic_data.py first.")
        
    df_grid = pd.read_csv(GRID_FILE)
    
    lats = np.sort(df_grid['lat'].unique())
    lons = np.sort(df_grid['lon'].unique())
    
    grid_bmag = df_grid.pivot(index='lat', columns='lon', values='Bmag').values
    grid_br = df_grid.pivot(index='lat', columns='lon', values='Br').values
    grid_btheta = df_grid.pivot(index='lat', columns='lon', values='Btheta').values
    grid_bphi = df_grid.pivot(index='lat', columns='lon', values='Bphi').values
    
    interp_bmag = RegularGridInterpolator((lats, lons), grid_bmag, bounds_error=False, fill_value=np.nan)
    interp_br = RegularGridInterpolator((lats, lons), grid_br, bounds_error=False, fill_value=np.nan)
    interp_btheta = RegularGridInterpolator((lats, lons), grid_btheta, bounds_error=False, fill_value=np.nan)
    interp_bphi = RegularGridInterpolator((lats, lons), grid_bphi, bounds_error=False, fill_value=np.nan)
    
    results = []
    
    for site in LANDING_SITES:
        name = site["name"]
        lat = site["lat"]
        lon = site["lon"] % 360
        mission = site["mission"]
        polar_vals = site.get("polar_vals")
        
        point = np.array([[lat, lon]])
        bmag = interp_bmag(point)[0]
        br = interp_br(point)[0]
        btheta = interp_btheta(point)[0]
        bphi = interp_bphi(point)[0]
        
        notes = "PDS Equatorial Grid (Hood et al. 2020)"
        
        # If outside equatorial grid coverage, resolve via South Polar model
        if pd.isna(bmag) and polar_vals is not None:
            bmag, br, btheta, bphi = polar_vals
            notes = site.get("source", "Hood et al. (2022) South Polar Model")
            
        classification = classify_field(bmag)
        
        results.append({
            "name": name,
            "lat": lat,
            "lon": lon,
            "mission": mission,
            "Bmag": float(bmag),
            "Br": float(br),
            "Btheta": float(btheta),
            "Bphi": float(bphi),
            "classification": classification,
            "notes": notes
        })
        
    df_results = pd.DataFrame(results)
    
    logging.info(f"Writing results to {OUTPUT_FILE}")
    df_results.to_csv(OUTPUT_FILE, index=False)
    logging.info("Site identification complete.")
    
    counts = df_results['classification'].value_counts()
    logging.info(f"Classification summary:\n{counts}")

if __name__ == "__main__":
    main()
