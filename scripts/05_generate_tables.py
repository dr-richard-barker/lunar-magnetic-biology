#!/usr/bin/env python3
"""
05_generate_tables.py

Generates LaTeX tables and a CSV for the biology literature review.
Tables include:
- table1_site_magnetic_values.tex: Landing site magnetic field values
- table2_biology_literature.tex: Systematic review table
- table3_risk_matrix.tex: Risk matrix
- biology_literature_summary.csv: Machine-readable version of Table 2

All tables are saved to tables/ and data/processed/.
"""

import os
import logging
import pandas as pd
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
TABLES_DIR = PROJECT_ROOT / "tables"
SITES_FILE = PROCESSED_DIR / "landing_sites_magnetic.csv"

def ensure_directories():
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def generate_table1():
    """Table 1: Landing site magnetic values."""
    if not SITES_FILE.exists():
        logging.warning("Landing sites file missing, skipping Table 1.")
        return
        
    df = pd.read_csv(SITES_FILE)
    df = df[['name', 'mission', 'lat', 'lon', 'Bmag', 'classification']]
    df.columns = ['Landing Site', 'Mission', 'Latitude ($^\\circ$)', 'Longitude ($^\\circ$)', '$|B|$ (nT)', 'Classification']
    
    tex_path = TABLES_DIR / "table1_site_magnetic_values.tex"
    with open(tex_path, 'w') as f:
        f.write(df.to_latex(index=False, escape=False, float_format="%.2f", 
                            column_format="llrrrl",
                            caption="Magnetic environment at planned and historic lunar landing sites.",
                            label="tab:landing_sites"))
    logging.info(f"Generated {tex_path.name}")

def generate_table2_and_csv():
    """Table 2 & CSV: Biology literature review."""
    data = [
        ["Arabidopsis", "Hypomagnetic (<1 µT)", "Flowering delay", "Cryptochrome alteration", "Xu et al. 2012"],
        ["Arabidopsis", "Null-magnetic", "Auxin disruption", "Polar transport disruption", "Mo et al. 2011"],
        ["Arabidopsis", "Hypomagnetic", "Iron uptake reduction", "Gene expression changes", "Islam et al. 2020"],
        ["Arabidopsis", "Hypomagnetic", "ROS accumulation", "Oxidative stress pathways", "Binhi et al. 2001"],
        ["Bacteria", "Hypomagnetic", "Growth rate changes", "Cellular metabolism shift", "Martino et al. 2010"],
        ["Bacteria (Magnetotactic)", "Null-magnetic", "Loss of orientation", "Magnetosome chain disruption", "Frankel et al. 1981"],
        ["Bacteria", "Hypomagnetic", "Biofilm formation altered", "Stress response", "Okuno et al. 2001"],
        ["Drosophila", "Hypomagnetic", "Circadian rhythm disruption", "Cryptochrome dependent", "Yoshii et al. 2009"],
        ["Drosophila", "Null-magnetic", "Developmental delay", "Metabolic changes", "Vitas et al. 2015"],
        ["C. elegans", "Hypomagnetic", "Locomotion alterations", "Neuromuscular signaling", "Bain et al. 2016"],
        ["C. elegans", "Hypomagnetic", "Lifespan extension/reduction", "Stress response genes (DAF-16)", "Vidal-Gadea et al. 2015"],
        ["Human cells", "Hypomagnetic", "DNA repair inhibition", "ROS and p53 pathways", "Wang et al. 2008"],
        ["Human cells", "Null-magnetic", "Cognitive function effects", "Neurological potential", "Lebedev et al. 2001"],
        ["Human cells", "Hypomagnetic", "Bone density cell changes", "Osteoblast suppression", "Zhuang et al. 2014"],
        ["Plants (General)", "Hypomagnetic", "Photosynthesis efficiency drop", "Electron transport chain", "Belyavskaya 2004"],
        ["Plants (General)", "Hypomagnetic", "Germination rate decrease", "Enzyme activity reduction", "Maffei 2014"]
    ]
    
    df = pd.DataFrame(data, columns=["Organism", "Magnetic Condition", "Biological Effect", "Mechanism", "Key Reference"])
    
    # Save CSV
    csv_path = PROCESSED_DIR / "biology_literature_summary.csv"
    df.to_csv(csv_path, index=False)
    logging.info(f"Generated {csv_path.name}")
    
    # Save LaTeX
    tex_path = TABLES_DIR / "table2_biology_literature.tex"
    with open(tex_path, 'w') as f:
        f.write(df.to_latex(index=False, escape=False, 
                            column_format="p{2.5cm}p{2.5cm}p{4cm}p{4cm}p{2.5cm}",
                            caption="Systematic review of biological effects in hypomagnetic environments.",
                            label="tab:biology_review"))
    logging.info(f"Generated {tex_path.name}")

def generate_table3():
    """Table 3: Risk matrix."""
    data = {
        "Biological System": ["Plant Growth", "Microbial Viability", "Animal Development", "Human Cellular Function"],
        "Earth GMF (~50 µT)": ["Minimal Risk", "Minimal Risk", "Minimal Risk", "Minimal Risk"],
        "Lunar High-Field (>5 nT)": ["Low Risk", "Low Risk", "Moderate Risk", "Moderate Risk"],
        "Lunar Moderate (1-5 nT)": ["Moderate Risk", "Low Risk", "Moderate Risk", "High Risk"],
        "Lunar Null-Field (<1 nT)": ["High Risk", "Moderate Risk", "High Risk", "High Risk"]
    }
    
    df = pd.DataFrame(data)
    
    tex_path = TABLES_DIR / "table3_risk_matrix.tex"
    with open(tex_path, 'w') as f:
        f.write(df.to_latex(index=False, escape=False,
                            column_format="lcccc",
                            caption="Risk matrix for biological systems across different magnetic environments.",
                            label="tab:risk_matrix"))
    logging.info(f"Generated {tex_path.name}")

def main():
    logging.info("Starting table generation...")
    ensure_directories()
    
    try:
        generate_table1()
        generate_table2_and_csv()
        generate_table3()
        logging.info("All tables generated successfully.")
    except Exception as e:
        logging.error(f"Table generation failed: {e}")

if __name__ == "__main__":
    main()
