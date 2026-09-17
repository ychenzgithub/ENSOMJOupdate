#!/usr/bin/env python3
"""
test_update_2026.py
===================
Demonstration script showing how easy it is to update or test hypothetical/forecast
2026 ONI and MJO values programmatically or via CLI.
"""

from plot_enso_mjo_timeseries import generate_all_figures

print("=== Demonstration: Updating 2026 ONI & MJO Data ===")
print("Suppose new NOAA ONI values are published for August and September 2026,")
print("and MJO observations/forecasts are added.")

# Example updates for late 2026:
new_2026_oni = {
    8: 2.15,  # August 2026 (JAS)
    9: 2.38,  # September 2026 (ASO)
}

new_2026_mjo = {
    8: 0.99,  # August 2026
    9: 1.15,  # September 2026 (full month)
    10: 1.35, # October 2026
}

print(f"Updating 2026 ONI: {new_2026_oni}")
print(f"Updating 2026 MJO: {new_2026_mjo}")

# Run figure generation with custom updates
figures = generate_all_figures(
    override_oni=new_2026_oni,
    override_mjo=new_2026_mjo,
    force_download=False,
)

print("\nFigures regenerated successfully with updated 2026 values:")
for fig_key, path in figures.items():
    print(f"  {fig_key}: {path}")
