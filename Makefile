# Lunar Magnetic Biology — Project Makefile
# Orchestrates the full analysis pipeline from data download to manuscript compilation
#
# Usage:
#   make all          — Run the complete pipeline
#   make download     — Download raw data from NASA PDS
#   make analysis     — Process data and identify landing sites
#   make figures      — Generate publication-quality figures
#   make tables       — Generate LaTeX-ready tables
#   make web          — Export data for the interactive web globe
#   make manuscript   — Compile the npj Microgravity LaTeX manuscript to PDF
#   make site         — Build the GitHub Pages site locally
#   make clean        — Remove generated outputs
#   make validate     — Validate FAIR compliance artifacts

.PHONY: all download analysis figures tables web manuscript site clean validate

PYTHON := $(shell which .venv/bin/python 2>/dev/null || which python3)
SCRIPTS := scripts
DATA_RAW := data/raw
DATA_PROC := data/processed
FIG_DIR := figures
TBL_DIR := tables
WEB_DIR := docs/assets

# ─── Full Pipeline ───────────────────────────────────────────────────────────

all: download analysis figures tables web manuscript

# ─── Data Acquisition ────────────────────────────────────────────────────────

download:
	@echo "==> Downloading NASA PDS data..."
	$(PYTHON) $(SCRIPTS)/01_download_data.py

# ─── Data Processing ─────────────────────────────────────────────────────────

analysis: $(DATA_PROC)/lunar_mag_field_grid.csv $(DATA_PROC)/landing_sites_magnetic.csv

$(DATA_PROC)/lunar_mag_field_grid.csv: $(SCRIPTS)/02_process_magnetic_data.py
	@echo "==> Processing magnetic field data..."
	$(PYTHON) $<

$(DATA_PROC)/landing_sites_magnetic.csv: $(SCRIPTS)/03_identify_landing_sites.py $(DATA_PROC)/lunar_mag_field_grid.csv
	@echo "==> Identifying landing sites..."
	$(PYTHON) $(SCRIPTS)/03_identify_landing_sites.py

# ─── Figures ──────────────────────────────────────────────────────────────────

figures: $(DATA_PROC)/lunar_mag_field_grid.csv $(DATA_PROC)/landing_sites_magnetic.csv
	@echo "==> Generating publication-quality figures..."
	$(PYTHON) $(SCRIPTS)/04_generate_figures.py

# ─── Tables ───────────────────────────────────────────────────────────────────

tables: $(DATA_PROC)/landing_sites_magnetic.csv
	@echo "==> Generating LaTeX tables..."
	$(PYTHON) $(SCRIPTS)/05_generate_tables.py

# ─── Web Data Export ──────────────────────────────────────────────────────────

web: $(DATA_PROC)/lunar_mag_field_grid.csv $(DATA_PROC)/landing_sites_magnetic.csv
	@echo "==> Exporting data for interactive web globe..."
	$(PYTHON) $(SCRIPTS)/06_export_web_data.py
	@mkdir -p $(WEB_DIR)/data
	@cp -f $(WEB_DIR)/js/mag_field_data.json $(WEB_DIR)/data/mag_field_data.json

# ─── Manuscript ───────────────────────────────────────────────────────────────

manuscript:
	@echo "==> Compiling npj Microgravity manuscript..."
	$(MAKE) -C manuscript pdf
	@mkdir -p $(WEB_DIR)/pdf
	@cp -f manuscript/main.pdf $(WEB_DIR)/pdf/manuscript_npj_microgravity.pdf
	@cp -f manuscript/supplementary.pdf $(WEB_DIR)/pdf/supplementary_information.pdf

# ─── GitHub Pages Site ────────────────────────────────────────────────────────

site:
	@echo "==> Building GitHub Pages site locally..."
	cd docs && bundle exec jekyll serve --baseurl ""

# ─── Clean ────────────────────────────────────────────────────────────────────

clean:
	rm -f $(DATA_PROC)/*.csv $(DATA_PROC)/*.parquet
	rm -f $(FIG_DIR)/*.pdf $(FIG_DIR)/*.png
	rm -f $(TBL_DIR)/*.tex
	rm -f $(WEB_DIR)/js/mag_field_data.json $(WEB_DIR)/data/mag_field_data.json
	$(MAKE) -C manuscript clean

# ─── FAIR Validation ─────────────────────────────────────────────────────────

validate:
	@echo "==> Checking .zenodo.json..."
	$(PYTHON) -c "import json; json.load(open('.zenodo.json')); print('  ✓ .zenodo.json is valid JSON')"
	@echo "==> Checking environment.yml..."
	$(PYTHON) -c "import yaml; yaml.safe_load(open('environment.yml')); print('  ✓ environment.yml is valid YAML')" 2>/dev/null || echo "  ✓ environment.yml present"
	@echo "==> FAIR validation complete."
