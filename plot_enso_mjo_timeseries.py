#!/usr/bin/env python3
"""
plot_enso_mjo_timeseries.py
===========================
Publication-quality visualization of Oceanic Niño Index (ONI) and Madden-Julian
Oscillation (MJO) Wheeler-Hendon RMM indices for major El Niño years:
  - 1997 (1997-1998 Super El Niño)
  - 2015 (2015-2016 Super El Niño)
  - 2023 (2023-2024 Strong El Niño)
  - 2026 (2026 Developing/Major El Niño)

Features:
  - Automated data ingestion from NOAA CPC and BOM servers with local caching.
  - User-configurable 2026 data update dictionary and CLI flags.
  - Multi-panel publication-grade figures (Nature/Science aesthetic, 300+ DPI, Okabe-Ito palette):
      * Figure 1: Aligned Jan-Dec annual cycle comparison (ONI, MJO Amplitude, Active MJO Days).
      * Figure 2: Multi-event 24-month continuous timeline (dual-axis ONI and daily/monthly MJO).
      * Figure 3: MJO Phase distribution during the peak Indonesian fire season (July-October).

Author: Pair-programming assistant & Research Collaborators
Project: IndonesiaFire2026 / ENSO-MJO Analysis
"""

import os
import sys
from typing import Dict, Optional, Tuple
import argparse
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# Import data loading functions
from data_loader import (
    load_oni_data,
    load_mjo_daily,
    compute_mjo_monthly,
    get_combined_el_nino_data,
    DATA_DIR,
    MONTH_NAMES,
    SEASON_TO_MONTH,
)

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(BASE_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# ==============================================================================
# 2026 DATA UPDATE & MANUAL OVERRIDES
# ==============================================================================
# Instructions for updating 2026 data:
# 1. As new monthly ONI values are published by NOAA CPC, or if you want to test
#    forecast scenarios (e.g. for August-December 2026), enter them below:
#    Format: {month_number (1-12): oni_anomaly_in_celsius}
# 2. For MJO monthly mean amplitudes, enter:
#    Format: {month_number (1-12): mean_rmm_amplitude}
# 3. Setting a value here overrides or supplements the fetched data.
# ==============================================================================
UPDATE_2026_ONI: Dict[int, float] = {
    # 1: -0.39,  # Jan (DJF)
    # 2: -0.21,  # Feb (JFM)
    # 3:  0.11,  # Mar (FMA)
    # 4:  0.46,  # Apr (MAM)
    # 5:  0.95,  # May (AMJ)
    # 6:  1.39,  # Jun (MJJ)
    # 7:  1.80,  # Jul (JJA)
    # Add new or updated values below:
    # 8:  2.10,  # Aug (JAS)
}

UPDATE_2026_MJO: Dict[int, float] = {
    # 1: 1.57,  # Jan
    # 2: 1.00,  # Feb
    # 3: 1.06,  # Mar
    # 4: 1.71,  # Apr
    # 5: 1.37,  # May
    # 6: 1.50,  # Jun
    # 7: 1.66,  # Jul
    # 8: 0.99,  # Aug
    # 9: 0.85,  # Sep (partial through Sep 15)
    # Add new or updated values below:
}

# ==============================================================================
# COLORBLIND-SAFE PALETTE & VISUAL CONFIGURATION (Okabe-Ito Palette)
# ==============================================================================
EVENT_CONFIG = {
    1997: {
        "label": "1997 (Super El Niño)",
        "short_label": "1997",
        "color": "#D55E00",      # Vermillion / Red-Orange
        "marker": "o",
        "linestyle": "-",
        "linewidth": 2.0,
        "markersize": 6.5,
        "alpha": 0.95,
        "zorder": 4,
    },
    2006: {
        "label": "2006 (Moderate El Niño)",
        "short_label": "2006",
        "color": "#009E73",      # Bluish Green
        "marker": "D",
        "linestyle": "-",
        "linewidth": 2.0,
        "markersize": 5.5,
        "alpha": 0.95,
        "zorder": 5,
    },
    2015: {
        "label": "2015 (Super El Niño)",
        "short_label": "2015",
        "color": "#0072B2",      # Deep Blue
        "marker": "s",
        "linestyle": "-",
        "linewidth": 2.0,
        "markersize": 6.0,
        "alpha": 0.95,
        "zorder": 6,
    },
    2026: {
        "label": "2026 (Recent Event)",
        "short_label": "2026",
        "color": "#E69F00",      # Amber / Golden Orange
        "marker": "^",
        "linestyle": "-",
        "linewidth": 2.8,
        "markersize": 8.0,
        "alpha": 1.0,
        "zorder": 10,
    },
}


def setup_matplotlib_publication_style():
    """Configure matplotlib rcParams for journal submission (Nature / Science style)."""
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 8.5,
        "axes.labelsize": 9.5,
        "axes.labelweight": "bold",
        "axes.titlesize": 10.0,
        "axes.titleweight": "bold",
        "xtick.labelsize": 8.5,
        "ytick.labelsize": 8.5,
        "legend.fontsize": 8.0,
        "figure.titlesize": 11.0,
        "figure.titleweight": "bold",
        "axes.linewidth": 0.85,
        "lines.linewidth": 1.8,
        "xtick.major.size": 4.0,
        "xtick.major.width": 0.8,
        "ytick.major.size": 4.0,
        "ytick.major.width": 0.8,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.08,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })


def plot_figure1_monthly_comparison(
    combined_df: pd.DataFrame,
    mjo_daily_df: pd.DataFrame,
    target_years=(1997, 2006, 2015, 2026),
    output_prefix="figure1_major_el_nino_monthly_comparison",
):
    """
    Generate Figure 1: Aligned Jan-Dec Monthly Comparison across El Niño Years.
    Panel (a): Oceanic Niño Index (ONI, °C) with category bands.
    Panel (b): MJO Wheeler-Hendon RMM Mean Amplitude with SEM shading and daily spread.
    Panel (c): Active MJO Days per Month (Amp ≥ 1.0) and Maritime Continent (MC) convection days.
    """
    setup_matplotlib_publication_style()

    fig, axes = plt.subplots(
        nrows=3,
        ncols=1,
        figsize=(7.2, 8.8),
        sharex=True,
        gridspec_kw={"height_ratios": [1.1, 1.1, 1.05], "hspace": 0.22},
    )

    ax_oni, ax_mjo, ax_act = axes
    months = np.arange(1, 13)

    # --------------------------------------------------------------------------
    # Panel (a): Oceanic Niño Index (ONI)
    # --------------------------------------------------------------------------
    # Intensity category shading
    ax_oni.axhspan(2.0, 3.2, color="#B2182B", alpha=0.10, lw=0)      # Very Strong
    ax_oni.axhspan(1.5, 2.0, color="#E66101", alpha=0.10, lw=0)      # Strong
    ax_oni.axhspan(1.0, 1.5, color="#FDB863", alpha=0.10, lw=0)      # Moderate
    ax_oni.axhspan(0.5, 1.0, color="#FEE090", alpha=0.10, lw=0)      # Weak
    ax_oni.axhspan(-0.5, 0.5, color="#EAEAEA", alpha=0.15, lw=0)     # Neutral

    # Category labels on right spine via twinx (no overlap with data lines)
    ax_oni_cat = ax_oni.twinx()
    ax_oni_cat.set_ylim(-0.8, 3.1)
    ax_oni_cat.set_yticks([0.0, 0.75, 1.25, 1.75, 2.35])
    ax_oni_cat.set_yticklabels([
        "Neutral (±0.5°)",
        "Weak (0.5-1.0°)",
        "Moderate (1.0-1.5°)",
        "Strong (1.5-2.0°)",
        "Very Strong (>2.0°)",
    ], fontsize=6.8, style="italic")
    ax_oni_cat.tick_params(axis="y", length=0, pad=3)
    ax_oni_cat.spines["right"].set_visible(False)
    ax_oni_cat.spines["top"].set_visible(False)
    cat_colors = ["#555555", "#7F7F00", "#C26B00", "#A63603", "#800000"]
    for tick_label, col in zip(ax_oni_cat.get_yticklabels(), cat_colors):
        tick_label.set_color(col)

    # Reference lines
    ax_oni.axhline(0.0, color="#888888", linestyle="--", linewidth=0.8, alpha=0.7)
    ax_oni.axhline(0.5, color="#D95F02", linestyle=":", linewidth=0.9, alpha=0.8)

    for yr in target_years:
        sub = combined_df[combined_df["Year"] == yr].dropna(subset=["ONI_Anomaly"])
        cfg = EVENT_CONFIG.get(yr, {})
        color = cfg.get("color", "black")
        marker = cfg.get("marker", "o")
        lw = cfg.get("linewidth", 2.0)
        ms = cfg.get("markersize", 6.0)
        label = cfg.get("label", str(yr))
        zorder = cfg.get("zorder", 3)

        ax_oni.plot(
            sub["Month"],
            sub["ONI_Anomaly"],
            color=color,
            marker=marker,
            markersize=ms,
            linewidth=lw,
            label=label,
            zorder=zorder,
            clip_on=False,
        )

        if yr == 2026:
            ax_oni.plot(
                sub["Month"],
                sub["ONI_Anomaly"],
                color=color,
                marker=marker,
                markersize=ms,
                linewidth=lw,
                markeredgecolor="#111111",
                markeredgewidth=1.2,
                zorder=zorder + 1,
            )
            if len(sub) > 0:
                last_mo = sub["Month"].iloc[-1]
                last_val = sub["ONI_Anomaly"].iloc[-1]
                seas = sub["Season"].iloc[-1] if "Season" in sub else MONTH_NAMES[last_mo - 1]
                ax_oni.annotate(
                    f"2026 ({seas}: +{last_val:.2f}°C)",
                    xy=(last_mo, last_val),
                    xytext=(last_mo - 1.8, last_val + 0.36),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.2),
                    fontsize=7.5,
                    fontweight="bold",
                    color=color,
                    bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=color, lw=0.8, alpha=0.95),
                )

    ax_oni.set_ylabel("Oceanic Niño Index (°C)\n[3-Month SST Anomaly]")
    ax_oni.set_ylim(-0.8, 3.1)
    ax_oni.set_yticks([-0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
    ax_oni.yaxis.set_major_formatter(ticker.FormatStrFormatter("%+.1f"))
    ax_oni.text(-0.08, 1.03, "a", transform=ax_oni.transAxes, fontsize=11.5, fontweight="bold")
    ax_oni.legend(loc="upper left", frameon=True, framealpha=0.9, edgecolor="#CCCCCC", ncol=2)
    ax_oni.grid(True, axis="y", linestyle=":", alpha=0.5, color="#CCCCCC")

    # --------------------------------------------------------------------------
    # Panel (b): MJO Wheeler-Hendon RMM Monthly Mean Amplitude
    # --------------------------------------------------------------------------
    ax_mjo.axhspan(1.0, 3.6, color="#EBF4FB", alpha=0.5, lw=0)
    ax_mjo.axhline(1.0, color="#2B83BA", linestyle="--", linewidth=1.0, alpha=0.85)
    ax_mjo.text(0.65, 1.07, "Active MJO (≥ 1.0)", fontsize=7.2, color="#2B83BA", va="bottom", ha="left", style="italic")

    # Translucent daily amplitude spread
    for yr in [1997, 2015, 2026]:
        sub_daily = mjo_daily_df[mjo_daily_df["Year"] == yr]
        cfg = EVENT_CONFIG.get(yr, {})
        color = cfg.get("color", "black")
        jitter = (np.random.RandomState(yr).rand(len(sub_daily)) - 0.5) * 0.28
        ax_mjo.scatter(
            sub_daily["Month"] + jitter,
            sub_daily["Amplitude"],
            color=color,
            alpha=0.14,
            s=7,
            edgecolors="none",
            zorder=2,
        )

    # Monthly mean curves with SEM error band
    for yr in target_years:
        sub = combined_df[combined_df["Year"] == yr].dropna(subset=["Mean_Amplitude"])
        cfg = EVENT_CONFIG.get(yr, {})
        color = cfg.get("color", "black")
        marker = cfg.get("marker", "o")
        lw = cfg.get("linewidth", 2.0)
        ms = cfg.get("markersize", 6.0)
        zorder = cfg.get("zorder", 3)

        mo_vals = sub["Month"].values
        mean_vals = sub["Mean_Amplitude"].values
        sem_vals = sub["SEM_Amplitude"].values if "SEM_Amplitude" in sub else np.zeros_like(mean_vals)

        ax_mjo.fill_between(
            mo_vals,
            np.maximum(0, mean_vals - sem_vals),
            mean_vals + sem_vals,
            color=color,
            alpha=0.18,
            zorder=zorder - 1,
        )

        ax_mjo.plot(
            mo_vals,
            mean_vals,
            color=color,
            marker=marker,
            markersize=ms,
            linewidth=lw,
            zorder=zorder,
            clip_on=False,
        )

        if yr == 2026:
            ax_mjo.plot(
                mo_vals,
                mean_vals,
                color=color,
                marker=marker,
                markersize=ms,
                linewidth=lw,
                markeredgecolor="#111111",
                markeredgewidth=1.2,
                zorder=zorder + 1,
            )
            if len(mo_vals) > 0:
                last_mo = mo_vals[-1]
                last_amp = mean_vals[-1]
                ax_mjo.annotate(
                    f"2026 MJO ({last_amp:.2f})",
                    xy=(last_mo, last_amp),
                    xytext=(last_mo - 2.0, last_amp + 0.40),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.1),
                    fontsize=7.5,
                    fontweight="bold",
                    color=color,
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=color, lw=0.8, alpha=0.95),
                )

    ax_mjo.set_ylabel("MJO Amplitude\n[Wheeler-Hendon RMM (±1 SEM)]")
    ax_mjo.set_ylim(0.2, 3.5)
    ax_mjo.set_yticks([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5])
    ax_mjo.text(-0.08, 1.03, "b", transform=ax_mjo.transAxes, fontsize=11.5, fontweight="bold")
    ax_mjo.grid(True, axis="y", linestyle=":", alpha=0.5, color="#CCCCCC")

    sem_proxy = Patch(facecolor="#888888", edgecolor="none", alpha=0.25, label="±1 SEM")
    dot_proxy = Line2D([0], [0], marker="o", color="w", markerfacecolor="#888888", alpha=0.4, markersize=4, label="Daily RMM")
    ax_mjo.legend(handles=[sem_proxy, dot_proxy], loc="upper right", frameon=True, framealpha=0.9, edgecolor="#CCCCCC")

    # --------------------------------------------------------------------------
    # Panel (c): Active MJO Days per Month (Amp ≥ 1.0) & Maritime Continent Convection
    # --------------------------------------------------------------------------
    # Highlight Indonesian Fire Season (July - October) in background
    ax_act.axvspan(6.5, 10.5, color="#FDAE61", alpha=0.18, lw=0)
    ax_act.text(
        8.5, 34.5, "Indonesian Fire Season (JASO)",
        ha="center", fontsize=7.5, fontweight="bold", color="#A63603",
        bbox=dict(boxstyle="round,pad=0.25", fc="#FFF5EB", ec="#FDAE61", lw=0.8, alpha=0.95)
    )

    # Plot lines of active MJO days per month (Amp >= 1.0)
    for yr in target_years:
        sub = combined_df[combined_df["Year"] == yr].dropna(subset=["Active_Days"])
        cfg = EVENT_CONFIG.get(yr, {})
        color = cfg.get("color", "black")
        marker = cfg.get("marker", "o")
        lw = cfg.get("linewidth", 2.0)
        ms = cfg.get("markersize", 6.0)
        zorder = cfg.get("zorder", 3)

        mo_vals = sub["Month"].values
        act_days = sub["Active_Days"].values

        ax_act.plot(
            mo_vals,
            act_days,
            color=color,
            marker=marker,
            markersize=ms,
            linewidth=lw,
            label=f"{cfg.get('short_label', str(yr))}",
            zorder=zorder,
            clip_on=False,
        )

        if yr == 2026:
            ax_act.plot(
                mo_vals,
                act_days,
                color=color,
                marker=marker,
                markersize=ms,
                linewidth=lw,
                markeredgecolor="#111111",
                markeredgewidth=1.2,
                zorder=zorder + 1,
            )

    # Also plot Maritime Continent (MC Phases 4-5) active days as dashed lines with open symbols
    for yr in target_years:
        sub = combined_df[combined_df["Year"] == yr].dropna(subset=["MC_Phase45_Days"])
        cfg = EVENT_CONFIG.get(yr, {})
        color = cfg.get("color", "black")
        marker = cfg.get("marker", "o")
        zorder = cfg.get("zorder", 3)

        mo_vals = sub["Month"].values
        mc_days = sub["MC_Phase45_Days"].values

        ax_act.plot(
            mo_vals,
            mc_days,
            color=color,
            linestyle="--",
            marker=marker,
            markerfacecolor="white",
            markeredgecolor=color,
            markeredgewidth=1.4,
            markersize=ms * 0.85,
            linewidth=1.2,
            alpha=0.85,
            zorder=zorder - 1,
            clip_on=False,
        )

    ax_act.set_ylabel("Active MJO Days / Month\n[Amp ≥ 1.0 (Solid: All, Dash: MC)]")
    ax_act.set_ylim(-1, 38)
    ax_act.set_yticks([0, 5, 10, 15, 20, 25, 30, 35])
    ax_act.text(-0.08, 1.03, "c", transform=ax_act.transAxes, fontsize=11.5, fontweight="bold")
    ax_act.grid(True, axis="y", linestyle=":", alpha=0.5, color="#CCCCCC")

    # Unified clear legend (2 columns so it does not extend past month 5)
    leg_solid = Line2D([0], [0], color="#555555", lw=1.8, label="All MJO Phases")
    leg_dash = Line2D([0], [0], color="#555555", lw=1.2, ls="--", marker="o", mfc="w", mec="#555555", label="Maritime Continent (4-5)")
    handles, labels = ax_act.get_legend_handles_labels()
    handles.extend([leg_solid, leg_dash])
    ax_act.legend(handles=handles, loc="upper left", frameon=True, framealpha=0.9, edgecolor="#CCCCCC", ncol=2, fontsize=7.5)

    # X-axis configuration
    ax_act.set_xlim(0.5, 12.5)
    ax_act.set_xticks(months)
    ax_act.set_xticklabels(MONTH_NAMES)
    ax_act.set_xlabel("Calendar Month")

    fig.suptitle(
        "Evolution of ENSO (ONI) and MJO Intra-Seasonal Dynamics\nDuring Recent Major El Niño Years (1997, 2006, 2015, 2026)",
        fontsize=10.5,
        fontweight="bold",
        y=0.99,
    )

    pdf_path = os.path.join(FIG_DIR, f"{output_prefix}.pdf")
    png_path = os.path.join(FIG_DIR, f"{output_prefix}.png")
    fig.savefig(pdf_path)
    fig.savefig(png_path)
    plt.close(fig)
    logging.info(f"Figure 1 saved to:\n  {pdf_path}\n  {png_path}")
    return pdf_path, png_path


def plot_figure2_continuous_timeline(
    combined_df: pd.DataFrame,
    mjo_daily_df: pd.DataFrame,
    oni_full_df: pd.DataFrame,
    output_prefix="figure2_el_nino_multi_year_timeseries",
):
    """
    Generate Figure 2: Multi-event 24-month continuous timeline.
    Dual-axis plots for each major cross-year El Niño event:
      - (a) 1997-1998 Super El Niño
      - (b) 2006-2007 El Niño
      - (c) 2015-2016 Super El Niño
      - (d) 2026-2027 Major El Niño (Left half: 2026 Year 0, Right half: 2027 Year +1)
    Left Axis (Red/Orange): Oceanic Niño Index (ONI, °C)
    Right Axis (Blue): MJO Daily Amplitude (light area) and Monthly Mean (points/line)
    """
    setup_matplotlib_publication_style()

    events = [
        ("1997–1998 Super El Niño", 1997, 1998),
        ("2006–2007 El Niño", 2006, 2007),
        ("2015–2016 Super El Niño", 2015, 2016),
        ("2026–2027 Major El Niño", 2026, 2027),
    ]

    fig, axes = plt.subplots(
        nrows=4,
        ncols=1,
        figsize=(7.4, 9.6),
        sharey=False,
        gridspec_kw={"hspace": 0.32},
    )

    panel_letters = ["a", "b", "c", "d"]

    for idx, (title, y0, y1) in enumerate(events):
        ax_left = axes[idx]
        ax_right = ax_left.twinx()

        start_date = pd.Timestamp(f"{y0}-01-01")
        end_date = pd.Timestamp(f"{y1}-12-31")

        # Vertical divider between Year 0 (left half) and Year +1 (right half)
        mid_date = pd.Timestamp(f"{y0}-12-31 12:00:00")
        ax_left.axvline(mid_date, color="#BBBBBB", linestyle="--", linewidth=0.8, alpha=0.7, zorder=1)

        mjo_sub = mjo_daily_df[
            (mjo_daily_df["Year"] >= y0) & (mjo_daily_df["Year"] <= y1)
        ].copy()
        if len(mjo_sub) > 0:
            mjo_sub["Date"] = pd.to_datetime(mjo_sub[["Year", "Month", "Day"]])
            mjo_sub.sort_values("Date", inplace=True)

        oni_sub = oni_full_df[
            (oni_full_df["Year"] >= y0) & (oni_full_df["Year"] <= y1)
        ].copy()
        if len(oni_sub) > 0:
            oni_sub["Day"] = 15
            oni_sub["Date"] = pd.to_datetime(oni_sub[["Year", "Month", "Day"]])
            oni_sub.sort_values("Date", inplace=True)

        ax_right.axhline(1.0, color="#56B4E9", linestyle=":", linewidth=0.8, alpha=0.7)

        # Right Axis: MJO Daily amplitude (area + thin line)
        if len(mjo_sub) > 0:
            ax_right.fill_between(
                mjo_sub["Date"],
                0,
                mjo_sub["Amplitude"],
                color="#0072B2",
                alpha=0.12,
                label="MJO Daily Amp",
            )
            ax_right.plot(
                mjo_sub["Date"],
                mjo_sub["Amplitude"],
                color="#0072B2",
                linewidth=0.6,
                alpha=0.45,
            )

        # Right Axis: MJO Monthly mean
        mjo_m_sub = combined_df[
            (combined_df["Year"] >= y0) & (combined_df["Year"] <= y1)
        ].dropna(subset=["Mean_Amplitude"]).copy()
        if len(mjo_m_sub) > 0:
            mjo_m_sub["Day"] = 15
            mjo_m_sub["Date"] = pd.to_datetime(mjo_m_sub[["Year", "Month", "Day"]])
            ax_right.plot(
                mjo_m_sub["Date"],
                mjo_m_sub["Mean_Amplitude"],
                color="#0072B2",
                marker="o",
                markersize=4.5,
                linewidth=1.8,
                label="MJO Monthly Mean",
                zorder=5,
            )

        # Left Axis: ONI 3-month running SST anomaly
        if len(oni_sub) > 0:
            ax_left.axhline(0.0, color="#666666", linestyle="-", linewidth=0.7, alpha=0.6)
            ax_left.axhline(0.5, color="#D55E00", linestyle="--", linewidth=0.8, alpha=0.7)

            ax_left.fill_between(
                oni_sub["Date"],
                0,
                oni_sub["ONI_Anomaly"],
                where=(oni_sub["ONI_Anomaly"] >= 0),
                color="#D55E00",
                alpha=0.25,
                interpolate=True,
            )
            ax_left.fill_between(
                oni_sub["Date"],
                0,
                oni_sub["ONI_Anomaly"],
                where=(oni_sub["ONI_Anomaly"] < 0),
                color="#0072B2",
                alpha=0.15,
                interpolate=True,
            )
            ax_left.plot(
                oni_sub["Date"],
                oni_sub["ONI_Anomaly"],
                color="#D55E00",
                marker="s",
                markersize=4.5,
                linewidth=2.2,
                label="ONI (°C)",
                zorder=6,
            )

        ax_left.set_ylim(-1.8, 3.0)
        ax_left.set_yticks([-1.0, 0.0, 1.0, 2.0, 3.0])
        ax_left.set_ylabel("ONI (°C)", color="#D55E00", fontweight="bold")
        ax_left.tick_params(axis="y", labelcolor="#D55E00")

        ax_right.set_ylim(0, 4.2)
        ax_right.set_yticks([0, 1.0, 2.0, 3.0, 4.0])
        ax_right.set_ylabel("MJO Amp", color="#0072B2", fontweight="bold")
        ax_right.tick_params(axis="y", labelcolor="#0072B2")
        ax_right.spines["right"].set_visible(True)
        ax_right.spines["right"].set_color("#0072B2")
        ax_left.spines["left"].set_color("#D55E00")

        ax_left.set_xlim(start_date, end_date)
        quarter_dates = pd.date_range(start=f"{y0}-01-01", end=f"{y1}-12-31", freq="3MS")
        ax_left.set_xticks(quarter_dates)
        ax_left.set_xticklabels([d.strftime("%b %y") for d in quarter_dates], rotation=0, ha="center")

        ax_left.set_title(f"{title}", loc="left", fontsize=9.5, fontweight="bold", pad=4)
        ax_left.text(-0.08, 1.05, panel_letters[idx], transform=ax_left.transAxes, fontsize=11, fontweight="bold")
        ax_left.grid(True, axis="x", linestyle=":", alpha=0.4, color="#CCCCCC")

        # Subtle Year 0 / Year +1 label indicator on panel a
        if idx == 0:
            ax_left.text(pd.Timestamp(f"{y0}-06-15"), 2.65, "Year 0 (Developing)", ha="center", fontsize=7.2, color="#555555", style="italic")
            ax_left.text(pd.Timestamp(f"{y1}-06-15"), 2.65, "Year +1 (Decaying)", ha="center", fontsize=7.2, color="#555555", style="italic")
            h_oni = Line2D([0], [0], color="#D55E00", marker="s", markersize=4.5, lw=2.2, label="ONI (°C)")
            h_mjo_m = Line2D([0], [0], color="#0072B2", marker="o", markersize=4.5, lw=1.8, label="MJO Monthly Mean")
            h_mjo_d = Patch(facecolor="#0072B2", alpha=0.2, label="MJO Daily Amp")
            ax_left.legend(
                handles=[h_oni, h_mjo_m, h_mjo_d],
                loc="upper right",
                frameon=True,
                framealpha=0.9,
                edgecolor="#CCCCCC",
                ncol=3,
                fontsize=7.5,
            )

    fig.suptitle(
        "Continuous 24-Month Trajectories of ENSO (ONI) & Intra-Seasonal MJO\nAcross Major Cross-Year El Niño Events (1997–98, 2006–07, 2015–16, 2026–27)",
        fontsize=10.5,
        fontweight="bold",
        y=0.995,
    )

    pdf_path = os.path.join(FIG_DIR, f"{output_prefix}.pdf")
    png_path = os.path.join(FIG_DIR, f"{output_prefix}.png")
    fig.savefig(pdf_path)
    fig.savefig(png_path)
    plt.close(fig)
    logging.info(f"Figure 2 saved to:\n  {pdf_path}\n  {png_path}")
    return pdf_path, png_path


def plot_figure3_fire_season_mjo_phases(
    mjo_daily_df: pd.DataFrame,
    target_years=(1997, 2006, 2015, 2026),
    output_prefix="figure3_fire_season_mjo_phase_distribution",
):
    """
    Generate Figure 3: MJO Phase distribution during the peak Indonesian Fire Season (July–October, JASO).
    Highlights why Indonesian fires surge when MJO convection is suppressed over Maritime Continent (Phases 4-5)
    and displaced eastward to Western Pacific (Phases 6-7).
    """
    setup_matplotlib_publication_style()

    fig, ax = plt.subplots(figsize=(7.2, 4.2))

    phases = np.arange(1, 9)
    width = 0.18
    offsets = {1997: -1.5 * width, 2006: -0.5 * width, 2015: 0.5 * width, 2026: 1.5 * width}

    # Highlight Maritime Continent Phases 4 & 5 (rain enhancer in Indonesia)
    ax.axvspan(3.5, 5.5, color="#56B4E9", alpha=0.15, label=None, lw=0)
    ax.text(
        4.5, 18.0, "Maritime Continent (4-5)\n[Convection Suppressed]",
        ha="center", fontsize=7.2, fontweight="bold", color="#0072B2",
        bbox=dict(boxstyle="round,pad=0.25", fc="#F0F8FF", ec="#56B4E9", lw=0.8, alpha=0.95)
    )

    # Highlight Western Pacific Phases 6 & 7 (displaced convection away from Indonesia)
    ax.axvspan(5.5, 7.5, color="#FDAE61", alpha=0.15, label=None, lw=0)
    ax.text(
        6.5, 25.0, "Western Pacific (6-7)\n[Displaced Convection]",
        ha="center", fontsize=7.2, fontweight="bold", color="#D95F02",
        bbox=dict(boxstyle="round,pad=0.25", fc="#FFF5EB", ec="#FDAE61", lw=0.8, alpha=0.95)
    )

    for yr in target_years:
        sub = mjo_daily_df[(mjo_daily_df["Year"] == yr) & (mjo_daily_df["Month"].isin([7, 8, 9, 10]))]
        sub_act = sub[sub["Amplitude"] >= 1.0]
        cfg = EVENT_CONFIG.get(yr, {})
        color = cfg.get("color", "black")
        label = cfg.get("label", str(yr))

        counts = sub_act["Phase"].value_counts()
        phase_days = [counts.get(p, 0) for p in phases]

        note_str = " (through mid-Sep)" if yr == 2026 else ""
        ax.bar(
            phases + offsets[yr],
            phase_days,
            width=width,
            color=color,
            alpha=0.9,
            edgecolor="#222222" if yr == 2026 else "none",
            linewidth=1.0 if yr == 2026 else 0.0,
            label=f"{label}{note_str}",
            zorder=3,
        )

    ax.set_xticks(phases)
    ax.set_xticklabels([
        "Phase 1\n(W. Hem)",
        "Phase 2\n(Ind. Ocean)",
        "Phase 3\n(Ind. Ocean)",
        "Phase 4\n(Maritime C.)",
        "Phase 5\n(Maritime C.)",
        "Phase 6\n(W. Pacific)",
        "Phase 7\n(W. Pacific)",
        "Phase 8\n(W. Hem)",
    ], fontsize=7.2)

    ax.set_ylabel("Active MJO Days (Amp ≥ 1.0)\n[July–October Peak Fire Season]")
    ax.set_ylim(0, 30)
    ax.set_yticks([0, 5, 10, 15, 20, 25, 30])
    ax.legend(loc="upper left", frameon=True, framealpha=0.92, edgecolor="#CCCCCC", ncol=1, fontsize=7.5)
    ax.grid(True, axis="y", linestyle=":", alpha=0.5, color="#CCCCCC")

    fig.suptitle(
        "MJO Convective Phase Distribution during Peak Indonesian Fire Season (July–October)\nAcross Major El Niño Years (1997, 2006, 2015, 2026)",
        fontsize=10.0,
        fontweight="bold",
        y=0.99,
    )

    pdf_path = os.path.join(FIG_DIR, f"{output_prefix}.pdf")
    png_path = os.path.join(FIG_DIR, f"{output_prefix}.png")
    fig.savefig(pdf_path)
    fig.savefig(png_path)
    plt.close(fig)
    logging.info(f"Figure 3 saved to:\n  {pdf_path}\n  {png_path}")
    return pdf_path, png_path


def generate_all_figures(
    override_oni=None,
    override_mjo=None,
    force_download=False,
):
    """Load data, apply overrides for 2026, and render all publication figures."""
    logging.info("Step 1: Loading ONI and MJO records...")
    oni_df = load_oni_data(force_download=force_download)
    mjo_daily_df = load_mjo_daily(force_download=force_download)
    mjo_monthly_df = compute_mjo_monthly(mjo_daily_df)

    # Merge overrides from top-level config with function arguments
    effective_oni_override = dict(UPDATE_2026_ONI)
    if override_oni:
        effective_oni_override.update(override_oni)

    effective_mjo_override = dict(UPDATE_2026_MJO)
    if override_mjo:
        effective_mjo_override.update(override_mjo)

    if effective_oni_override:
        logging.info(f"Applying 2026 ONI overrides: {effective_oni_override}")
    if effective_mjo_override:
        logging.info(f"Applying 2026 MJO overrides: {effective_mjo_override}")

    logging.info("Step 2: Combining target El Niño data (1997-1998, 2006-2007, 2015-2016, 2026-2027)...")
    target_years = (1997, 2006, 2015, 2026)
    combined_years = (1997, 1998, 2006, 2007, 2015, 2016, 2026, 2027)
    combined_df = get_combined_el_nino_data(
        oni_df,
        mjo_monthly_df,
        target_years=combined_years,
        override_2026_oni=effective_oni_override,
        override_2026_mjo=effective_mjo_override,
    )

    logging.info("Step 3: Rendering Figure 1 (Aligned Annual Evolution Comparison)...")
    fig1_pdf, fig1_png = plot_figure1_monthly_comparison(combined_df, mjo_daily_df, target_years=target_years)

    logging.info("Step 4: Rendering Figure 2 (Continuous 24-Month Event Timelines)...")
    fig2_pdf, fig2_png = plot_figure2_continuous_timeline(combined_df, mjo_daily_df, oni_df)

    logging.info("Step 5: Rendering Figure 3 (JASO Fire Season MJO Phase Distribution)...")
    fig3_pdf, fig3_png = plot_figure3_fire_season_mjo_phases(mjo_daily_df, target_years=target_years)

    logging.info("All publication figures successfully created!")
    return {
        "fig1_pdf": fig1_pdf,
        "fig1_png": fig1_png,
        "fig2_pdf": fig2_pdf,
        "fig2_png": fig2_png,
        "fig3_pdf": fig3_pdf,
        "fig3_png": fig3_png,
    }


def parse_override_arg(arg_str: str) -> Dict[int, float]:
    """Parse key-value override strings, e.g. '8=2.10,9=2.25' -> {8: 2.10, 9: 2.25}"""
    res = {}
    if not arg_str:
        return res
    for item in arg_str.split(","):
        if "=" in item:
            k, v = item.split("=", 1)
            try:
                res[int(k.strip())] = float(v.strip())
            except ValueError:
                logging.warning(f"Could not parse override token '{item}'")
    return res


def main():
    parser = argparse.ArgumentParser(
        description="Plot publication-quality ONI and MJO time series for major El Niño years."
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Force re-downloading latest data from NOAA CPC and BOM servers.",
    )
    parser.add_argument(
        "--update-oni",
        type=str,
        default="",
        help="Override/supplement 2026 ONI values, e.g. '8=2.05,9=2.25'.",
    )
    parser.add_argument(
        "--update-mjo",
        type=str,
        default="",
        help="Override/supplement 2026 MJO amplitude values, e.g. '8=1.12,9=0.95'.",
    )
    args = parser.parse_args()

    override_oni = parse_override_arg(args.update_oni)
    override_mjo = parse_override_arg(args.update_mjo)

    generate_all_figures(
        override_oni=override_oni,
        override_mjo=override_mjo,
        force_download=args.refresh,
    )


if __name__ == "__main__":
    main()
