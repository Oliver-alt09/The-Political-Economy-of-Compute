# Replication Package — The Political Economy of Compute

Associated working paper: **The Political Economy of Compute: AI, Industrial Policy, and the Reorganization of Comparative Advantage**

Author: **Sandeep**
Affiliation: **National Institute of Technology Jamshedpur, India**
Forecast vintage: **12 September 2026**

## Scope

This package reproduces every empirically computed quantity reported in Section 7.1 (HS 8517 shift-share analysis) and Section 7.3 (the populated Compute and Security FCVI dimensions).

It is not a complete replication of every claim in the paper. The Energy, Capital, and Labour FCVI dimensions are not populated because a fully harmonised cross-country panel was not assembled. The shift-share material includes the single-industry HS 8517 two-term decomposition for 2015–2019 and the 2015–2024 absolute-growth comparison; it does not include a full multi-industry three-term decomposition.

## Package structure

```text
Political Economy of Compute/
├── Readme.md
├── data/
│   ├── oecd_fdirri_2024.csv
│   ├── top500_2015.xls
│   ├── top500_2026.xlsx
│   ├── ministry_of_commerce.pdf
│   └── comtrade_hs8517_india.json
├── Figures/
│   ├── Industrial Policy Feedback.png
│   ├── Infrastructure Bottleneck.png
│   ├── FCVI Measurement Framework.png
│   └── Forecast Dependency Network.png
├── outputs/
│   ├── fcvi_results.json
│   └── hs8517_shiftshare_results.json
├── scripts/
│   ├── fcvi_normalize.py
│   └── shiftshare_hs8517.py
└── Tables/
    ├── Forecast_Portfolio.xlsx
    ├── India_Trade_Benchmarks.xlsx
    ├── FCVI_Partial_Dimensions.xlsx
    ├── Qualitative_Positioning.xlsx
    ├── Scenario_Payoff_Matrix.xlsx
    ├── Forecast_Dependencies.xlsx
    └── Forecast_Audit.xlsx
```

## Reproduction

From the `scripts/` directory:

```bash
pip install pandas openpyxl xlrd
python3 fcvi_normalize.py
python3 shiftshare_hs8517.py
```

The scripts require no network access or API key because the source data used for the reported computations are included in `data/`.

## Provenance and verification

The OECD FDIRRI and TOP500 files were supplied as source files for the paper. The HS 8517 trade figures were cross-checked using the Ministry of Commerce report and UN Comtrade public-preview data included in the package.

The package intentionally does not claim that a composite five-dimension FCVI or a full three-term multi-industry shift-share has been reproduced. Those analyses remain explicitly identified as incomplete in the manuscript.
