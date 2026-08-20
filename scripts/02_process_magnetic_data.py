#!/usr/bin/env python3
"""
02_process_magnetic_data.py

Processes the PDS .tab ASCII tables of the lunar magnetic field.
Computes derived quantities (magnitude, inclination, declination) and prepares
a tidy CSV grid format suitable for mapping and interpolation.

Output: data/processed/lunar_mag_field_grid.csv
"""

import os
import logging
import numpy as np
import pandas as pd
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
MAIN_TAB_FILE = RAW_DATA_DIR / "Bm_30km_65S65N_0E360E.tab"
OUTPUT_FILE = PROCESSED_DIR / "lunar_mag_field_grid.csv"

def ensure_directories():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def process_equatorial_data():
    """Load and process the main equatorial map."""
    if not MAIN_TAB_FILE.exists():
        logging.error(f"Data file not found: {MAIN_TAB_FILE}")
        raise FileNotFoundError(f"Missing {MAIN_TAB_FILE}. Run 01_download_data.py first.")
    
    logging.info(f"Loading {MAIN_TAB_FILE}...")
    
    # Columns in actual PDS file:
    # 1: Longitude (deg)
    # 2: Latitude (deg)
    # 3: B-Mag. (magnitude, nT)
    # 4: B-Rad. (radial, nT)
    # 5: B-East (eastward, nT)
    # 6: B-North (northward, nT)
    cols = ['lon', 'lat', 'Bmag_original', 'Br', 'BEast', 'BNorth']
    
    df = pd.read_csv(
        MAIN_TAB_FILE, 
        sep=r'\s+', 
        skiprows=11,
        names=cols,
        comment='#'
    )
    
    logging.info(f"Loaded {len(df)} rows of equatorial data.")
    
    # Coordinate system conversion:
    # Bphi = BEast
    # Btheta = -BNorth (colatitude component pointing South)
    df['Bphi'] = df['BEast']
    df['Btheta'] = -df['BNorth']
    
    # Compute derived quantities
    # Bmag = sqrt(Br^2 + Btheta^2 + Bphi^2)
    df['Bmag'] = np.sqrt(df['Br']**2 + df['Btheta']**2 + df['Bphi']**2)
    
    diff = np.abs(df['Bmag'] - df['Bmag_original']).mean()
    logging.info(f"Mean difference between computed and provided Bmag: {diff:.4f} nT")
    
    Bh = np.sqrt(df['Btheta']**2 + df['Bphi']**2)
    df['inclination'] = np.degrees(np.arctan2(df['Br'], Bh))
    df['declination'] = np.degrees(np.arctan2(df['Bphi'], df['BNorth']))
    
    df = df[['lat', 'lon', 'Br', 'Btheta', 'Bphi', 'Bmag', 'inclination', 'declination']]
    return df

def merge_polar_maps(main_df):
    """Placeholder to merge polar maps if they exist in data/raw/polar_maps/."""
    polar_dir = RAW_DATA_DIR / "polar_maps"
    if polar_dir.exists() and list(polar_dir.glob("*.csv")):
        logging.info("Polar maps found. Merging logic should be implemented here.")
        # E.g., load polar grids, interpolate or append where lat > 65 or lat < -65
    else:
        logging.info("No polar maps found to merge. Continuing with equatorial data only.")
    return main_df

def main():
    logging.info("Starting data processing...")
    ensure_directories()
    
    try:
        df = process_equatorial_data()
        df = merge_polar_maps(df)
        
        # Save processed data
        logging.info(f"Saving processed grid to {OUTPUT_FILE}...")
        df.to_csv(OUTPUT_FILE, index=False)
        logging.info("Data processing complete.")
        
        # Log basic stats
        logging.info("\nData Quality Statistics:")
        logging.info(df[['Bmag', 'Br', 'Btheta', 'Bphi']].describe())
        
    except Exception as e:
        logging.error(f"Processing failed: {e}")

if __name__ == "__main__":
    main()
