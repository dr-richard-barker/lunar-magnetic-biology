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
    
    tex_path = TABLES_DIR / "table1_site_magnetic_values.tex"
    with open(tex_path, 'w') as f:
        f.write("\\begin{table*}[t]\n")
        f.write("\\centering\n")
        f.write("\\small\n")
        f.write("\\caption{\\textbf{Crustal magnetic field environment at planned Artemis, Apollo, Chang'e, and Chandrayaan landing sites.} Total field magnitude $|\\mathbf{B}|$ and vector components at \\SI{30}{\\kilo\\meter} altitude derived from Lunar Prospector and Kaguya observations.}\n")
        f.write("\\label{tab:site_magnetic_values}\n")
        f.write("\\begin{tabular}{llrrccl}\n")
        f.write("\\toprule\n")
        f.write("\\textbf{Landing Site} & \\textbf{Mission} & \\textbf{Latitude ($^\\circ$)} & \\textbf{Longitude ($^\\circ$)} & \\textbf{$|\\mathbf{B}|$ at 30 km (nT)} & \\textbf{Classification} & \\textbf{Data Source} \\\\\n")
        f.write("\\midrule\n")
        
        for _, row in df.iterrows():
            name = row['name']
            mission = row['mission']
            lat = f"{row['lat']:.2f}"
            lon = f"{row['lon']:.2f}"
            bmag = f"{row['Bmag']:.2f}"
            classification = row['classification']
            source = row['notes'].replace('&', '\\&')
            f.write(f"{name} & {mission} & {lat} & {lon} & {bmag} & {classification} & {source} \\\\\n")
            
        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n")
        f.write("\\end{table*}\n")
        
    logging.info(f"Generated {tex_path.name}")

def generate_table2_and_csv():
    """Table 2 & CSV: Systematic review of hypomagnetic field (HMF) effects on biology."""
    data = [
        ["\\textit{Arabidopsis thaliana}", "Near-null ($<\\SI{1}{\\micro\\tesla}$)", "Delayed flowering time", "Cryptochrome and phytochrome signaling disruption", "Agliassa et al. (2018) \\citep{Agliassa2018}"],
        ["\\textit{Arabidopsis thaliana}", "Near-null ($<\\SI{1}{\\micro\\tesla}$)", "Disrupted root growth and morphology", "PIN2 polar auxin transport redistribution", "Narayana et al. (2018) \\citep{Narayana2018}"],
        ["\\textit{Arabidopsis thaliana}", "Hypomagnetic ($<\\SI{5}{\\micro\\tesla}$)", "Impaired iron uptake and homeostasis", "Downregulation of FIT and IRT1 transcription", "Narayana et al. (2021) \\citep{Narayana2021}"],
        ["\\textit{Arabidopsis thaliana}", "Near-null ($<\\SI{1}{\\micro\\tesla}$)", "Reactive oxygen species (ROS) imbalance", "Redox signaling and antioxidant enzyme shift", "Maffei (2014) \\citep{Maffei2014}"],
        ["Higher Plants (General)", "Hypomagnetic ($<\\SI{5}{\\micro\\tesla}$)", "Reduced photosynthetic efficiency", "Thylakoid ultrastructure and electron transport disruption", "Belyavskaya (2004) \\citep{Belyavskaya2004}"],
        ["Microorganisms (Bacteria)", "Hypomagnetic ($<\\SI{5}{\\micro\\tesla}$)", "Altered cell division and growth kinetics", "Membrane potential and ion channel modulation", "Creanga et al. (2009) \\citep{Creanga2009}"],
        ["Magnetotactic Bacteria", "Near-null ($<\\SI{1}{\\micro\\tesla}$)", "Loss of geomagnetic orientation", "Magnetosome chain dipolar alignment loss", "Frankel et al. (1981) \\citep{Frankel1981}"],
        ["Gut Microbiome (Murine)", "Hypomagnetic ($<\\SI{5}{\\micro\\tesla}$)", "Altered bacterial community structure", "Phylum-level taxonomic ratio shifts (Bacteroidetes/Firmicutes)", "Zhang et al. (2017) \\citep{Zhang2017}"],
        ["\\textit{Drosophila melanogaster}", "Hypomagnetic ($<\\SI{5}{\\micro\\tesla}$)", "Circadian rhythm period lengthening", "Cryptochrome-dependent radical pair modulation", "Yoshii et al. (2009) \\citep{Yoshii2009}"],
        ["\\textit{Drosophila melanogaster}", "Near-null ($<\\SI{1}{\\micro\\tesla}$)", "Embryonic developmental delays", "Mitochondrial metabolic pathway alterations", "Vitas et al. (2015) \\citep{Vitas2015}"],
        ["\\textit{Caenorhabditis elegans}", "Hypomagnetic ($<\\SI{5}{\\micro\\tesla}$)", "Altered burrowing and magnetosensation", "AFD sensory neuron and DAF-16 pathway changes", "Vidal-Gadea et al. (2015) \\citep{VidalGadea2015}"],
        ["Human Neuroblastoma Cells", "Hypomagnetic ($<\\SI{1}{\\micro\\tesla}$)", "Altered gene expression and proliferation", "Transcriptomic rewiring of cell cycle genes", "Mo et al. (2012) \\citep{Mo2012}"],
        ["Mammalian Model (Rat)", "Hypomagnetic ($<\\SI{1}{\\micro\\tesla}$)", "Exacerbated musculoskeletal bone loss", "Osteoblast suppression and osteoclast activation", "Xu et al. (2012) \\citep{Xu2012}"],
        ["Mammalian Model (Rat)", "Near-null ($<\\SI{1}{\\micro\\tesla}$)", "Accelerated trabecular bone demineralization", "Hindlimb unloading synergy with HMF", "Mo et al. (2014) \\citep{Mo2014}"],
        ["Human Cardiovascular", "Near-null ($<\\SI{1}{\\micro\\tesla}$)", "Altered microcirculatory capillary flow", "Endothelial and autonomic tone modulation", "Gurfinkel et al. (2014) \\citep{Gurfinkel2014}"],
        ["Mammalian Cells (General)", "Hypomagnetic ($<\\SI{1}{\\micro\\tesla}$)", "Altered DNA damage response and repair", "Radical pair spin state recombination kinetics", "Binhi and Prato (2017) \\citep{Binhi2017}"]
    ]
    
    # Save CSV
    clean_csv_data = [
        [row[0].replace('\\textit{', '').replace('}', ''),
         row[1].replace('\\SI{', '').replace('}{\\micro\\tesla}', ' µT').replace('$<', '<').replace('$', ''),
         row[2], row[3], row[4].split('\\citep')[0].strip()]
        for row in data
    ]
    df_csv = pd.DataFrame(clean_csv_data, columns=["Organism / Model", "Magnetic Condition", "Biological Effect", "Mechanism", "Key Reference"])
    csv_path = PROCESSED_DIR / "biology_literature_summary.csv"
    df_csv.to_csv(csv_path, index=False)
    logging.info(f"Generated {csv_path.name}")
    
    # Save LaTeX
    tex_path = TABLES_DIR / "table2_biology_literature.tex"
    with open(tex_path, 'w') as f:
        f.write("\\begin{table*}[t]\n")
        f.write("\\centering\n")
        f.write("\\small\n")
        f.write("\\caption{\\textbf{Systematic synthesis of biological responses and physiological mechanisms documented under hypomagnetic field (HMF) conditions.} Summary of peer-reviewed experimental literature across plants, microbes, animals, and human cellular models.}\n")
        f.write("\\label{tab:biology_review}\n")
        f.write("\\begin{tabular}{p{3.2cm}p{2.6cm}p{3.6cm}p{4.6cm}p{3.2cm}}\n")
        f.write("\\toprule\n")
        f.write("\\textbf{Organism / Model} & \\textbf{Condition} & \\textbf{Biological Effect} & \\textbf{Mechanism} & \\textbf{Key Reference} \\\\\n")
        f.write("\\midrule\n")
        
        for row in data:
            f.write(f"{row[0]} & {row[1]} & {row[2]} & {row[3]} & {row[4]} \\\\\n")
            
        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n")
        f.write("\\end{table*}\n")
        
    logging.info(f"Generated {tex_path.name}")

def generate_table3():
    """Table 3: Risk matrix across lunar magnetic environments."""
    tex_path = TABLES_DIR / "table3_risk_matrix.tex"
    with open(tex_path, 'w') as f:
        f.write("\\begin{table*}[t]\n")
        f.write("\\centering\n")
        f.write("\\small\n")
        f.write("\\caption{\\textbf{Biological risk matrix across lunar magnetic environments.} Qualitative risk classification for key biological processes relative to baseline terrestrial geomagnetic field (GMF) exposure.}\n")
        f.write("\\label{tab:risk_matrix}\n")
        f.write("\\begin{tabular}{p{4.8cm}cccc}\n")
        f.write("\\toprule\n")
        f.write("\\textbf{Biological System} & \\textbf{Earth GMF ($\\sim\\SI{50}{\\micro\\tesla}$)} & \\textbf{Lunar High-Field ($>\\SI{5}{\\nano\\tesla}$)} & \\textbf{Lunar Moderate ($\\SI{1}{--}\\SI{5}{\\nano\\tesla}$)} & \\textbf{Lunar Null-Field ($<\\SI{1}{\\nano\\tesla}$)} \\\\\n")
        f.write("\\midrule\n")
        f.write("Plant Vegetative Growth and Biomass & Nominal (Baseline) & Low-Moderate Risk & Moderate Risk & High Risk \\\\\n")
        f.write("Plant Flowering and Seed Production & Nominal (Baseline) & Moderate Risk & Moderate-High Risk & High Risk \\\\\n")
        f.write("Microbial Ecology and Biofilm Dynamics & Nominal (Baseline) & Low Risk & Low-Moderate Risk & Moderate Risk \\\\\n")
        f.write("Animal Development and Circadian Clocks & Nominal (Baseline) & Moderate Risk & Moderate-High Risk & High Risk \\\\\n")
        f.write("Human Cellular Integrity and Bone Mass & Nominal (Baseline) & Moderate-High Risk & High Risk & High Risk \\\\\n")
        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n")
        f.write("\\end{table*}\n")
        
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
