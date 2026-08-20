#!/usr/bin/env python3
"""
04_generate_figures.py

Generates 7 publication-quality figures for the lunar magnetic biology project.
Adheres to Nature Publishing Group (NPG) guidelines:
- 300 DPI vector PDF & PNG
- Arial/Helvetica fonts, 7pt minimum
- Single column (88mm) or double column (180mm) widths
- Colorblind-safe colormaps (viridis, plasma, RdBu)

Figures are saved to figures/ and docs/assets/img/figures/.
"""

import os
import logging
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from pathlib import Path
import shutil

# Try to import Cartopy, standard for this domain
try:
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    CARTOPY_AVAILABLE = True
except ImportError:
    CARTOPY_AVAILABLE = False
    logging.warning("Cartopy not available. Projections will degrade to standard matplotlib plots.")

# Try to import Seaborn for heatmaps and violins
try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False
    logging.warning("Seaborn not available. Falling back to matplotlib for stats plots.")

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
    'font.size': 7,
    'axes.labelsize': 8,
    'axes.titlesize': 8,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'legend.fontsize': 7,
    'pdf.fonttype': 42,  # TrueType
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
    
    fig.savefig(pdf_path, format='pdf')
    fig.savefig(png_path, format='png')
    logging.info(f"Saved {name}.pdf and .png")

def load_data():
    """Load grid and site data."""
    if not GRID_FILE.exists() or not SITES_FILE.exists():
        raise FileNotFoundError("Processed data missing. Run scripts 02 and 03 first.")
    df_grid = pd.read_csv(GRID_FILE)
    df_sites = pd.read_csv(SITES_FILE)
    return df_grid, df_sites

def reshape_grid(df_grid, value_col):
    """Reshape dataframe column to 2D numpy arrays for plotting."""
    lats = np.sort(df_grid['lat'].unique())
    lons = np.sort(df_grid['lon'].unique())
    Z = df_grid.pivot(index='lat', columns='lon', values=value_col).values
    return lons, lats, Z

def plot_fig1(df_grid):
    """Fig 1: Mollweide projection of |B| field magnitude."""
    lons, lats, bmag = reshape_grid(df_grid, 'Bmag')
    
    # NPG double column width in inches (~7.08)
    fig = plt.figure(figsize=(7.08, 4))
    if CARTOPY_AVAILABLE:
        ax = plt.axes(projection=ccrs.Mollweide(central_longitude=180))
        img = ax.pcolormesh(lons, lats, bmag, transform=ccrs.PlateCarree(), cmap='viridis', shading='auto')
        ax.coastlines(color='none') # No coastlines on moon, but initializes feature
        ax.gridlines(draw_labels=False, color='gray', alpha=0.5, linestyle='--')
    else:
        ax = plt.axes()
        img = ax.pcolormesh(lons, lats, bmag, cmap='viridis', shading='auto')
        ax.set_aspect('equal')
    
    cbar = plt.colorbar(img, orientation='horizontal', pad=0.05, shrink=0.8, ax=ax)
    cbar.set_label('Magnetic Field Magnitude |B| (nT)')
    ax.set_title('Global Lunar Crustal Magnetic Field')
    
    save_fig(fig, 'fig1_global_mag_map')
    plt.close(fig)

def plot_fig2(df_grid):
    """Fig 2: 3-panel (Br, Bθ, Bφ) cylindrical equidistant projection."""
    lons, lats, br = reshape_grid(df_grid, 'Br')
    _, _, btheta = reshape_grid(df_grid, 'Btheta')
    _, _, bphi = reshape_grid(df_grid, 'Bphi')
    
    fig, axs = plt.subplots(3, 1, figsize=(7.08, 8), sharex=True)
    
    cmaps = ['RdBu_r'] * 3
    data = [br, btheta, bphi]
    titles = ['Radial Component ($B_r$)', 'Colatitude Component ($B_\\theta$)', 'Azimuthal Component ($B_\\phi$)']
    
    for i, (ax, d, title) in enumerate(zip(axs, data, titles)):
        vmax = np.nanmax(np.abs(d))
        img = ax.pcolormesh(lons, lats, d, cmap='RdBu', vmin=-vmax, vmax=vmax, shading='auto')
        cbar = plt.colorbar(img, ax=ax, pad=0.02)
        cbar.set_label('nT')
        ax.set_title(title)
        ax.set_ylabel('Latitude ($^\\circ$)')
        if i == 2:
            ax.set_xlabel('Longitude ($^\\circ$)')
            
    plt.tight_layout()
    save_fig(fig, 'fig2_mag_components')
    plt.close(fig)

def plot_fig3(df_grid, df_sites):
    """Fig 3: Robinson projection with |B| + landing sites as markers."""
    lons, lats, bmag = reshape_grid(df_grid, 'Bmag')
    
    fig = plt.figure(figsize=(7.08, 4.5))
    if CARTOPY_AVAILABLE:
        ax = plt.axes(projection=ccrs.Robinson(central_longitude=180))
        img = ax.pcolormesh(lons, lats, bmag, transform=ccrs.PlateCarree(), cmap='viridis', shading='auto', alpha=0.7)
        ax.gridlines(draw_labels=False, color='gray', alpha=0.5, linestyle='--')
    else:
        ax = plt.axes()
        img = ax.pcolormesh(lons, lats, bmag, cmap='viridis', shading='auto', alpha=0.7)
    
    # Plot sites
    markers = {'Artemis': '*', 'Apollo': 'o', "Chang'e": 'd', 'Chandrayaan': 'd'}
    colors = {'Artemis': 'red', 'Apollo': 'white', "Chang'e": 'orange', 'Chandrayaan': 'cyan'}
    
    for mission in df_sites['mission'].unique():
        subset = df_sites[df_sites['mission'] == mission]
        if CARTOPY_AVAILABLE:
            ax.scatter(subset['lon'], subset['lat'], marker=markers.get(mission, 'o'), 
                       color=colors.get(mission, 'white'), edgecolor='black', s=40,
                       transform=ccrs.PlateCarree(), label=mission, zorder=5)
        else:
            ax.scatter(subset['lon'], subset['lat'], marker=markers.get(mission, 'o'), 
                       color=colors.get(mission, 'white'), edgecolor='black', s=40,
                       label=mission, zorder=5)
            
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=4)
    cbar = plt.colorbar(img, ax=ax, orientation='vertical', fraction=0.03, pad=0.04)
    cbar.set_label('|B| (nT)')
    ax.set_title('Lunar Landing Sites and Crustal Magnetic Field')
    
    save_fig(fig, 'fig3_landing_sites_overlay')
    plt.close(fig)

def plot_fig4(df_sites):
    """Fig 4: Grouped bar or violin plot of |B| at each site."""
    fig, ax = plt.subplots(figsize=(7.08, 4))
    
    # Drop unknown sites
    df_clean = df_sites.dropna(subset=['Bmag']).copy()
    df_clean = df_clean.sort_values('Bmag', ascending=False)
    
    if SEABORN_AVAILABLE:
        sns.barplot(data=df_clean, x='name', y='Bmag', hue='classification', dodge=False, ax=ax,
                    palette={'high-field': 'red', 'moderate': 'orange', 'low/null-field': 'blue'})
    else:
        ax.bar(df_clean['name'], df_clean['Bmag'])
        
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_ylabel('Magnetic Field Magnitude (nT)')
    ax.set_xlabel('Landing Site')
    ax.set_title('Magnetic Environment at Planned and Historic Landing Sites')
    
    plt.tight_layout()
    save_fig(fig, 'fig4_high_low_comparison')
    plt.close(fig)

def plot_fig5():
    """Fig 5: Biology summary heatmap."""
    organisms = ['Arabidopsis', 'Bacteria', 'Drosophila', 'C. elegans', 'Human cells', 'Zebrafish']
    effects = ['Growth', 'Reproduction', 'DNA repair', 'Navigation', 'Gene expression', 'Oxidative stress']
    
    # Mock data for evidence strength (0=none, 1=limited, 2=moderate, 3=strong)
    data = np.array([
        [2, 1, 3, 0, 3, 3], # Arabidopsis
        [3, 2, 1, 3, 2, 2], # Bacteria
        [1, 2, 1, 3, 2, 1], # Drosophila
        [1, 2, 0, 1, 2, 2], # C. elegans
        [2, 1, 3, 0, 2, 3], # Human cells
        [2, 2, 1, 2, 1, 1], # Zebrafish
    ])
    
    fig, ax = plt.subplots(figsize=(7.08, 4))
    if SEABORN_AVAILABLE:
        sns.heatmap(data, annot=True, xticklabels=effects, yticklabels=organisms, 
                    cmap='plasma', cbar_kws={'label': 'Evidence Strength (0=None to 3=Strong)'}, ax=ax)
    else:
        im = ax.imshow(data, cmap='plasma')
        ax.set_xticks(np.arange(len(effects)))
        ax.set_yticks(np.arange(len(organisms)))
        ax.set_xticklabels(effects, rotation=45, ha='right')
        ax.set_yticklabels(organisms)
        plt.colorbar(im, label='Evidence Strength (0=None to 3=Strong)')
        
    ax.set_title('Biological Effects in Altered Magnetic Environments')
    plt.tight_layout()
    save_fig(fig, 'fig5_biology_summary')
    plt.close(fig)

def plot_fig_s1(df_grid, df_sites):
    """Fig S1: South pole stereographic projection (60-90°S)."""
    fig = plt.figure(figsize=(4, 4))
    
    if CARTOPY_AVAILABLE:
        ax = plt.axes(projection=ccrs.SouthPolarStereo())
        ax.set_extent([-180, 180, -90, -60], ccrs.PlateCarree())
        
        lons, lats, bmag = reshape_grid(df_grid, 'Bmag')
        img = ax.pcolormesh(lons, lats, bmag, transform=ccrs.PlateCarree(), cmap='viridis', shading='auto')
        
        artemis = df_sites[df_sites['mission'] == 'Artemis']
        ax.scatter(artemis['lon'], artemis['lat'], transform=ccrs.PlateCarree(), 
                   color='red', marker='*', s=50, edgecolor='black', zorder=5)
                   
        cbar = plt.colorbar(img, ax=ax, pad=0.05, shrink=0.8)
        cbar.set_label('|B| (nT)')
        ax.set_title('South Pole Artemis Landing Sites')
    else:
        ax = plt.axes()
        ax.text(0.5, 0.5, 'Cartopy required for polar projection', ha='center', va='center')
        
    save_fig(fig, 'fig_S1_polar_detail')
    plt.close(fig)

def plot_fig_s2(df_grid, df_sites):
    """Fig S2: Histogram of global |B| distribution with vertical lines."""
    fig, ax = plt.subplots(figsize=(7.08, 4))
    
    bmag_vals = df_grid['Bmag'].dropna().values
    
    if SEABORN_AVAILABLE:
        sns.histplot(bmag_vals, bins=100, log_scale=(False, True), ax=ax, color='gray')
    else:
        ax.hist(bmag_vals, bins=100, log=True, color='gray', edgecolor='black')
        
    # Add vertical lines for sites
    colors = {'Artemis': 'red', 'Apollo': 'blue', "Chang'e": 'orange'}
    for mission in ['Artemis', 'Apollo', "Chang'e"]:
        sub = df_sites[(df_sites['mission'] == mission) & (df_sites['Bmag'].notna())]
        if not sub.empty:
            mean_val = sub['Bmag'].mean()
            ax.axvline(mean_val, color=colors.get(mission, 'black'), linestyle='--', 
                       label=f'{mission} Mean')
                       
    ax.legend()
    ax.set_xlabel('Magnetic Field Magnitude (nT)')
    ax.set_ylabel('Frequency (Log Scale)')
    ax.set_title('Global Distribution of Crustal Magnetic Field Magnitude')
    
    plt.tight_layout()
    save_fig(fig, 'fig_S2_field_histogram')
    plt.close(fig)

def main():
    logging.info("Starting figure generation...")
    try:
        df_grid, df_sites = load_data()
        
        plot_fig1(df_grid)
        plot_fig2(df_grid)
        plot_fig3(df_grid, df_sites)
        plot_fig4(df_sites)
        plot_fig5()
        plot_fig_s1(df_grid, df_sites)
        plot_fig_s2(df_grid, df_sites)
        
        logging.info("All figures generated successfully.")
    except Exception as e:
        logging.error(f"Figure generation failed: {e}")

if __name__ == "__main__":
    main()
