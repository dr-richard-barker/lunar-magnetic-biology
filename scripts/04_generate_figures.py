#!/usr/bin/env python3
"""
04_generate_figures.py

Generates 7 publication-quality figures for the lunar magnetic biology project.
Adheres to Nature Publishing Group (NPG) guidelines:
- 300 DPI vector PDF & web PNG
- Arial/Helvetica fonts, 7pt minimum
- Single column (88mm) or double column (180mm) widths
- Colorblind-safe colormaps (viridis, plasma, RdBu)

Figures saved to figures/ (PDF) and docs/assets/img/figures/ (PNG).
"""

import os
import logging
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from pathlib import Path

# Try to import Cartopy
try:
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    CARTOPY_AVAILABLE = True
except ImportError:
    CARTOPY_AVAILABLE = False
    logging.info("Cartopy not available. Using native matplotlib projections.")

# Try to import Seaborn
try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
GRID_FILE = PROCESSED_DIR / "lunar_mag_field_grid.csv"
SITES_FILE = PROCESSED_DIR / "landing_sites_magnetic.csv"
FIG_DIR = PROJECT_ROOT / "figures"
DOCS_FIG_DIR = PROJECT_ROOT / "docs" / "assets" / "img" / "figures"

# Matplotlib configuration for NPG guidelines
mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 7.5,
    'axes.labelsize': 8.5,
    'axes.titlesize': 9.0,
    'xtick.labelsize': 7.5,
    'ytick.labelsize': 7.5,
    'legend.fontsize': 7.5,
    'figure.titlesize': 10.0,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

def save_fig(fig, name):
    """Save figure to both PDF and PNG in required directories."""
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_FIG_DIR.mkdir(parents=True, exist_ok=True)
    
    pdf_path = FIG_DIR / f"{name}.pdf"
    png_path = DOCS_FIG_DIR / f"{name}.png"
    
    fig.savefig(pdf_path, format='pdf', dpi=300)
    fig.savefig(png_path, format='png', dpi=300)
    logging.info(f"Saved {name}.pdf and .png")

def load_data():
    """Load grid and landing site data."""
    if not GRID_FILE.exists() or not SITES_FILE.exists():
        logging.error("Required processed CSV files missing. Run scripts 02 and 03 first.")
        raise FileNotFoundError("Processed files missing.")
    df_grid = pd.read_csv(GRID_FILE)
    df_sites = pd.read_csv(SITES_FILE)
    return df_grid, df_sites

def reshape_grid(df_grid, value_col):
    """Reshape dataframe into 2D meshgrid arrays for plotting."""
    lats = np.sort(df_grid['lat'].unique())
    lons = np.sort(df_grid['lon'].unique())
    z = df_grid.pivot(index='lat', columns='lon', values=value_col).values
    lon_mesh, lat_mesh = np.meshgrid(lons, lats)
    return lon_mesh, lat_mesh, z

def plot_fig1(df_grid):
    """Fig 1: Global |B| crustal magnetic field map."""
    lon_mesh, lat_mesh, z_bmag = reshape_grid(df_grid, 'Bmag')
    
    fig = plt.figure(figsize=(7.08, 3.8))
    if CARTOPY_AVAILABLE:
        ax = plt.axes(projection=ccrs.Mollweide(central_longitude=180))
        img = ax.pcolormesh(lon_mesh, lat_mesh, z_bmag, transform=ccrs.PlateCarree(),
                            cmap='viridis', vmin=0, vmax=np.nanpercentile(z_bmag, 98), shading='auto')
        ax.gridlines(draw_labels=False, color='gray', alpha=0.5, linestyle=':')
    else:
        ax = plt.axes()
        img = ax.pcolormesh(lon_mesh, lat_mesh, z_bmag, cmap='viridis',
                            vmin=0, vmax=np.nanpercentile(z_bmag, 98), shading='auto')
        ax.set_xlabel('Longitude (°E)')
        ax.set_ylabel('Latitude (°N)')
        ax.set_xlim(0, 360)
        ax.set_ylim(-65, 65)
        
    cbar = plt.colorbar(img, ax=ax, orientation='horizontal', fraction=0.046, pad=0.08)
    cbar.set_label('Total Crustal Magnetic Field Magnitude $|\\mathbf{B}|$ at 30 km (nT)')
    ax.set_title('Global Lunar Crustal Magnetic Field Magnitude ($|\\mathbf{B}|$, 30 km altitude)')
    
    save_fig(fig, 'fig1_global_mag_map')
    plt.close(fig)

def plot_fig2(df_grid):
    """Fig 2: Br, Btheta, Bphi vector components triptych."""
    lon_mesh, lat_mesh, z_br = reshape_grid(df_grid, 'Br')
    _, _, z_btheta = reshape_grid(df_grid, 'Btheta')
    _, _, z_bphi = reshape_grid(df_grid, 'Bphi')
    
    vlim = np.nanpercentile(np.abs(z_br), 97)
    
    fig, axes = plt.subplots(3, 1, figsize=(7.08, 7.5), sharex=True)
    components = [
        ('Radial Component $B_r$', z_br, axes[0]),
        ('Colatitudinal Component $B_\\theta$ (Southward)', z_btheta, axes[1]),
        ('Azimuthal Component $B_\\phi$ (Eastward)', z_bphi, axes[2])
    ]
    
    for title, z_data, ax in components:
        img = ax.pcolormesh(lon_mesh, lat_mesh, z_data, cmap='RdBu_r',
                            vmin=-vlim, vmax=vlim, shading='auto')
        ax.set_ylabel('Latitude (°N)')
        ax.set_title(title, fontsize=8.5)
        ax.set_ylim(-65, 65)
        cbar = plt.colorbar(img, ax=ax, orientation='vertical', fraction=0.02, pad=0.02)
        cbar.set_label('nT')
        
    axes[2].set_xlabel('Longitude (°E)')
    axes[2].set_xlim(0, 360)
    plt.tight_layout()
    save_fig(fig, 'fig2_mag_components')
    plt.close(fig)

def plot_fig3(df_grid, df_sites):
    """Fig 3: Crustal field map with landing site locations."""
    lon_mesh, lat_mesh, z_bmag = reshape_grid(df_grid, 'Bmag')
    
    fig, ax = plt.subplots(figsize=(7.08, 4.2))
    img = ax.pcolormesh(lon_mesh, lat_mesh, z_bmag, cmap='viridis',
                        vmin=0, vmax=np.nanpercentile(z_bmag, 98), alpha=0.85, shading='auto')
    
    markers = {'Artemis': '*', 'Apollo': 'o', "Chang'e": 's', 'Chandrayaan': '^'}
    colors = {'Artemis': '#ef5350', 'Apollo': '#ffffff', "Chang'e": '#ffca28', 'Chandrayaan': '#29b6f6'}
    
    for mission in ['Apollo', "Chang'e", 'Chandrayaan', 'Artemis']:
        subset = df_sites[df_sites['mission'] == mission]
        if not subset.empty:
            ax.scatter(subset['lon'], subset['lat'], marker=markers.get(mission, 'o'),
                       color=colors.get(mission, 'white'), edgecolor='black', linewidth=0.6,
                       s=60 if mission == 'Artemis' else 35, label=f"{mission} ({len(subset)})", zorder=5)
            
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=4, frameon=True)
    ax.set_xlabel('Longitude (°E)')
    ax.set_ylabel('Latitude (°N)')
    ax.set_xlim(0, 360)
    ax.set_ylim(-90, 65)
    
    cbar = plt.colorbar(img, ax=ax, orientation='vertical', fraction=0.03, pad=0.02)
    cbar.set_label('$|\\mathbf{B}|$ at 30 km (nT)')
    ax.set_title('Lunar Landing Sites and Crustal Magnetic Field Distribution')
    
    plt.tight_layout()
    save_fig(fig, 'fig3_landing_sites_overlay')
    plt.close(fig)

def plot_fig4(df_sites):
    """Fig 4: Bar plot comparing magnetic field strength across all 23 landing sites."""
    fig, ax = plt.subplots(figsize=(7.08, 4.2))
    
    df_sorted = df_sites.sort_values(['mission', 'Bmag'], ascending=[True, False]).reset_index(drop=True)
    
    color_map = {'high-field': '#d32f2f', 'moderate': '#f57c00', 'low/null-field': '#1976d2'}
    bar_colors = [color_map.get(c, '#757575') for c in df_sorted['classification']]
    
    x_pos = np.arange(len(df_sorted))
    bars = ax.bar(x_pos, df_sorted['Bmag'], color=bar_colors, edgecolor='black', linewidth=0.5)
    
    # Threshold lines
    ax.axhline(5.0, color='#d32f2f', linestyle='--', linewidth=0.8, label='High Field Threshold (5 nT)')
    ax.axhline(1.0, color='#f57c00', linestyle=':', linewidth=0.8, label='Moderate Field Threshold (1 nT)')
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels(df_sorted['name'], rotation=55, ha='right', fontsize=6.5)
    ax.set_ylabel('Crustal Field Magnitude $|\\mathbf{B}|$ at 30 km (nT)')
    ax.set_title('Crustal Magnetic Field Magnitude Across Candidate and Historical Landing Sites')
    ax.legend(loc='upper right', frameon=True)
    ax.set_ylim(0, max(df_sorted['Bmag']) * 1.15)
    
    plt.tight_layout()
    save_fig(fig, 'fig4_high_low_comparison')
    plt.close(fig)

def plot_fig5():
    """Fig 5: Biology summary evidence matrix heatmap."""
    organisms = ['Arabidopsis thaliana', 'Microorganisms (Bacteria)', 'Drosophila melanogaster',
                 'Caenorhabditis elegans', 'Human Cellular Models', 'Vertebrate Models (Zebrafish)']
    effects = ['Growth & Biomass', 'Flowering / Dev.', 'DNA Integrity', 'ROS / Oxidative',
               'Gene Expression', 'Biofilm / Motility']
    
    # Quantitative synthesis matrix: 0=No reported effect, 1=Limited, 2=Moderate, 3=Robust/Repeated
    evidence_matrix = np.array([
        [3, 3, 2, 3, 3, 1], # Arabidopsis
        [3, 2, 2, 2, 3, 3], # Bacteria
        [2, 3, 1, 2, 2, 1], # Drosophila
        [2, 2, 1, 2, 3, 2], # C. elegans
        [2, 2, 3, 3, 3, 0], # Human Cells
        [2, 2, 1, 2, 2, 2], # Zebrafish
    ])
    
    fig, ax = plt.subplots(figsize=(7.08, 4.0))
    im = ax.imshow(evidence_matrix, cmap='YlOrRd', vmin=0, vmax=3, aspect='auto')
    
    ax.set_xticks(np.arange(len(effects)))
    ax.set_yticks(np.arange(len(organisms)))
    ax.set_xticklabels(effects, rotation=35, ha='right', fontsize=8)
    ax.set_yticklabels(organisms, fontsize=8)
    
    # Annotate values
    for i in range(len(organisms)):
        for j in range(len(effects)):
            score = evidence_matrix[i, j]
            label = ['None', 'Limited', 'Moderate', 'Strong'][score]
            text_color = 'white' if score >= 2 else 'black'
            ax.text(j, i, label, ha="center", va="center", color=text_color, fontsize=7, weight='bold')
            
    cbar = plt.colorbar(im, ax=ax, orientation='vertical', fraction=0.03, pad=0.03, ticks=[0, 1, 2, 3])
    cbar.ax.set_yticklabels(['0: None', '1: Limited', '2: Moderate', '3: Strong'])
    cbar.set_label('Evidence Strength in Hypomagnetic Field (HMF) Literature')
    ax.set_title('Biological Responses to Hypomagnetic Environments Across Model Systems')
    
    plt.tight_layout()
    save_fig(fig, 'fig5_biology_summary')
    plt.close(fig)

def plot_fig_s1(df_sites):
    """Fig S1: South Pole stereographic projection (60°S - 90°S) with Artemis sites."""
    fig = plt.figure(figsize=(5.5, 5.0))
    ax = fig.add_subplot(111, projection='polar')
    
    # Polar coordinates: theta = lon (radians), r = (90 - |lat|)
    artemis_sites = df_sites[df_sites['mission'] == 'Artemis']
    chandra_site = df_sites[df_sites['mission'] == 'Chandrayaan']
    
    # Latitude rings
    lat_rings = [60, 70, 80, 85]
    r_rings = [90 - l for l in lat_rings]
    ax.set_yticks(r_rings)
    ax.set_yticklabels([f"{l}°S" for l in lat_rings], fontsize=7)
    ax.set_ylim(0, 30) # 90°S to 60°S
    
    # Plot Artemis sites
    for _, site in artemis_sites.iterrows():
        theta = np.radians(site['lon'])
        r = 90 - abs(site['lat'])
        ax.scatter(theta, r, marker='*', color='#ef5350', edgecolor='black', s=90, zorder=6)
        
        # Position labels neatly
        offset_theta = 0.05
        ax.text(theta + offset_theta, r + 0.5, site['name'], fontsize=6.5, weight='bold',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7, edgecolor='none'))
        
    # Plot Chandrayaan-3
    for _, site in chandra_site.iterrows():
        theta = np.radians(site['lon'])
        r = 90 - abs(site['lat'])
        ax.scatter(theta, r, marker='^', color='#29b6f6', edgecolor='black', s=70, zorder=6, label='Chandrayaan-3')
        ax.text(theta + 0.05, r + 0.5, 'Chandrayaan-3', fontsize=6.5, weight='bold',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7, edgecolor='none'))
        
    ax.scatter([], [], marker='*', color='#ef5350', edgecolor='black', s=90, label='Artemis III Candidate Sites (13)')
    ax.legend(loc='lower left', bbox_to_anchor=(-0.1, -0.15), frameon=True, fontsize=7.5)
    ax.set_title('Lunar South Polar Region (60°S–90°S) Candidate Landing Sites', pad=15)
    
    plt.tight_layout()
    save_fig(fig, 'fig_S1_polar_detail')
    plt.close(fig)

def plot_fig_s2(df_grid, df_sites):
    """Fig S2: Histogram of global |B| distribution with vertical landing site lines."""
    fig, ax = plt.subplots(figsize=(7.08, 4.0))
    
    bmag_vals = df_grid['Bmag'].dropna().values
    
    counts, bins, _ = ax.hist(bmag_vals, bins=80, log=True, color='#90a4ae', edgecolor='white', linewidth=0.5)
    
    # Mark notable site locations
    mean_val = np.mean(bmag_vals)
    median_val = np.median(bmag_vals)
    
    ax.axvline(median_val, color='black', linestyle='--', linewidth=1.0, label=f'Global Median ({median_val:.2f} nT)')
    ax.axvline(mean_val, color='#004d40', linestyle='-', linewidth=1.0, label=f'Global Mean ({mean_val:.2f} nT)')
    
    # Mark Apollo 16 & Chang'e 4
    ap16_bmag = df_sites[df_sites['name'] == 'Apollo 16']['Bmag'].values[0]
    ce4_bmag = df_sites[df_sites['name'] == "Chang'e 4 (SPA Basin)"]['Bmag'].values[0]
    artemis_mean = df_sites[df_sites['mission'] == 'Artemis']['Bmag'].mean()
    
    ax.axvline(artemis_mean, color='#1976d2', linestyle=':', linewidth=1.2, label=f'Artemis III Mean ({artemis_mean:.2f} nT)')
    ax.axvline(ap16_bmag, color='#f57c00', linestyle='-.', linewidth=1.2, label=f'Apollo 16 ({ap16_bmag:.2f} nT)')
    ax.axvline(ce4_bmag, color='#d32f2f', linestyle='-.', linewidth=1.2, label=f"Chang'e 4 SPA ({ce4_bmag:.2f} nT)")
    
    ax.set_xlabel('Total Crustal Magnetic Field Magnitude $|\\mathbf{B}|$ at 30 km (nT)')
    ax.set_ylabel('Number of Grid Points (Log Scale)')
    ax.set_title('Global Distribution of Lunar Crustal Magnetic Field Magnitude')
    ax.legend(loc='upper right', frameon=True, fontsize=7.5)
    
    plt.tight_layout()
    save_fig(fig, 'fig_S2_field_histogram')
    plt.close(fig)

def main():
    logging.info("Starting figure generation pipeline...")
    df_grid, df_sites = load_data()
    
    plot_fig1(df_grid)
    plot_fig2(df_grid)
    plot_fig3(df_grid, df_sites)
    plot_fig4(df_sites)
    plot_fig5()
    plot_fig_s1(df_sites)
    plot_fig_s2(df_grid, df_sites)
    
    logging.info("Figure generation pipeline completed successfully.")

if __name__ == "__main__":
    main()
