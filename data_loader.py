#!/usr/bin/env python3
"""
data_loader.py
==============
Data loader and preprocessor for Oceanic Niño Index (ONI) and Madden-Julian
Oscillation (MJO) Wheeler-Hendon RMM indices.

Sources:
  - ONI: NOAA Climate Prediction Center (CPC)
    URL: https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt
    Alt: https://psl.noaa.gov/data/correlation/oni.data
  - MJO: Australian Bureau of Meteorology (BOM) Wheeler-Hendon RMM Index
    URL: http://www.bom.gov.au/clim_data/IDCKGEM000/rmm.74toRealtime.txt

Author: Pair-programming assistant & Research Collaborators
Project: IndonesiaFire2026 / ENSO-MJO Analysis
"""

import os
import sys
import logging
import requests
import numpy as np
import pandas as pd
from typing import Dict, Optional, Tuple

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
ONI_RAW_PATH = os.path.join(DATA_DIR, "oni_raw.txt")
MJO_RAW_PATH = os.path.join(DATA_DIR, "rmm_raw.txt")
ONI_CSV_PATH = os.path.join(DATA_DIR, "oni_monthly.csv")
MJO_DAILY_CSV_PATH = os.path.join(DATA_DIR, "mjo_daily.csv")
MJO_MONTHLY_CSV_PATH = os.path.join(DATA_DIR, "mjo_monthly.csv")
COMBINED_CSV_PATH = os.path.join(DATA_DIR, "el_nino_events_monthly.csv")

# Remote URLs
ONI_URL = "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"
ONI_BACKUP_URL = "https://psl.noaa.gov/data/correlation/oni.data"
MJO_URL = "http://www.bom.gov.au/clim_data/IDCKGEM000/rmm.74toRealtime.txt"

# Season to central month mapping (ONI 3-month running means)
SEASON_TO_MONTH = {
    "DJF": 1, "JFM": 2, "FMA": 3, "MAM": 4,
    "AMJ": 5, "MJJ": 6, "JJA": 7, "JAS": 8,
    "ASO": 9, "SON": 10, "OND": 11, "NDJ": 12,
}
MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def ensure_dir(path: str):
    """Ensure directory exists."""
    os.makedirs(path, exist_ok=True)


def download_file(url: str, dest_path: str, timeout: int = 15) -> bool:
    """Download file with browser user-agent header; fallback to cached file if fails."""
    ensure_dir(os.path.dirname(dest_path))
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        logging.info(f"Fetching {url}...")
        resp = requests.get(url, headers=headers, timeout=timeout)
        if resp.status_code == 200 and len(resp.text) > 500:
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(resp.text)
            logging.info(f"Saved {len(resp.text)} bytes to {dest_path}")
            return True
        else:
            logging.warning(f"Failed to fetch {url}: HTTP status {resp.status_code}")
    except Exception as e:
        logging.warning(f"Error downloading from {url}: {e}")

    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 0:
        logging.info(f"Using existing cached file: {dest_path}")
        return True
    return False


def load_oni_data(force_download: bool = False) -> pd.DataFrame:
    """
    Load NOAA CPC ONI data.
    Returns DataFrame with columns: ['Year', 'Month', 'Season', 'SST_Total', 'ONI_Anomaly']
    """
    if force_download or not os.path.exists(ONI_RAW_PATH):
        success = download_file(ONI_URL, ONI_RAW_PATH)
        if not success:
            download_file(ONI_BACKUP_URL, ONI_RAW_PATH)

    if not os.path.exists(ONI_RAW_PATH):
        raise FileNotFoundError(f"Could not find or download ONI data at {ONI_RAW_PATH}")

    with open(ONI_RAW_PATH, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]

    rows = []
    # Identify format: CPC ascii or PSL table
    if lines[0].startswith("SEAS"):
        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 4:
                seas, yr, total, anom = parts[0], parts[1], parts[2], parts[3]
                try:
                    yr = int(yr)
                    mo = SEASON_TO_MONTH.get(seas, None)
                    if mo is not None:
                        rows.append({
                            "Year": yr,
                            "Month": mo,
                            "Season": seas,
                            "SST_Total": float(total),
                            "ONI_Anomaly": float(anom),
                        })
                except ValueError:
                    continue
    else:
        # Fallback for PSL table format
        for line in lines[1:]:
            parts = line.split()
            if len(parts) == 13:
                try:
                    yr = int(parts[0])
                    for mo in range(1, 13):
                        val = float(parts[mo])
                        if val > -90:  # -99.9 indicates missing
                            seas = list(SEASON_TO_MONTH.keys())[mo - 1]
                            rows.append({
                                "Year": yr,
                                "Month": mo,
                                "Season": seas,
                                "SST_Total": np.nan,
                                "ONI_Anomaly": val,
                            })
                except ValueError:
                    continue

    df = pd.DataFrame(rows)
    df.sort_values(by=["Year", "Month"], inplace=True)
    df.to_csv(ONI_CSV_PATH, index=False)
    logging.info(f"Loaded {len(df)} ONI records ({df['Year'].min()}-{df['Year'].max()})")
    return df


def load_mjo_daily(force_download: bool = False) -> pd.DataFrame:
    """
    Load BOM Wheeler-Hendon RMM MJO daily data.
    Returns DataFrame with columns: ['Year', 'Month', 'Day', 'RMM1', 'RMM2', 'Phase', 'Amplitude']
    """
    if force_download or not os.path.exists(MJO_RAW_PATH):
        download_file(MJO_URL, MJO_RAW_PATH)

    if not os.path.exists(MJO_RAW_PATH):
        raise FileNotFoundError(f"Could not find or download MJO data at {MJO_RAW_PATH}")

    with open(MJO_RAW_PATH, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]

    rows = []
    # Skip header lines (first 2 lines typically)
    for line in lines:
        parts = line.split()
        if len(parts) >= 7:
            try:
                yr = int(parts[0])
                mo = int(parts[1])
                day = int(parts[2])
                rmm1 = float(parts[3])
                rmm2 = float(parts[4])
                phase = int(parts[5])
                amp = float(parts[6])
                if amp < 99.0:  # filter missing value codes (999 or 1.E36)
                    rows.append({
                        "Year": yr,
                        "Month": mo,
                        "Day": day,
                        "RMM1": rmm1,
                        "RMM2": rmm2,
                        "Phase": phase,
                        "Amplitude": amp,
                    })
            except ValueError:
                continue

    df = pd.DataFrame(rows)
    df.sort_values(by=["Year", "Month", "Day"], inplace=True)
    df.to_csv(MJO_DAILY_CSV_PATH, index=False)
    logging.info(f"Loaded {len(df)} daily MJO records ({df['Year'].min()}-{df['Year'].max()})")
    return df


def compute_mjo_monthly(df_daily: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate daily MJO records to monthly metrics:
      - mean_amplitude, std_amplitude, sem_amplitude
      - rms_amplitude (root-mean-square)
      - active_days (amp >= 1.0)
      - total_days, active_pct
      - phase45_days (Maritime Continent phases, critical for Indonesian fire suppression)
      - mean_rmm1, mean_rmm2
    """
    def calc_group(g):
        n = len(g)
        amps = g["Amplitude"].values
        mean_amp = float(np.mean(amps))
        std_amp = float(np.std(amps, ddof=1)) if n > 1 else 0.0
        sem_amp = std_amp / np.sqrt(n) if n > 0 else 0.0
        rms_amp = float(np.sqrt(np.mean(amps**2)))
        active_mask = amps >= 1.0
        active_days = int(np.sum(active_mask))
        active_pct = 100.0 * active_days / n if n > 0 else 0.0

        # Maritime Continent phases 4 & 5
        mc_mask = active_mask & (g["Phase"].isin([4, 5]))
        mc_days = int(np.sum(mc_mask))

        return pd.Series({
            "Mean_Amplitude": mean_amp,
            "Std_Amplitude": std_amp,
            "SEM_Amplitude": sem_amp,
            "RMS_Amplitude": rms_amp,
            "Active_Days": active_days,
            "Total_Days": n,
            "Active_Pct": active_pct,
            "MC_Phase45_Days": mc_days,
            "Mean_RMM1": float(np.mean(g["RMM1"])),
            "Mean_RMM2": float(np.mean(g["RMM2"])),
        })

    df_monthly = df_daily.groupby(["Year", "Month"]).apply(calc_group, include_groups=False).reset_index()
    df_monthly.to_csv(MJO_MONTHLY_CSV_PATH, index=False)
    logging.info(f"Computed {len(df_monthly)} monthly MJO records")
    return df_monthly


def get_combined_el_nino_data(
    oni_df: pd.DataFrame,
    mjo_monthly_df: pd.DataFrame,
    target_years=(1997, 1998, 2006, 2007, 2015, 2016, 2026, 2027),
    override_2026_oni: Optional[Dict[int, float]] = None,
    override_2026_mjo: Optional[Dict[int, float]] = None,
) -> pd.DataFrame:
    """
    Combine ONI and MJO monthly metrics for target El Niño years.
    Applies optional overrides/updates for 2026 data.
    """
    merged = pd.merge(oni_df, mjo_monthly_df, on=["Year", "Month"], how="outer")
    subset = merged[merged["Year"].isin(target_years)].copy()

    # Apply 2026 overrides if provided
    if override_2026_oni:
        for mo, val in override_2026_oni.items():
            mask = (subset["Year"] == 2026) & (subset["Month"] == mo)
            if mask.any():
                subset.loc[mask, "ONI_Anomaly"] = val
            else:
                new_row = pd.DataFrame([{
                    "Year": 2026,
                    "Month": mo,
                    "Season": list(SEASON_TO_MONTH.keys())[mo - 1],
                    "ONI_Anomaly": val,
                }])
                subset = pd.concat([subset, new_row], ignore_index=True)

    if override_2026_mjo:
        for mo, val in override_2026_mjo.items():
            mask = (subset["Year"] == 2026) & (subset["Month"] == mo)
            if mask.any():
                subset.loc[mask, "Mean_Amplitude"] = val
            else:
                new_row = pd.DataFrame([{
                    "Year": 2026,
                    "Month": mo,
                    "Mean_Amplitude": val,
                }])
                subset = pd.concat([subset, new_row], ignore_index=True)

    subset.sort_values(by=["Year", "Month"], inplace=True)
    subset.to_csv(COMBINED_CSV_PATH, index=False)
    return subset


if __name__ == "__main__":
    ensure_dir(DATA_DIR)
    oni = load_oni_data(force_download=True)
    mjo_daily = load_mjo_daily(force_download=True)
    mjo_monthly = compute_mjo_monthly(mjo_daily)
    combined = get_combined_el_nino_data(oni, mjo_monthly)
    print("\nData preparation complete!")
    print(f"Target El Niño records summary:\n{combined.groupby('Year')[['ONI_Anomaly', 'Mean_Amplitude']].count()}")
