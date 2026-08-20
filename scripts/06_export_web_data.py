#!/usr/bin/env python3
"""
06_export_web_data.py

Exports processed lunar magnetic data for use in a Three.js web globe application.
- Downsamples the grid to ~1° resolution to reduce JSON payload size.
- Outputs docs/assets/js/mag_field_data.json.
- Outputs an equirectangular PNG texture for direct use as a Three.js material map.
"""

import json
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.ndimage import zoom

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
GRID_FILE = PROCESSED_DIR / "lunar_mag_field_grid.csv"
SITES_FILE = PROCESSED_DIR / "landing_sites_magnetic.csv"
WEB_JS_DIR = PROJECT_ROOT / "docs" / "assets" / "js"
WEB_IMG_DIR = PROJECT_ROOT / "docs" / "assets" / "img"

JSON_OUTPUT = WEB_JS_DIR / "mag_field_data.json"
TEXTURE_OUTPUT = WEB_IMG_DIR / "lunar_mag_texture.png"

def ensure_directories():
    WEB_JS_DIR.mkdir(parents=True, exist_ok=True)
    WEB_IMG_DIR.mkdir(parents=True, exist_ok=True)

def export_json(df_grid, df_sites):
    """Downsample grid and export to JSON with site data."""
    logging.info("Preparing JSON data...")
    
    # Downsample grid: currently 0.5 deg (720x261 if 65S to 65N)
    # We'll take roughly every 2nd point to get ~1.0 deg resolution
    df_downsampled = df_grid[(df_grid['lat'] * 2).round() % 2 == 0]
    df_downsampled = df_downsampled[(df_downsampled['lon'] * 2).round() % 2 == 0]
    
    lats = np.sort(df_downsampled['lat'].unique())
    lons = np.sort(df_downsampled['lon'].unique())
    
    # Reshape to 2D array, fill NaNs with 0 for web visualization simplicity
    grid_pivot = df_downsampled.pivot(index='lat', columns='lon', values='Bmag').fillna(0)
    
    sites_list = df_sites.replace({np.nan: None}).to_dict(orient='records')
    
    data = {
        "grid": {
            "lat_min": float(lats.min()),
            "lat_max": float(lats.max()),
            "lon_min": float(lons.min()),
            "lon_max": float(lons.max()),
            "resolution": 1.0,
            "values": grid_pivot.values.tolist()
        },
        "sites": sites_list,
        "metadata": {
            "source": "NASA PDS",
            "doi": "10.17189/1520494",
            "altitude_km": 30,
            "units": "nT"
        }
    }
    
    with open(JSON_OUTPUT, 'w') as f:
        json.dump(data, f, separators=(',', ':')) # compact
    logging.info(f"Exported JSON to {JSON_OUTPUT}")

def export_texture(df_grid):
    """Export an equirectangular PNG texture of the magnetic field."""
    logging.info("Preparing equirectangular texture...")
    
    # For a full global texture, we need 90S to 90N. 
    # If our data is 65S to 65N, we pad the rest with 0s.
    lons = np.arange(0, 360, 0.5)
    lats = np.arange(-90, 90.5, 0.5)
    
    full_grid = pd.DataFrame([(lat, lon) for lat in lats for lon in lons], columns=['lat', 'lon'])
    merged = pd.merge(full_grid, df_grid[['lat', 'lon', 'Bmag']], on=['lat', 'lon'], how='left')
    
    Z = merged.pivot(index='lat', columns='lon', values='Bmag').fillna(0).values
    
    # The image origin for matplotlib is bottom-left, but textures usually expect top-left.
    # Flip upside down for standard UV mapping.
    Z = np.flipud(Z)
    
    plt.imsave(TEXTURE_OUTPUT, Z, cmap='viridis', vmin=0, vmax=np.nanpercentile(df_grid['Bmag'], 98))
    logging.info(f"Exported texture to {TEXTURE_OUTPUT}")

def main():
    logging.info("Starting web data export...")
    ensure_directories()
    
    if not GRID_FILE.exists() or not SITES_FILE.exists():
        logging.error("Processed data missing. Run scripts 02 and 03 first.")
        return
        
    df_grid = pd.read_csv(GRID_FILE)
    df_sites = pd.read_csv(SITES_FILE)
    
    try:
        export_json(df_grid, df_sites)
        export_texture(df_grid)
        logging.info("Web data export complete.")
    except Exception as e:
        logging.error(f"Web data export failed: {e}")

if __name__ == "__main__":
    main()
