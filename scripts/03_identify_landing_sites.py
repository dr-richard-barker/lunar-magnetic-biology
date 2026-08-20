#!/usr/bin/env python3
"""
03_identify_landing_sites.py

Maps hardcoded lunar landing sites to magnetic field values by performing
bilinear interpolation on the gridded magnetic dataset. Output is classified
by expected biological impact levels (high, moderate, low/null).

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

# Landing sites database (name, lat, lon, mission)
LANDING_SITES = [
    # Artemis III candidates (~84-90 S)
    ("Faustini Rim A", -85.3, 77.0, "Artemis"),
    ("Peak Near Shackleton", -89.7, 166.0, "Artemis"),
    ("Connecting Ridge", -88.0, 137.0, "Artemis"),
    ("Connecting Ridge Extension", -88.3, 148.0, "Artemis"),
    ("de Gerlache Rim 1", -88.5, -70.0 + 360, "Artemis"), # Normalize negative lon
    ("de Gerlache Rim 2", -88.7, -66.0 + 360, "Artemis"),
    ("de Gerlache-Kocher Massif", -86.0, -75.0 + 360, "Artemis"),
    ("Haworth", -87.4, -2.0 + 360, "Artemis"),
    ("Malapert Massif", -86.0, 0.0, "Artemis"),
    ("Leibnitz Beta Plateau", -85.0, 31.0, "Artemis"),
    ("Nobile Rim 1", -85.4, 35.0, "Artemis"),
    ("Nobile Rim 2", -84.8, 47.0, "Artemis"),
    ("Amundsen Rim", -84.5, 85.0, "Artemis"),
    
    # Historic Apollo
    ("Apollo 11", 0.67, 23.47, "Apollo"),
    ("Apollo 12", -3.01, -23.42 + 360, "Apollo"),
    ("Apollo 14", -3.65, -17.47 + 360, "Apollo"),
    ("Apollo 15", 26.13, 3.63, "Apollo"),
    ("Apollo 16", -8.97, 15.50, "Apollo"),
    ("Apollo 17", 20.19, 30.77, "Apollo"),
    
    # Chang'e
    ("Chang'e 3", 44.12, -19.51 + 360, "Chang'e"),
    ("Chang'e 4", -45.46, 177.60, "Chang'e"),
    ("Chang'e 5", 43.06, -51.92 + 360, "Chang'e"),
    
    # Chandrayaan
    ("Chandrayaan-3", -69.37, 32.35, "Chandrayaan")
]

def classify_field(bmag):
    """Classify magnetic field strength for biology perspective."""
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
        raise FileNotFoundError(f"Run 02_process_magnetic_data.py first.")
        
    # Load grid data
    df_grid = pd.read_csv(GRID_FILE)
    
    # Create interpolators
    lats = np.sort(df_grid['lat'].unique())
    lons = np.sort(df_grid['lon'].unique())
    
    # Reshape data into 2D grids (lat, lon)
    grid_bmag = df_grid.pivot(index='lat', columns='lon', values='Bmag').values
    grid_br = df_grid.pivot(index='lat', columns='lon', values='Br').values
    grid_btheta = df_grid.pivot(index='lat', columns='lon', values='Btheta').values
    grid_bphi = df_grid.pivot(index='lat', columns='lon', values='Bphi').values
    
    interp_bmag = RegularGridInterpolator((lats, lons), grid_bmag, bounds_error=False, fill_value=np.nan)
    interp_br = RegularGridInterpolator((lats, lons), grid_br, bounds_error=False, fill_value=np.nan)
    interp_btheta = RegularGridInterpolator((lats, lons), grid_btheta, bounds_error=False, fill_value=np.nan)
    interp_bphi = RegularGridInterpolator((lats, lons), grid_bphi, bounds_error=False, fill_value=np.nan)
    
    results = []
    
    for name, lat, lon, mission in LANDING_SITES:
        # Normalize lon to 0-360
        lon_norm = lon % 360
        
        point = np.array([[lat, lon_norm]])
        bmag = interp_bmag(point)[0]
        br = interp_br(point)[0]
        btheta = interp_btheta(point)[0]
        bphi = interp_bphi(point)[0]
        
        classification = classify_field(bmag)
        notes = ""
        if pd.isna(bmag):
            notes = "polar — see polar dataset or out of bounds"
            
        results.append({
            "name": name,
            "lat": lat,
            "lon": lon_norm,
            "mission": mission,
            "Bmag": bmag,
            "Br": br,
            "Btheta": btheta,
            "Bphi": bphi,
            "classification": classification,
            "notes": notes
        })
        
    df_results = pd.DataFrame(results)
    
    logging.info(f"Writing results to {OUTPUT_FILE}")
    df_results.to_csv(OUTPUT_FILE, index=False)
    logging.info("Site identification complete.")
    
    # Log summary
    counts = df_results['classification'].value_counts()
    logging.info(f"Classification summary:\n{counts}")

if __name__ == "__main__":
    main()
