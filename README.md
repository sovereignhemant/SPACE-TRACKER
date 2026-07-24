# 🚀 India Space Policy & Regulatory Regime Tracker

[![Streamlit Dashboard](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/brydgework/india-space-policy-tracker)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data Validation](https://img.shields.io/badge/Data%20Validation-Passing-brightgreen.svg)](scripts/validate_data.py)

An open, versioned, structured dataset and comparative analytical dashboard tracking the evolution of India's commercial space policy and regulatory regime from 2020 to 2026, benchmarked against three leading international space regimes (**United States**, **Luxembourg**, and **United Arab Emirates**).

---

## 📌 Executive Summary

India's space sector underwent a structural regime shift following the June 2020 Cabinet approval establishing **IN-SPACe** (Indian National Space Promotion and Authorization Centre) and expanding **NSIL**'s commercial aggregator mandate. This tracker converts non-governmental space authorizations, gazette notifications, FDI policy shifts, and legislative drafts into a single, standardized tidy dataset (`policy_events.csv`) accompanied by a comparative matrix (`regimes.csv`). By standardizing discrete policy events across countries, this project enables think tanks, policy analysts, journalists, and investors to evaluate regulatory velocity, policy-to-enactment lag, and global competitiveness without re-deriving primary source data.

---

## 🔍 Key Findings

1. **Policy-to-Regulatory Implementation Lag**: While the Union Cabinet approved liberalized foreign direct investment (FDI) caps on **February 21, 2024**, official operationalization under FEMA Non-Debt Instruments rules occurred on **April 16, 2024** (Press Note 1 of 2024) — representing an exact **55-day statutory enactment window**. Under the finalized rules, India permits **100% FDI** across the sector, with automatic clearance up to **74%** for satellite manufacturing/ops, **49%** for launch vehicles, and **100%** for satellite components.
2. **Authorization Velocity Expansion**: Between June 2022 (maiden authorizations to Dhruva Space and Digantara) and July 2026, IN-SPACe authorization types expanded from single-payload sub-orbital tests to comprehensive commercial infrastructure permissions — including **Ground Station as a Service (GSaaS)** for Dhruva Space, private launchpad operations (**Dhanush** at Sriharikota by Agnikul), national **Earth Observation constellations** (Pixxel consortium), and commercial **orbital launch missions** (Skyroot's Vikram-1).
3. **Single-Window vs. Multi-Agency Tradeoff**: India's IN-SPACe operates on an autonomous **single-window authorization model** similar to Luxembourg (LSA) and the UAE (UAESA), contrasting sharply with the United States' fragmented **multi-agency framework** (FAA/AST for launch, FCC for spectrum, NOAA for remote sensing, and CFIUS for investment).

---

## 🖥️ Live Streamlit Dashboard

Explore the interactive dashboard, generate custom charts, and filter milestones by regime or category:

👉 **[Launch Interactive Streamlit Dashboard](https://share.streamlit.io/brydgework/india-space-policy-tracker)**

### Dashboard Features:
* **Timeline View**: Filterable Plotly visualization of policy events across India, USA, Luxembourg, and UAE.
* **Regime Comparator**: Side-by-side benchmarking of FDI caps, liability frameworks, and licensing models.
* **IN-SPACe Authorization Tracker**: Cumulative velocity tracking and searchable directory of private Indian space permissions.

---

## 📂 Repository Structure

```
india-space-policy-tracker/
├── README.md                 # Policy brief summary, key findings, citation & repo links
├── data/
│   ├── policy_events.csv     # Primary dataset: discrete policy events (34+ rows)
│   ├── regimes.csv           # Comparative matrix: India vs USA, Luxembourg, UAE
│   └── sources.md            # Primary source citations, precision notes, audit log
├── dashboard/
│   └── app.py                # Streamlit dashboard application
├── notebooks/
│   └── exploration.ipynb     # Jupyter notebook analyzing policy trends & charts
├── scripts/
│   └── validate_data.py      # Automated schema & referential integrity validator
├── docs/
│   └── methodology.md        # Comprehensive scope, taxonomy, & sourcing rules
└── requirements.txt          # Python dependencies
```

---

## 📊 Data Schema Quick Reference

### `policy_events.csv`
| Column | Type | Description |
|---|---|---|
| `event_id` | String | Unique slug (e.g. `inspace-approved-2020`) |
| `country` | String | Country (`India`, `USA`, `Luxembourg`, `UAE`) |
| `date` | ISO Date | `YYYY-MM-DD` |
| `date_precision` | Enum | `day` / `month` / `year` |
| `category` | Enum | `institutional` / `regulatory` / `authorization` / `funding` / `launch_milestone` |
| `title` | String | Human-readable title |
| `description` | String | 1-3 sentences, neutral tone, original synthesis |
| `actors` | String | Comma-separated entities involved |
| `source_url` | String | Mandatory link to primary source |
| `source_type` | Enum | `official_gazette` / `press_release` / `news` / `academic` |
| `status` | Enum | `enacted` / `draft` / `proposed` / `superseded` |
| `supersedes_event_id` | String | Nullable link to prior draft event |

### Validation
To run the automated data quality checks:
```bash
python scripts/validate_data.py
```

---

## 📚 Methodology & Sourcing

Every row in `policy_events.csv` is anchored to a verified primary source (PIB releases, Gazette of India, Federal Register, Legilux, UAESA portals). No un-sourced rows are permitted. All event descriptions are original analytical syntheses.

For detailed taxonomy, scope boundaries, and date precision rules, see [docs/methodology.md](docs/methodology.md) and [data/sources.md](data/sources.md).

---

## 📖 How to Cite This Project

If you use this dataset or dashboard in a report, academic paper, or policy brief, please cite as follows:

> **Brydgework Policy Research (2026).** *India Space Policy and Regulatory Regime Tracker*. Version 1.0. Available at: [https://github.com/brydgework/india-space-policy-tracker](https://github.com/brydgework/india-space-policy-tracker).

```bibtex
@dataset{india_space_policy_tracker_2026,
  author       = {Brydgework Policy Research},
  title        = {India Space Policy and Regulatory Regime Tracker},
  year         = 2026,
  publisher    = {GitHub},
  url          = {https://github.com/brydgework/india-space-policy-tracker}
}
```

---

## 👤 Author & Companion Projects

**Author**: Policy Research Team, **Brydgework**  
**Companion Project**: Check out our companion dataset on Indian space expenditure: [india-space-budget](https://github.com/brydgework/india-space-budget)
