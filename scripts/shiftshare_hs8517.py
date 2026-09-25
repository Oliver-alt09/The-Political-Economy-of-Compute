"""
02_shift_share_hs8517.py

Reproduces the two shift-share results reported in Section 7.1 of
"The Political Economy of Compute":

  1. The 2015-2024 absolute growth figures (India's HS 8517 exports),
     sourced directly from the UN Comtrade public preview API.

  2. The 2015-2019 two-term constant-market-share decomposition
     (Market Growth Effect vs. Competitive Share Effect), sourced from
     the Ministry of Commerce / Department of Commerce report
     "India's International Trade of Telephone Sets and Apparatus"
     (Tables 2 and 6), which draws on UN Comtrade and the Export Import
     Data Bank.

Note on scope: this is a genuine SINGLE-INDUSTRY (HS 8517 only) two-term
decomposition. It does NOT include an Industry Mix term, which requires
a multi-HS4-code portfolio (not available from the source PDF, which
covers HS 8517 only). The paper is explicit about this scope limitation.

Run:  python3 02_shift_share_hs8517.py
"""

import json

# --- Part 1: Comtrade-sourced absolute figures, 2015 vs 2024 -------------
with open("../data/comtrade_hs8517_india.json") as f:
    comtrade = json.load(f)

india_2015_comtrade = comtrade["query_2015"]["response"]["data"][0]["fobvalue"]
india_2024_comtrade = comtrade["query_2024"]["response"]["data"][0]["fobvalue"]

growth_multiple = india_2024_comtrade / india_2015_comtrade

# --- Part 2: Ministry of Commerce report figures, 2015 vs 2019 -----------
# Table 2 (world exports of HS 8517, million USD) and Table 6 (India's
# exports of HS 8517, million USD), transcribed directly from the PDF.
WORLD_HS8517_2015_M = 511762.99
WORLD_HS8517_2019_M = 565417.34
INDIA_HS8517_2015_M = 788.98956
INDIA_HS8517_2019_M = 4285.712


def two_term_shift_share(world_t0, world_t1, country_t0, country_t1):
    """Standard constant-market-share (CMS) identity for a single industry:

        delta_X = (g_world * X_t0) + [(g_country - g_world) * X_t0]
                = Market Growth Effect + Competitive Share Effect

    This is the single-industry special case of the full three-term
    shift-share identity used elsewhere in the paper; with only one
    industry, the Industry Mix term is undefined (it requires comparing
    growth rates across multiple industries within the country's
    portfolio).
    """
    g_world = (world_t1 - world_t0) / world_t0
    g_country = (country_t1 - country_t0) / country_t0

    delta_x = country_t1 - country_t0
    market_growth_effect = g_world * country_t0
    competitive_effect = (g_country - g_world) * country_t0

    return {
        "g_world": g_world,
        "g_country": g_country,
        "delta_x": delta_x,
        "market_growth_effect": market_growth_effect,
        "competitive_effect": competitive_effect,
        "market_growth_share_of_total": market_growth_effect / delta_x,
        "competitive_share_of_total": competitive_effect / delta_x,
        "sum_check": market_growth_effect + competitive_effect,
    }


if __name__ == "__main__":
    cross_check = {
        "comtrade_india_2015_usd": india_2015_comtrade,
        "moc_report_india_2015_musd_x1e6": INDIA_HS8517_2015_M * 1e6,
        "match": abs(india_2015_comtrade - INDIA_HS8517_2015_M * 1e6) < 1000,
    }

    absolute_growth = {
        "india_hs8517_exports_2015_usd": india_2015_comtrade,
        "india_hs8517_exports_2024_usd": india_2024_comtrade,
        "growth_multiple": round(growth_multiple, 2),
    }

    decomposition = two_term_shift_share(
        WORLD_HS8517_2015_M, WORLD_HS8517_2019_M,
        INDIA_HS8517_2015_M, INDIA_HS8517_2019_M,
    )

    results = {
        "cross_validation_comtrade_vs_moc_report": cross_check,
        "absolute_growth_2015_2024_comtrade": absolute_growth,
        "two_term_decomposition_2015_2019_moc_report": {
            k: (round(v, 4) if isinstance(v, float) else v)
            for k, v in decomposition.items()
        },
    }

    print(json.dumps(results, indent=2))

    with open("../outputs/hs8517_shiftshare_results.json", "w") as f:
        json.dump(results, f, indent=2)
