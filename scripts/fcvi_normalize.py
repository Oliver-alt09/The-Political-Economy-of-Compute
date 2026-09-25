"""
01_fcvi_normalize.py

Reproduces the two populated FCVI dimensions reported in Section 7.3
of "The Political Economy of Compute":
  - Security (S): OECD FDI Regulatory Restrictiveness Index, 2024 vintage
  - Compute (C): TOP500 list, June 2026, Rmax share by country

Normalization follows the paper's own stated rule exactly:
    z_ij = (x_ij - min_j(x_j)) / (max_j(x_j) - min_j(x_j))
    v_ij = z_ij       if a larger raw value means greater VULNERABILITY
    v_ij = 1 - z_ij   if a larger raw value means greater CAPACITY

Run:  python3 01_fcvi_normalize.py
Requires: pandas, openpyxl, xlrd (for the .xls file)
"""

import pandas as pd
import json

DATA_DIR = "../data"

EU27_OECD_CODES = [
    "AUT", "BEL", "BGR", "HRV", "CZE", "DNK", "EST", "FIN", "FRA", "DEU",
    "GRC", "HUN", "IRL", "ITA", "LVA", "LTU", "LUX", "NLD", "POL", "PRT",
    "ROU", "SVK", "SVN", "ESP", "SWE",
]  # Malta and Cyprus are not covered by the FDIRRI (per OECD documentation)

EU27_TOP500_NAMES = [
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech Republic",
    "Czechia", "Denmark", "Estonia", "Finland", "France", "Germany",
    "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania",
    "Luxembourg", "Malta", "Netherlands", "Poland", "Portugal", "Romania",
    "Slovakia", "Slovenia", "Spain", "Sweden",
]


def normalize(value, vmin, vmax):
    return (value - vmin) / (vmax - vmin)


def security_dimension():
    """Compute the Security (S) dimension from the real OECD FDIRRI CSV."""
    df = pd.read_csv(f"{DATA_DIR}/oecd_fdirri_2024.csv")
    total = df[df["POL_CAT"] == "_T"].set_index("REF_AREA")["OBS_VALUE"]

    present_eu = [c for c in EU27_OECD_CODES if c in total.index]
    eu_avg = total.loc[present_eu].mean()

    raw = {
        "United States": total["USA"],
        "China": total["CHN"],
        "India": total["IND"],
        "European Union": eu_avg,
    }
    vmin, vmax = min(raw.values()), max(raw.values())

    # Higher FDIRRI score = more restrictive = greater vulnerability -> v = z
    normalized = {k: normalize(v, vmin, vmax) for k, v in raw.items()}

    return {"raw": raw, "normalized": normalized, "eu_members_used": present_eu}


def compute_dimension():
    """Compute the Compute (C) dimension from the real TOP500 June 2026 list."""
    df = pd.read_excel(f"{DATA_DIR}/top500_2026.xlsx")
    rmax_col = "Rmax [TFlop/s]"
    total_world = df[rmax_col].sum()

    eu_rmax = df[df["Country"].isin(EU27_TOP500_NAMES)][rmax_col].sum()
    us_rmax = df[df["Country"] == "United States"][rmax_col].sum()
    cn_rmax = df[df["Country"] == "China"][rmax_col].sum()
    in_rmax = df[df["Country"] == "India"][rmax_col].sum()

    shares = {
        "United States": us_rmax / total_world,
        "China": cn_rmax / total_world,
        "India": in_rmax / total_world,
        "European Union": eu_rmax / total_world,
    }
    vmin, vmax = min(shares.values()), max(shares.values())

    # Higher Rmax share = more capacity = LOWER vulnerability -> v = 1 - z
    normalized = {k: 1 - normalize(v, vmin, vmax) for k, v in shares.items()}

    return {"world_total_tflops": total_world, "shares": shares, "normalized": normalized}


def compute_dimension_2015_baseline():
    """India's TOP500 share in June 2015, for the trajectory comparison."""
    df = pd.read_excel(f"{DATA_DIR}/top500_2015.xls")
    rmax_col = "Rmax"
    total_world = df[rmax_col].sum()
    in_rmax = df[df["Country"] == "India"][rmax_col].sum()
    return {"world_total_2015": total_world, "india_share_2015": in_rmax / total_world}


if __name__ == "__main__":
    sec = security_dimension()
    comp = compute_dimension()
    comp_2015 = compute_dimension_2015_baseline()

    results = {
        "security_dimension": {
            "raw_fdirri_scores": {k: round(v, 6) for k, v in sec["raw"].items()},
            "eu_members_used": sec["eu_members_used"],
            "n_eu_members": len(sec["eu_members_used"]),
            "normalized_v": {k: round(v, 3) for k, v in sec["normalized"].items()},
        },
        "compute_dimension": {
            "world_total_rmax_tflops_2026": round(comp["world_total_tflops"], 1),
            "shares_2026": {k: round(v, 4) for k, v in comp["shares"].items()},
            "normalized_v": {k: round(v, 3) for k, v in comp["normalized"].items()},
            "india_share_2015": round(comp_2015["india_share_2015"], 4),
            "world_total_rmax_2015": round(comp_2015["world_total_2015"], 1),
        },
    }

    print(json.dumps(results, indent=2))

    with open("../outputs/fcvi_results.json", "w") as f:
        json.dump(results, f, indent=2)
