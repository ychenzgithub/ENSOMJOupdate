# ENSO (ONI) and MJO Indices for Major El Niño Years (1997, 2006, 2015, 2026)

This repository provides automated data acquisition, subseasonal-to-interannual climate index processing, and publication-quality scientific visualization of the **Oceanic Niño Index (ONI)** and the **Wheeler-Hendon Real-time Multivariate MJO (RMM) index**.

It is specifically tailored to analyze and contrast the developing **2026 El Niño** with historic benchmark events (**1997**, **2006**, and **2015**) in the context of tropical climate variability and Indonesian drought/peatland fire risk. All four years represent the developing first year (Year 0) of cross-year El Niño episodes (1997–98, 2006–07, 2015–16, 2026–27).

---

## 1. Data Sources & Scientific Background

| Climate Index | Source Organization | Remote URL | Description |
| :--- | :--- | :--- | :--- |
| **Oceanic Niño Index (ONI)** | NOAA Climate Prediction Center (CPC) | [NOAA CPC ONI Data](https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt)<br>Alt: [NOAA PSL ONI](https://psl.noaa.gov/data/correlation/oni.data) | 3-month running mean of ERSST SST anomalies in the Niño 3.4 region ($5^\circ\text{N}–5^\circ\text{S}, 120^\circ\text{W}–170^\circ\text{W}$). Thresholds: Weak ($\ge +0.5^\circ\text{C}$), Moderate ($\ge +1.0^\circ\text{C}$), Strong ($\ge +1.5^\circ\text{C}$), Very Strong ($\ge +2.0^\circ\text{C}$). |
| **MJO Index (RMM1, RMM2)** | Australian Bureau of Meteorology (BoM) | [BoM RMM Real-Time Archive](http://www.bom.gov.au/clim_data/IDCKGEM000/rmm.74toRealtime.txt) | Daily Wheeler and Hendon (2004) Real-time Multivariate MJO indices based on combined EOFs of 15°S–15°N OLR, 850-hPa zonal wind, and 200-hPa zonal wind. Intraseasonal amplitude is $\sqrt{\text{RMM1}^2 + \text{RMM2}^2}$. |

### Key Scientific Relevance for Indonesian Fires
* **El Niño (ONI):** Strong positive ONI anomalies suppress Walker circulation ascendance over the Maritime Continent, inducing acute drought and lengthening the dry season across Sumatra, Kalimantan, and Papua. In Indonesian fire research, 1997, 2006, and 2015 represent the primary historical benchmark disaster years.
* **MJO Phase Modulation:**
  * **Phases 4 & 5 (Maritime Continent):** Enhance deep convection and rainfall over Indonesia, acting as a natural fire-suppression mechanism.
  * **Phases 6–8 & 1–3:** Shift convective activity away from Indonesia into the Western/Central Pacific or Indian Ocean, leaving Indonesia under convective subsidence and exacerbating biomass burning risk.

---

## 2. Directory Structure & Generated Files

```text
.
├── data/
│   ├── oni_raw.txt                   # Raw ASCII downloaded from NOAA CPC
│   ├── rmm_raw.txt                   # Raw ASCII downloaded from BoM
│   ├── oni_monthly.csv               # Processed monthly ONI anomalies (1950–2026)
│   ├── mjo_daily.csv                 # Processed daily RMM1, RMM2, Phase, Amplitude (1974–2026)
│   ├── mjo_monthly.csv               # Aggregated monthly MJO statistics (Mean, SEM, Active Days, MC Days)
│   └── el_nino_events_monthly.csv    # Consolidated dataset for target El Niño years
├── figures/
│   ├── figure1_major_el_nino_monthly_comparison.pdf   # Publication Figure 1 (Vector)
│   ├── figure1_major_el_nino_monthly_comparison.png   # Publication Figure 1 (300 DPI Raster)
│   ├── figure2_el_nino_multi_year_timeseries.pdf      # Publication Figure 2 (Vector)
│   ├── figure2_el_nino_multi_year_timeseries.png      # Publication Figure 2 (300 DPI Raster)
│   ├── figure3_fire_season_mjo_phase_distribution.pdf # Publication Figure 3 (Vector)
│   └── figure3_fire_season_mjo_phase_distribution.png # Publication Figure 3 (300 DPI Raster)
├── data_loader.py                    # Modular data downloading, cleaning, and preprocessing
├── plot_enso_mjo_timeseries.py       # Main plotting script with customizable 2026 overrides
├── test_update_2026.py               # Test/demo script for programmatic 2026 updates
└── README.md                         # Project documentation
```

---

## 3. Publication Figures Overview

### Figure 1: Aligned Annual Evolution Comparison
- **File:** [figure1_major_el_nino_monthly_comparison.png](./figures/figure1_major_el_nino_monthly_comparison.png) ([PDF](./figures/figure1_major_el_nino_monthly_comparison.pdf))
- **Panel a:** Monthly Oceanic Niño Index (ONI, $^\circ\text{C}$) from January to December for 1997, 2006, 2015, and 2026, with shaded NOAA ENSO category zones and right-axis threshold labels.
- **Panel b:** MJO Monthly Mean Amplitude ($\pm 1\text{ SEM}$) with translucent background daily RMM amplitude spread and active threshold ($\ge 1.0$).
- **Panel c:** Active MJO Days per Month (all phases, solid lines) and Maritime Continent Convective Days (Phases 4–5, dashed lines) with the Indonesian fire season (July–October, JASO) highlighted.

### Figure 2: Continuous 24-Month Event Timelines
- **File:** [figure2_el_nino_multi_year_timeseries.png](./figures/figure2_el_nino_multi_year_timeseries.png) ([PDF](./figures/figure2_el_nino_multi_year_timeseries.pdf))
- Dual-axis time series displaying continuous daily MJO amplitude (light blue shading), monthly mean MJO amplitude (blue curve), and monthly ONI anomalies (red/orange filled area) across 4 aligned 24-month panels (Year 0 on left half, Year +1 on right half):
  - **(a)** 1997–1998 Super El Niño
  - **(b)** 2006–2007 El Niño
  - **(c)** 2015–2016 Super El Niño
  - **(d)** 2026–2027 Major El Niño (2026 on left half, 2027 decaying phase on right half)

### Figure 3: Peak Fire Season MJO Phase Breakdown
- **File:** [figure3_fire_season_mjo_phase_distribution.png](./figures/figure3_fire_season_mjo_phase_distribution.png) ([PDF](./figures/figure3_fire_season_mjo_phase_distribution.pdf))
- Distribution of active MJO days across all 8 Wheeler-Hendon phases during the critical fire window (July–October). Highlights the contrast in Maritime Continent convection (Phases 4–5) across benchmark years.

---

## 4. How to Update 2026 Data

The codebase is built so that 2026 data can be updated dynamically as new observations are released or under forecast scenarios.

### Method A: Edit the Configuration Dictionaries in Code
Open [plot_enso_mjo_timeseries.py](./plot_enso_mjo_timeseries.py) and locate the top section:
```python
# ==============================================================================
# 2026 DATA UPDATE & MANUAL OVERRIDES
# ==============================================================================
UPDATE_2026_ONI = {
    8: 2.10,   # August 2026 (JAS ONI)
    9: 2.30,   # September 2026 (ASO ONI)
}

UPDATE_2026_MJO = {
    8: 0.99,   # August 2026 mean amplitude
    9: 1.15,   # September 2026 mean amplitude
}
```
Then run:
```bash
python plot_enso_mjo_timeseries.py
```

### Method B: Command-Line Interface (CLI)
You can supply updates directly from the terminal without modifying code:
```bash
# Update August and September 2026 ONI and MJO values:
python plot_enso_mjo_timeseries.py --update-oni "8=2.10,9=2.30" --update-mjo "8=1.05,9=1.20"
```

### Method C: Automatic Online Fetch
To pull the latest observations directly from NOAA CPC and BoM:
```bash
python plot_enso_mjo_timeseries.py --refresh
```

### Method D: Python Programmatic API
```python
from plot_enso_mjo_timeseries import generate_all_figures

generate_all_figures(
    override_oni={8: 2.10, 9: 2.30},
    override_mjo={8: 1.05, 9: 1.20},
    force_download=False,
)
```

---

## 5. Python Environment Requirements
- Python $\ge 3.10$
- `requests`
- `numpy`
- `pandas`
- `matplotlib`
- `scipy`

Install dependencies:
```bash
pip install requests numpy pandas matplotlib scipy
```

---

## 6. Citations
1. **Wheeler, M. C., & Hendon, H. H. (2004).** An all-season real-time multivariate MJO index: Development of an index for monitoring and prediction. *Monthly Weather Review*, 132(8), 1917–1932.
2. **Gottschalck, J., et al. (2010).** A framework for assessing operational Madden–Julian Oscillation forecasts: A CLIVAR MJO Working Group project. *Bulletin of the American Meteorological Society*, 91(9), 1247–1258.
3. **Huang, B., et al. (2017).** Extended Reconstructed Sea Surface Temperature, Version 5 (ERSSTv5): Upgrades, validations, and intercomparisons. *Journal of Climate*, 30(20), 8179–8205.
