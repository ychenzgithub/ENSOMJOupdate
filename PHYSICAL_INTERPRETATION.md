# Physical and Meteorological Interpretation of ENSO and MJO Figures

This document provides an in-depth scientific interpretation of the three publication figures generated in this repository ([figure1_major_el_nino_monthly_comparison.png](./figures/figure1_major_el_nino_monthly_comparison.png), [figure2_el_nino_multi_year_timeseries.png](./figures/figure2_el_nino_multi_year_timeseries.png), and [figure3_fire_season_mjo_phase_distribution.png](./figures/figure3_fire_season_mjo_phase_distribution.png)).

These figures analyze the multi-scale climate drivers governing Indonesian drought and catastrophic peatland fire risk, comparing the developing **2026 El Niño** with primary historical benchmark events (**1997**, **2006**, and **2015**).

---

## 1. Scientific Background & Theoretical Framework

### 1.1 Macro-Scale Driver: The Walker Circulation & ENSO
Indonesian precipitation and drought vulnerability are primarily dictated by the **Indo-Pacific Walker Circulation**:
* Under **Neutral / La Niña** conditions, warm sea surface temperatures (SST) in the Indo-Pacific Warm Pool drive strong atmospheric convection and heavy rainfall over the Maritime Continent (Indonesia, Malaysia, Papua New Guinea).
* During an **El Niño event** (positive Oceanic Niño Index, ONI), anomalously warm waters expand into the central and eastern equatorial Pacific ($5^\circ\text{N}–5^\circ\text{S}, 170^\circ\text{W}–120^\circ\text{W}$). This shifts the ascending convective branch eastward, replacing the normal upward motion over Indonesia with persistent, large-scale **atmospheric subsidence (sinking dry air)**.
* In Indonesian peatland ecosystems (Central Kalimantan, South Sumatra, Riau, and Papua), prolonged subsidence during the dry season (July–October, JASO) lowers the water table below the critical threshold (typically $\approx 40\text{ cm}$ below the surface), causing deep peat desiccation and highly flammable conditions.

### 1.2 Subseasonal Driver: The Madden–Julian Oscillation (MJO)
While ENSO sets the interannual background dryness, the intra-seasonal timing and severity of fire outbreaks are modulated by the **Madden–Julian Oscillation (MJO)**—a 30–60 day eastward-propagating envelope of tropical convective activity:
* **Maritime Continent Wetting (Phases 4 & 5):** When the MJO convective center tracks across Indonesia, strong low-level moisture convergence and anomalous upward motion bring widespread convective rainfall. These wetting pulses act as a natural fire-suppression mechanism, raising peat water tables and extinguishing surface ignitions even against an El Niño background.
* **Subsidence & Drought Amplification (Phases 6–8 & 1–3):** When the convective core migrates into the Western Pacific (Phases 6 & 7) or Western Hemisphere (Phase 8), the descending (subsiding) limb of the MJO wave settles directly over Indonesia. This clears cloud cover, intensifies solar insolation, drops relative humidity, and severely exacerbates peat burning.
* **Kelvin Wave Seeding (Spring Phase):** In early spring of Year 0, intense MJO events in the Western Pacific produce low-level westerly wind bursts (WWBs) along the equator. These WWBs collapse trade winds and trigger downwelling oceanic Kelvin waves that kick off the El Niño warming cycle (Bjerknes positive feedback).

---

## 2. Detailed Interpretation of Figures

### Figure 1: Aligned Annual Evolution Comparison
* **File:** [figure1_major_el_nino_monthly_comparison.png](./figures/figure1_major_el_nino_monthly_comparison.png) ([Vector PDF](./figures/figure1_major_el_nino_monthly_comparison.pdf))
* **Layout:** Three vertically aligned panels from January to December across 1997, 2006, 2015, and 2026.

```
Panel a: Oceanic Niño Index (ONI, °C)         → Macro-scale background drought forcing
Panel b: MJO Amplitude (Wheeler-Hendon RMM)    → Intra-seasonal wave energy & wind bursts
Panel c: Active Days (Total vs. Maritime Cont) → Episodic fire-quenching rainfall vs. suppression
```

#### Panel a: Oceanic Niño Index (ONI, °C)
* **What is plotted:** The 3-month running mean of ERSSTv5 sea surface temperature anomalies in the Niño 3.4 region, overlaid on NOAA categorical intensity zones (Neutral: $\pm 0.5^\circ\text{C}$, Weak: $0.5–1.0^\circ\text{C}$, Moderate: $1.0–1.5^\circ\text{C}$, Strong: $1.5–2.0^\circ\text{C}$, Very Strong / Super: $>2.0^\circ\text{C}$).
* **Physical Insights:**
  * **1997 & 2015 Super El Niños:** Both events exhibited an explosive warming rate in boreal spring, crossing the $+1.0^\circ\text{C}$ threshold by May/June and surpassing $+1.5^\circ\text{C}$ to $+2.0^\circ\text{C}$ heading into July–August. Both culminated in historic peatland burning episodes.
  * **2006 Moderate El Niño:** Warming was delayed, crossing into weak El Niño territory ($+0.5^\circ\text{C}$) only in late summer (August). However, severe fires still occurred due to strong coupling with a concurrent positive Indian Ocean Dipole (+IOD).
  * **2026 Developing Trajectory:** 2026 began neutral in winter ($-0.39^\circ\text{C}$ in Jan, $+0.11^\circ\text{C}$ in Mar) and underwent rapid intensification through spring and summer: $+0.95^\circ\text{C}$ in May (AMJ), $+1.39^\circ\text{C}$ in June (MJJ), and reaching **$+1.80^\circ\text{C}$ in July (JJA)**. The onset slope of 2026 directly matches the growth rate of the 1997 and 2015 benchmark disasters.

#### Panel b: MJO Wheeler–Hendon RMM Amplitude ($\pm 1\text{ SEM}$)
* **What is plotted:** Intraseasonal convective amplitude ($\sqrt{\text{RMM1}^2 + \text{RMM2}^2}$). The dashed blue horizontal line at $1.0$ separates weak/disorganized tropical convection ($<1.0$) from coherent, active MJO episodes ($\ge 1.0$). Semi-transparent dots show daily values, while curves and shaded bands show monthly means $\pm 1$ standard error of the mean (SEM).
* **Physical Insights:**
  * **Spring Kelvin Wave Forcing:** High MJO amplitude peaks occurred during early spring in 1997 (March amplitude $>3.1$), 2015 (March amplitude $>2.5$), and 2026 (April amplitude $\approx 1.7$, July amplitude $\approx 1.66$). These energetic spring pulses provided the atmospheric momentum kicks (westerly wind bursts) that initiated eastern Pacific thermocline depression.
  * **Summer Amplitude Behavior:** During the critical Indonesian dry season (August–September), mean MJO amplitude in 2026 dipped toward $0.85–0.99$. In late 1997 and late 2015, average amplitude also subsided to near $0.7–1.0$, illustrating how background warm-pool expansion during mature El Niño episodes disrupts standard equatorial MJO propagation.

#### Panel c: Active MJO Days vs. Maritime Continent Convective Days
* **What is plotted:** Solid lines show total active MJO days per month ($\text{Amp} \ge 1.0$). Dashed lines with open markers denote active days specifically in **Phases 4 & 5** (Maritime Continent). The orange shaded vertical band marks the peak Indonesian fire season (**July to October, JASO**).
* **Physical Insights & Fire Danger Mechanism:**
  * **The Absence of Wetting Pulses:** In a normal year, episodic MJO passages through Phases 4 & 5 bring 5–15 days of wetting storms each month, raising peat water tables.
  * In **1997**, Phase 4–5 days plummeted to near zero in August and September.
  * In **2015**, Phase 4–5 days were **zero throughout July–October**, leaving the desiccation process completely unchecked and producing the catastrophic Southeast Asian haze crisis.
  * In **2026**, Phase 4–5 convective days dropped to **0 days in August and 0 days in September**, replicating the dangerous intraseasonal drought lock of 1997 and 2015.

---

### Figure 2: Continuous 24-Month Event Trajectories
* **File:** [figure2_el_nino_multi_year_timeseries.png](./figures/figure2_el_nino_multi_year_timeseries.png) ([Vector PDF](./figures/figure2_el_nino_multi_year_timeseries.pdf))
* **Layout:** Four continuous 24-month dual-axis panels spanning Year 0 (developing/peak year, left half) to Year +1 (decay/transition year, right half):
  - **(a)** 1997–1998 Super El Niño
  - **(b)** 2006–2007 El Niño
  - **(c)** 2015–2016 Super El Niño
  - **(d)** 2026–2027 Developing / Major El Niño

```
Left Axis (Red/Orange): Oceanic Niño Index (ONI, °C)  → Low-frequency ocean thermal inertia
Right Axis (Blue):      Daily & Monthly MJO Amplitude  → High-frequency atmospheric intraseasonal energy
```

#### Physical Insights:
1. **Timescale Separation & Coupled Feedbacks:**
   * The slowly evolving, filled red ONI curve represents the immense **heat content and thermal inertia** of the upper equatorial Pacific Ocean ($1–2$ year lifecycle).
   * The high-frequency blue envelope depicts the rapid **subseasonal atmospheric variability** ($30–60$ day lifecycle).
   * The juxtaposition highlights how short-duration intraseasonal wind events in early Year 0 trigger multi-year ocean-atmosphere reorganizations.
2. **Seasonal Phase Locking & Asymmetric Decay:**
   * Major El Niño events peak near the end of Year 0 / beginning of Year +1 (November–January, centered at the vertical dashed line).
   * During Year +1, strong events collapse rapidly: the 1997–98 event decayed abruptly from $+2.4^\circ\text{C}$ in late 1997 to negative ONI values (La Niña) by mid-1998 (blue shading below $0^\circ\text{C}$).
3. **MJO Suppression at ENSO Peak:**
   * In panels (a) and (c), as ONI exceeds $+2.0^\circ\text{C}$ in autumn/winter of Year 0, monthly mean MJO amplitude frequently drops below $1.0$. The massive eastward shift of convective heating reorganizes global planetary waves and suppresses canonical MJO propagation across the Maritime Continent.
4. **Current Status of the 2026–2027 Cycle:**
   * Panel (d) shows 2026 tracking through Year 0. The ONI curve is climbing monotonically past $+1.8^\circ\text{C}$ by mid-summer, demonstrating that 2026 is an established major El Niño heading toward an anticipated mature peak at the turn of the year.

---

### Figure 3: Peak Fire Season MJO Phase Breakdown
* **File:** [figure3_fire_season_mjo_phase_distribution.png](./figures/figure3_fire_season_mjo_phase_distribution.png) ([Vector PDF](./figures/figure3_fire_season_mjo_phase_distribution.pdf))
* **Layout:** Bar chart displaying the frequency distribution of active MJO days ($\text{Amp} \ge 1.0$) across all 8 Wheeler–Hendon phases during the peak Indonesian fire season (**July to October, JASO**).

```
Phase 1:        Western Hemisphere / Africa
Phases 2 & 3:   Indian Ocean
Phases 4 & 5:   MARITIME CONTINENT  → [Blue Shading: Direct convective wetting over Indonesia]
Phases 6 & 7:   WESTERN PACIFIC      → [Orange Shading: Convective ascent shifted east; subsidence over Indonesia]
Phase 8:        Western Hemisphere
```

#### Physical Insights & Regional Circulation:
1. **The Phase 4–5 "Wetting Deficit":**
   * Phases 4 & 5 represent the active convective phase over Indonesia.
   * In **2015 (Super El Niño)**, there were **0 active days** in Phase 4 and **0 active days** in Phase 5 throughout the entire 4-month fire season. The complete absence of wetting storms led to the desiccation of over $2.6\text{ million hectares}$ of peatlands and forests.
   * In **2026 (Recent Event)**, through mid-September, there have also been **0 active days** in both Phase 4 and Phase 5 during the fire season.
2. **The Phase 6–7 "Subsidence Trap":**
   * When MJO convection shifts to the Western Pacific (Phases 6 and 7, centered at $120^\circ\text{E}–160^\circ\text{E}$), the ascending limb is located east of Indonesia.
   * Consequently, the strong, dry **subsiding limb** of the MJO cell is positioned directly over Sumatra, Kalimantan, and the Java Sea. This clears cloud cover, maximizes daytime solar heating, lowers surface relative humidity, and accelerates peat fuel drying.
   * In **2026**, active MJO days are concentrated in **Phase 6 (14 days)**, **Phase 7 (21 days)**, and **Phase 8 (18 days)**.
   * Rather than offsetting the El Niño drought, intraseasonal MJO dynamics in 2026 have actively exacerbated drought conditions by remaining trapped in subsidence-inducing phases.

---

## 3. Comparative Summary Across Benchmark Events

| Diagnostic Feature | 1997–98 Benchmark | 2006–07 Benchmark | 2015–16 Benchmark | 2026–27 Event |
| :--- | :--- | :--- | :--- | :--- |
| **ENSO Classification** | Super El Niño | Moderate El Niño | Super El Niño | Major / Strong El Niño |
| **Peak ONI Anomaly** | $+2.4^\circ\text{C}$ (NDJ 1997) | $+1.0^\circ\text{C}$ (OND 2006) | $+2.6^\circ\text{C}$ (NDJ 2015) | $+1.80^\circ\text{C}$ (JJA 2026, rising) |
| **Spring WWB / MJO Forcing** | Extreme (Mar Amp $>3.1$) | Weak–Moderate | Strong (Mar Amp $>2.5$) | Strong (Apr Amp $\approx 1.7$) |
| **Fire Season MJO (Phases 4–5)** | Strongly suppressed in Aug–Sep | Present (sporadic) | **0 days** (entire JASO) | **0 days** (through mid-Sep) |
| **Fire Season MJO (Phases 6–8)** | Present | Moderate | High (Phases 6–7) | **Extremely high** (53 total days) |
| **Indonesian Fire Consequence** | Historic disaster; widespread burning | Severe emissions (amplified by +IOD) | Worst fire disaster since 1997 | **High compound risk**: severe drying + subsidence trap |

---

## 4. Key Takeaways for 2026 Peatland Fire Risk

1. **Compound Hazard Mechanism:** 2026 is experiencing an alignment of two major drought drivers:
   - *Interannual background:* A rapidly intensifying El Niño ($+1.80^\circ\text{C}$ by July) causing broad-scale Walker circulation breakdown.
   - *Intraseasonal circulation:* An MJO wave that has completely bypassed Maritime Continent wetting phases (Phases 4–5) and remained trapped in Western Pacific subsidence phases (Phases 6–7 and Phase 8).
2. **Peat Hydrology Impact:** Without episodic Phase 4–5 rainfall to interrupt the dry season, groundwater table drawdowns in drained peatlands accelerate rapidly, leading to high fuel flammability and elevated risks of deep, smoldering underground peat fires.
3. **Forecasting & Monitoring Utility:** Monitoring daily MJO phase transitions in late September and October provides a critical $1–3$ week early warning window for whether monsoonal rains will arrive on schedule or if fire suppression operations will need to be extended.

---

## 5. References
1. **Wheeler, M. C., & Hendon, H. H. (2004).** An all-season real-time multivariate MJO index: Development of an index for monitoring and prediction. *Monthly Weather Review*, 132(8), 1917–1932.
2. **Field, R. D., & Shen, S. S. (2008).** Predictability of Indonesian fire activity using antecedent rainfall. *Atmospheric Chemistry and Physics*, 8(8), 2269–2280.
3. **Reid, J. S., et al. (2012).** Relationships between national-scale fire emissions, regional emissions, and large-scale meteorology in Maritime Continent. *Atmospheric Chemistry and Physics*, 12(22), 10807–10832.
4. **Huang, B., et al. (2017).** Extended Reconstructed Sea Surface Temperature, Version 5 (ERSSTv5): Upgrades, validations, and intercomparisons. *Journal of Climate*, 30(20), 8179–8205.
