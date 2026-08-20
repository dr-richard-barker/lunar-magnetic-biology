# Lunar Crustal Magnetic Field Heterogeneity and Implications for Biological Systems at Candidate Landing Sites

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)

## Overview

This repository contains the analysis pipeline, publication-quality figures, LaTeX manuscript, and interactive web visualization for a study of lunar crustal magnetic field heterogeneity and its potential biological implications for landing site selection.

**Key Outputs:**
- 🌍 **Interactive 3D Moon Globe** — [View Online](https://dr-richard-barker.github.io/lunar-magnetic-biology/globe/)
- 📄 **Manuscript** — LaTeX source in `manuscript/`, formatted for Nature Publishing Group journals
- 📊 **Publication Figures** — Vector PDF figures in `figures/`
- 📋 **Data Tables** — LaTeX-ready tables in `tables/`

## Scientific Context

The Moon lacks a global magnetic field, but possesses localized crustal magnetic anomalies ranging from near-zero to ~20 nT at 30 km altitude. These fields create heterogeneous magnetic environments across potential landing sites. On Earth, the geomagnetic field (~25–65 μT) plays critical roles in biological processes:

- **Navigation**: Magnetoreception in migratory species via the radical pair mechanism
- **Growth & development**: Plant flowering, auxin transport, and iron uptake in *Arabidopsis*
- **Cellular processes**: DNA repair, oxidative stress regulation, circadian rhythm entrainment
- **Microbial ecology**: Community structure, growth rates, biofilm formation

This project maps the magnetic field environment at candidate lunar landing sites (including Artemis III regions) and synthesizes the literature on hypomagnetic field (HMF) effects to inform biological risk assessment for future missions.

## Data Sources

| Dataset | Coverage | Source | DOI |
|---------|----------|--------|-----|
| Lunar Crustal Magnetic Field Map | 65°S – 65°N, 30 km alt | NASA PDS / Hood et al. 2020 | [10.17189/1520494](https://doi.org/10.17189/1520494) |
| Lunar Polar Magnetic Field Maps | 60° – 90° lat (both poles), 20 & 30 km alt | NASA PDS / Hood et al. 2022 | [10.17189/rk57-g992](https://doi.org/10.17189/rk57-g992) |

Data are sourced from the NASA Planetary Data System (PDS) Planetary Plasma Interactions (PPI) Node, derived from **Lunar Prospector** and **SELENE (Kaguya)** vector magnetometer measurements.

## Quickstart

### Prerequisites
- Python 3.11+ with conda or pip
- LaTeX distribution (TeX Live, MacTeX, or MiKTeX) for manuscript compilation
- Ruby + Bundler for local GitHub Pages preview (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/dr-richard-barker/lunar-magnetic-biology.git
cd lunar-magnetic-biology

# Create conda environment
conda env create -f environment.yml
conda activate lunar-magnetic-biology

# Or use pip
pip install -r requirements.txt
```

### Run the Pipeline

```bash
# Full pipeline
make all

# Individual steps
make download    # Fetch data from NASA PDS
make analysis    # Process and merge datasets
make figures     # Generate all publication figures
make tables      # Generate LaTeX tables
make web         # Export data for interactive globe
make manuscript  # Compile LaTeX → PDF
```

### Interactive Globe (Local)

```bash
cd docs
bundle install
bundle exec jekyll serve
# Open http://localhost:4000/lunar-magnetic-biology/globe/
```

## Repository Structure

```
├── data/raw/              # Downloaded PDS data (not tracked in git)
├── data/processed/        # Cleaned, merged datasets
├── scripts/               # Analysis pipeline (01–06)
├── figures/               # Publication-quality PDF figures
├── tables/                # LaTeX-ready data tables
├── manuscript/            # Complete LaTeX manuscript
├── docs/                  # GitHub Pages site with interactive globe
├── CITATION.cff           # Machine-readable citation
├── .zenodo.json           # Zenodo deposit metadata
├── environment.yml        # Conda environment
└── Makefile               # Pipeline orchestration
```

## How to Cite

If you use this code or data in your research, please cite:

```bibtex
@software{lunar_magnetic_biology_2026,
  author    = {Barker, R. et al.},
  title     = {Lunar Crustal Magnetic Field Heterogeneity and Implications
               for Biological Systems at Candidate Landing Sites},
  year      = {2026},
  doi       = {10.5281/zenodo.XXXXXXX},
  url       = {https://github.com/dr-richard-barker/lunar-magnetic-biology}
}
```

## License

This work is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/). See [LICENSE](LICENSE) for details.

NASA PDS data are in the US public domain.

## Acknowledgments

This project uses data from the NASA Planetary Data System, derived from the Lunar Prospector and SELENE (Kaguya) missions. We acknowledge the instrument teams and the PDS Planetary Plasma Interactions Node for data archival and distribution.
