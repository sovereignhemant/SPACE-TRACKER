# Methodology & Scope Specification

## 1. Project Objective & Target Audience

The **India Space Policy & Regulatory Regime Tracker** is a public, structured dataset and comparative research project designed to track the evolution of India's commercial space policy framework since 2020, benchmarked against three established international regimes (**United States**, **Luxembourg**, and **United Arab Emirates**).

**Target Audience**: Space policy analysts, academic researchers, think-tank fellows (ORF, CEEW, Carnegie India, CAPS), journalists, and recruiters evaluating applied policy synthesis capability.

**Success Criteria**: Any analyst or researcher can directly cite a chart, metric, or row from this repository in a policy brief or report without needing to independently re-derive or verify raw regulatory dates.

---

## 2. Scope Boundaries

### 2.1 Primary Focus: India (2020 – Present)
The dataset tracks discrete events across five core categories:
1. **Institutional Milestones**: Creation of IN-SPACe (June 2020), commercialization mandate expansion of NewSpace India Limited (NSIL), and redefinition of ISRO's role as an R&D entity.
2. **Regulatory Instruments**: Draft Space Activities Bills (2017, 2020), Indian Space Policy 2023, IN-SPACe Norms, Guidelines and Procedures (NGP), and Foreign Direct Investment (FDI) policy amendments (100% FDI rules under FEMA).
3. **Approvals & Authorizations**: Formal IN-SPACe authorizations granted to non-governmental entities (NGEs) including Dhruva Space, Digantara, Skyroot Aerospace, Agnikul Cosmos, Pixxel, etc.
4. **Budget / Funding Signals**: DoS allocations relevant to commercialization, seed funds, and the ₹1,000 Crore Space Venture Capital Fund approved by the Cabinet in October 2024.
5. **Launch Milestones**: Policy-linked flight milestones such as the first private sub-orbital rocket launch (Vikram-S, Nov 2022), private launchpad flight (Agnibaan SOrTeD, May 2024), and private orbital launches (Vikram-1, July 2026).

### 2.2 Comparator Regimes (Depth over Breadth)
Three international regimes were selected for structural comparability:
* **United States**: Commercial Space Launch Act of 1984, 2015 Commercial Space Launch Competitiveness Act (space resource rights), FAA/AST Part 450 licensing, and Artemis Accords framework.
* **Luxembourg**: 2016 SpaceResources.lu initiative, 2017 Space Resources Law (first European space mining law), and Luxembourg Space Agency (LSA) creation.
* **United Arab Emirates**: 2014 UAE Space Agency establishment, 2019 Federal Space Law No. 12, and 2021 Space Activity Permitting Regulations.

### 2.3 Explicit Out of Scope (v1)
* **Defense & Military Programs**: Focused strictly on civil and commercial space policy.
* **State-Level Policies**: National/federal level policies only.
* **Full Text Reproduction**: Primary links are provided; text is synthesized in original words to avoid copyright infringement and maintain concise analytical utility.

---

## 3. Data Schema & Enums

### 3.1 `policy_events.csv`
| Column | Type | Enum Values / Format | Notes |
|---|---|---|---|
| `event_id` | String | Unique Slug (e.g. `inspace-approved-2020`) | Primary key |
| `country` | String | `India` / `USA` / `Luxembourg` / `UAE` | Regime identifier |
| `date` | ISO Date | `YYYY-MM-DD` | Event timestamp |
| `date_precision` | Enum | `day` / `month` / `year` | Honesty regarding source precision |
| `category` | Enum | `institutional` / `regulatory` / `authorization` / `funding` / `launch_milestone` | Taxonomy classification |
| `title` | String | Short human-readable title | Title case |
| `description` | String | 1-3 sentences | Original synthesis in neutral tone |
| `actors` | String | Comma-separated list | Entities involved |
| `source_url` | String | Valid `http://` or `https://` URL | Mandatory primary citation |
| `source_type` | Enum | `official_gazette` / `press_release` / `news` / `academic` | Source credibility metric |
| `status` | Enum | `enacted` / `draft` / `proposed` / `superseded` | Legal status of event |
| `supersedes_event_id` | String | Nullable `event_id` | Lineage tracking (e.g. draft → enacted) |

### 3.2 `regimes.csv` (One row per country)
| Column | Type | Description |
|---|---|---|
| `country` | String | Country name |
| `regulator` | String | Primary regulatory body (e.g. IN-SPACe, FAA/AST) |
| `fdi_cap_satellites` | String | Foreign direct investment ceiling for satellite ops |
| `fdi_cap_launch_vehicles` | String | FDI ceiling for launch vehicle manufacturing |
| `fdi_cap_ground_segment` | String | FDI ceiling for ground stations & component manufacturing |
| `liability_framework` | String | 1-2 sentence summary of 3rd-party liability & insurance rules |
| `licensing_model` | String | Single-window vs multi-agency approval structure |
| `resource_rights` | String | Domestic legal framework for space resource exploitation |

---

## 4. Sourcing & Verification Rules

1. **Primary Source Requirement**: Every event row MUST have a valid `source_url`.
2. **Sourcing Hierarchy**:
   * *Tier 1*: Official Government Gazette (e.g. Gazette of India, Legilux, US Federal Register), Official Ministry Press Releases (PIB, DoS, White House, UAESA).
   * *Tier 2*: Official regulatory portal publications (IN-SPACe NGP documents, FAA licensing rules).
   * *Tier 3*: Reputable international news outlets (Reuters, SpaceNews, The Hindu) used only when primary press releases are un-archived.
3. **No Direct Copy-Pasting**: All descriptions are original analytical syntheses.
4. **Automated Schema Validation**: Run `python scripts/validate_data.py` to enforce data types, enum bounds, URL formats, and referential integrity before committing changes.
