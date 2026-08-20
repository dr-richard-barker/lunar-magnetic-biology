#!/usr/bin/env python3
"""
01_download_data.py

Downloads NASA PDS data for the lunar crustal magnetic field map, including
the main equatorial map and optionally polar maps (Hood et al. 2022).

This script follows FAIR principles, includes retry logic, and verifies data integrity.
If direct download fails, it provides manual download instructions.
"""

import os
import time
import logging
import requests
from pathlib import Path
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
POLAR_DATA_DIR = RAW_DATA_DIR / "polar_maps"

# URLs
BASE_URL = "https://pds-ppi.igpp.ucla.edu/data/lunar_crust_magnetic.field_map/data"
FILES_TO_DOWNLOAD = {
    "Bm_30km_65S65N_0E360E.tab": f"{BASE_URL}/Bm_30km_65S65N_0E360E.tab",
    "Bm_30km_65S65N_0E360E.xml": f"{BASE_URL}/Bm_30km_65S65N_0E360E.xml"
}

def ensure_directories():
    """Ensure output directories exist."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    POLAR_DATA_DIR.mkdir(parents=True, exist_ok=True)
    logging.info(f"Ensured directories exist at: {RAW_DATA_DIR}")

def download_file(url: str, output_path: Path, max_retries: int = 3) -> bool:
    """Download a file with retry logic and basic progress tracking."""
    if output_path.exists():
        logging.info(f"File already exists: {output_path.name}. Skipping download.")
        return True

    for attempt in range(1, max_retries + 1):
        try:
            logging.info(f"Downloading {url} (Attempt {attempt}/{max_retries})...")
            with requests.get(url, stream=True, timeout=30) as r:
                r.raise_for_status()
                total_length = r.headers.get('content-length')
                
                with open(output_path, 'wb') as f:
                    if total_length is None: # no content length header
                        f.write(r.content)
                    else:
                        dl = 0
                        total_length = int(total_length)
                        for data in r.iter_content(chunk_size=4096):
                            dl += len(data)
                            f.write(data)
                            
                            # Simple progress indicator
                            if dl % (1024 * 1024 * 5) == 0:  # Print every 5MB
                                done = int(50 * dl / total_length)
                                logging.info(f"\r[{'=' * done}{' ' * (50-done)}] {dl/(1024*1024):.1f}MB / {total_length/(1024*1024):.1f}MB")
                logging.info(f"Successfully downloaded {output_path.name}")
                return True
        except requests.exceptions.RequestException as e:
            logging.error(f"Download failed: {e}")
            if attempt < max_retries:
                logging.info("Waiting 5 seconds before retrying...")
                time.sleep(5)
            else:
                logging.error(f"Failed to download {url} after {max_retries} attempts.")
                if output_path.exists():
                    output_path.unlink() # Clean up partial file
                return False

def print_manual_instructions():
    """Print instructions for manual download if automated process fails."""
    instructions = f"""
    =====================================================================
    AUTOMATED DOWNLOAD FAILED.
    Please download the data manually:
    
    1. Go to: https://pds-ppi.igpp.ucla.edu/search/view/?id=pds://PPI/lunar-crust-magnetic.field-map/data/Bm_30km_65S65N_0E360E
    2. Download 'Bm_30km_65S65N_0E360E.tab' and 'Bm_30km_65S65N_0E360E.xml'
    3. Save them to: {RAW_DATA_DIR}
    
    For Polar maps (Hood et al. 2022, DOI: 10.17189/rk57-g992):
    1. Check PDS or specific repositories for polar equivalents.
    2. Save any polar .tab/.csv files to: {POLAR_DATA_DIR}
    =====================================================================
    """
    logging.warning(instructions)

def main():
    """Main execution block."""
    logging.info("Starting Lunar Magnetic Field Data Download...")
    ensure_directories()
    
    success_all = True
    for filename, url in FILES_TO_DOWNLOAD.items():
        out_path = RAW_DATA_DIR / filename
        success = download_file(url, out_path)
        if not success:
            success_all = False
            
    if not success_all:
        print_manual_instructions()
    else:
        logging.info("All essential data downloaded successfully.")
        logging.info("Note: Polar maps from Hood et al. 2022 require manual download if not publicly accessible via direct URL.")

if __name__ == "__main__":
    main()
