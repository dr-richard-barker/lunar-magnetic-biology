#!/usr/bin/env python3
"""
05_generate_tables.py

Generates publication-quality LaTeX tables and CSV datasets:
- table1_site_magnetic_values.tex: Landing site magnetic field values at 30 km altitude
- table2_biology_literature.tex: Systematic review of biological effects in hypomagnetic fields (HMF)
- table3_risk_matrix.tex: Biological risk matrix across lunar magnetic environments
- biology_literature_summary.csv: Machine-readable version of Table 2

Saved to tables/ and data/processed/.
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
    """Table 1: Landing site magnetic field values."""
    if not SITES_FILE.exists():
        logging.warning("Landing sites file missing, skipping Table 1.")
        return
        
    df = pd.read_csv(SITES_FILE)
    df_out = df[['name', 'mission', 'lat', 'lon', 'Bmag', 'classification', 'notes']].copy()
    df_out.columns = ['Landing Site', 'Mission', 'Latitude ($^\\circ$)', 'Longitude ($^\\circ$)', '$|\\mathbf{B}|$ at 30 km (nT)', 'Classification', 'Data Source']
    
    tex_path = TABLES_DIR / "table1_site_magnetic_values.tex"
    with open(tex_path, 'w') as f:
        f.write(df_out.to_latex(index=False, escape=False, float_format="%.2f", 
                                column_format="p{3.2cm}p{1.8cm}rrclp{4.2cm}",
                                caption="Crustal magnetic field environment at planned Artemis, Apollo, Chang'e, and Chandrayaan landing sites.",
                                label="tab:site_magnetic_values"))
    logging.info(f"Generated {tex_path.name}")

def generate_table2_and_csv():
    """Table 2 & CSV: Systematic review of hypomagnetic field (HMF) effects on biology."""
    data = [
        ["Arabidopsis thaliana", "Near-null (<1 µT)", "Delayed flowering time", "Cryptochrome & phytochrome signaling disruption", "Agliassa et al. (2018)"],
        ["Arabidopsis thaliana", "Near-null (<1 µT)", "Disrupted root growth & auxin transport", "PIN2 polar auxin transport redistribution", "Narayana et al. (2018)"],
        ["Arabidopsis thaliana", "Hypomagnetic (<5 µT)", "Impaired iron uptake & homeostasis", "Downregulation of FIT and IRT1 transcription", "Narayana et al. (2021)"],
        ["Arabidopsis thaliana", "Near-null (<1 µT)", "Reactive oxygen species (ROS) imbalance", "Redox signaling & antioxidant enzyme shift", "Maffei (2014)"],
        ["Higher Plants (General)", "Hypomagnetic (<5 µT)", "Reduced photosynthesis & chloroplast alterations", "Thylakoid ultrastructure & ETC disruption", "Belyavskaya (2004)"],
        ["Microorganisms (Bacteria)", "Hypomagnetic (<5 µT)", "Altered cell division & growth kinetics", "Membrane potential & ion channel modulation", "Creanga et al. (2009)"],
        ["Magnetotactic Bacteria", "Near-null (<1 µT)", "Loss of geomagnetic orientation", "Magnetosome chain dipolar alignment loss", "Frankel et al. (1981)"],
        ["Gut Microbiome (Murine)", "Hypomagnetic (<5 µT)", "Altered bacterial community structure", "Phylum-level taxonomic ratio shifts (Bacteroidetes/Firmicutes)", "Zhang et al. (2017)"],
        ["Drosophila melanogaster", "Hypomagnetic (<5 µT)", "Circadian rhythm period lengthening", "Cryptochrome-dependent radical pair modulation", "Yoshii et al. (2009)"],
        ["Drosophila melanogaster", "Near-null (<1 µT)", "Embryonic developmental delays", "Mitochondrial metabolic pathway alterations", "Vitas et al. (2015)"],
        ["Caenorhabditis elegans", "Hypomagnetic (<5 µT)", "Altered burrowing & magnetosensation", "AFD sensory neuron & DAF-16 pathway changes", "Vidal-Gadea et al. (2015)"],
        ["Human Neuroblastoma Cells", "Hypomagnetic (<1 µT)", "Altered gene expression & proliferation", "Transcriptomic rewiring of cell cycle genes", "Mo et al. (2012)"],
        ["Mammalian Model (Rat)", "Hypomagnetic (<1 µT)", "Exacerbated musculoskeletal bone loss", "Osteoblast suppression & osteoclast activation", "Xu et al. (2012)"],
        ["Mammalian Model (Rat)", "Near-null (<1 µT)", "Accelerated trabecular bone demineralization", "Hindlimb unloading synergy with HMF", "Mo et al. (2014)"],
        ["Human Cardiovascular", "Near-null (<1 µT)", "Altered microcirculatory capillary flow", "Endothelial and autonomic tone modulation", "Gurfinkel et al. (2014)"],
        ["Mammalian Cells (General)", "Hypomagnetic (<1 µT)", "Altered DNA damage response & repair", "Radical pair spin state recombination kinetics", "Binhi & Prato (2017)"]
    ]
    
    df = pd.DataFrame(data, columns=["Organism / Model", "Magnetic Condition", "Biological Effect", "Mechanism", "Key Reference"])
    
    # Save CSV
    csv_path = PROCESSED_DIR / "biology_literature_summary.csv"
    df.to_csv(csv_path, index=False)
    logging.info(f"Generated {csv_path.name}")
    
    # Save LaTeX
    tex_path = TABLES_DIR / "table2_biology_literature.tex"
    with open(tex_path, 'w') as f:
        f.write(df.to_latex(index=False, escape=False, 
                            column_format="p{2.8cm}p{2.2cm}p{3.8cm}p{4.2cm}p{2.8cm}",
                            caption="Systematic synthesis of biological responses and physiological mechanisms documented under hypomagnetic field (HMF) conditions.",
                            label="tab:biology_review"))
    logging.info(f"Generated {tex_path.name}")

def generate_table3():
    """Table 3: Risk matrix across lunar magnetic environments."""
    data = {
        "Biological System": [
            "Plant Vegetative Growth & Biomass",
            "Plant Flowering & Seed Production",
            "Microbial Ecology & Biofilm Dynamics",
            "Animal Development & Circadian Entrainment",
            "Human Cellular Integrity & Bone Homeostasis"
        ],
        "Terrestrial GMF (~50 µT)": [
            "Nominal (Baseline)",
            "Nominal (Baseline)",
            "Nominal (Baseline)",
            "Nominal (Baseline)",
            "Nominal (Baseline)"
        ],
        "Lunar High-Field (>5 nT)": [
            "Low-Moderate Risk",
            "Moderate Risk",
            "Low Risk",
            "Moderate Risk",
            "Moderate-High Risk"
        ],
        "Lunar Moderate (1-5 nT)": [
            "Moderate Risk",
            "Moderate-High Risk",
            "Low-Moderate Risk",
            "Moderate-High Risk",
            "High Risk"
        ],
        "Lunar Null-Field (<1 nT)": [
            "High Risk",
            "High Risk",
            "Moderate Risk",
            "High Risk",
            "High Risk"
        ]
    }
    
    df = pd.DataFrame(data)
    
    tex_path = TABLES_DIR / "table3_risk_matrix.tex"
    with open(tex_path, 'w') as f:
        f.write(df.to_latex(index=False, escape=False,
                            column_format="p{3.8cm}cccc",
                            caption="Biological risk matrix evaluating physiological and developmental vulnerability across lunar magnetic environments relative to Earth's geomagnetic field (GMF).",
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
