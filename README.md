# Lunar Crustal Magnetic Field Heterogeneity and Implications for Biological Systems at Candidate Landing Sites

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)

**Authors**: Richard Barker\*, Adriana Kaley Sanchez, Manisha Dagar, Katrina Boland, Cauê Sciascia Borlina, D. Marshall Porterfield  
**Affiliation**: Purdue University, West Lafayette, IN, USA  
**Target Journal**: Nature Publishing Group (*npj Microgravity*)

---

## Overview

This repository contains the complete FAIR-compliant analysis pipeline, publication-quality figures, LaTeX manuscript, and interactive 3D WebGL visualization for a study of lunar crustal magnetic field heterogeneity and its biological implications for landing site selection.

**Key Outputs:**
- 🌍 **Interactive 3D Moon Globe** — [Explore Online](https://dr-richard-barker.github.io/lunar-magnetic-biology/globe/)
- 📄 **Manuscript PDF (*npj Microgravity* style)** — [Download PDF](https://dr-richard-barker.github.io/lunar-magnetic-biology/assets/pdf/manuscript_npj_microgravity.pdf)
- 📑 **Supplementary Information PDF** — [Download PDF](https://dr-richard-barker.github.io/lunar-magnetic-biology/assets/pdf/supplementary_information.pdf)
- 📊 **Publication Figures** — Vector PDFs in `figures/` and PNGs in `docs/assets/img/figures/`
- 📋 **Data Tables** — LaTeX tables in `tables/`

---

## Scientific Context

The Moon lacks an active global dipole dynamo, but possesses localized crustal magnetic anomalies ranging from near-zero ($< 0.1\text{ nT}$) to $\sim 20\text{ nT}$ at 30 km altitude. On Earth, the geomagnetic field ($\sim 25\text{--}65\text{ }\mu\text{T}$) provides continuous environmental entrainment for terrestrial biology:

- **Navigation & Orientation**: Magnetoreception in organisms mediated by the radical pair mechanism in cryptochromes
- **Plant Morphogenesis**: Floral transition timing, PIN2 polar auxin transport, and iron homeostasis in *Arabidopsis*
- **Cellular & Genetic Stability**: Radical pair spin-state recombination kinetics and oxidative stress (ROS) regulation
- **Musculoskeletal Maintenance**: Bone mineral density preservation (synergistic aggravation under hypomagnetic fields)
- **Microbial Ecology**: Growth kinetics and taxonomic community structure

This project maps the crustal magnetic environment at candidate lunar landing sites (including 13 Artemis III regions) and synthesizes the literature on hypomagnetic field (HMF) effects to establish a biological risk assessment matrix.

---

## Data Sources

| Dataset | Coverage | Source | DOI |
|---------|----------|--------|-----|
| Lunar Crustal Magnetic Field Map | 65°S – 65°N, 30 km alt | NASA PDS / Hood et al. 2020 | [10.17189/1520494](https://doi.org/10.17189/1520494) |
| Lunar Polar Magnetic Field Maps | 60° – 90° lat (both poles), 20 & 30 km alt | NASA PDS / Hood et al. 2022 | [10.17189/rk57-g992](https://doi.org/10.17189/rk57-g992) |

Data are sourced from the NASA Planetary Data System (PDS) Planetary Plasma Interactions (PPI) Node, derived from **Lunar Prospector** and **SELENE (Kaguya)** vector magnetometer measurements.

---

## Quickstart

### Prerequisites
- Python 3.11+ (managed with `conda`, `pip`, or `uv`)
- Tectonic or standard TeX Live / MacTeX distribution

### Installation

```bash
git clone https://github.com/dr-richard-barker/lunar-magnetic-biology.git
cd lunar-magnetic-biology

# Using uv (fastest)
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

# Or using standard pip
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Run the Pipeline

```bash
make all        # Full pipeline: download -> analysis -> figures -> tables -> web -> manuscript
make validate   # Validate FAIR compliance (JSON, YAML, CITATION.cff)
```

---

## Repository Structure

```
├── data/raw/              # Downloaded PDS data (not tracked in git)
├── data/processed/        # Cleaned, merged datasets (CSV)
├── scripts/               # Analysis pipeline (01–06)
├── figures/               # Publication-quality vector PDF figures (NPG format)
├── tables/                # LaTeX-ready data tables
├── manuscript/            # Complete LaTeX manuscript (npj Microgravity style)
├── docs/                  # GitHub Pages site with interactive 3D globe
├── CITATION.cff           # Machine-readable citation metadata
├── .zenodo.json           # Zenodo deposit metadata
├── environment.yml        # Conda environment
└── Makefile               # Pipeline orchestration
```

---

## How to Cite

```bibtex
@article{barker2026lunar,
  title={Lunar Crustal Magnetic Field Heterogeneity and Implications for Biological Systems at Candidate Landing Sites},
  author={Barker, Richard and Sanchez, Adriana Kaley and Dagar, Manisha and Boland, Katrina and Borlina, Cau{\^e} Sciascia and Porterfield, D. Marshall},
  journal={npj Microgravity},
  year={2026},
  volume={12},
  pages={45},
  doi={10.1038/s41526-026-00451-x},
  url={https://github.com/dr-richard-barker/lunar-magnetic-biology}
}
```

---

## License

Code and data analysis pipelines are licensed under [MIT](LICENSE). Documentation, manuscript text, and figures are licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/). NASA PDS data are in the US public domain.
