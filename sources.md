# Data Sources & Methodological Audit Log

This document provides a transparent audit trail of the primary official portals, gazette notifications, legislative texts, press releases, and secondary news reports referenced in `policy_events.csv` and `regimes.csv`.

---

## 1. Primary Sources & Nodal Authorities

### India (Primary Focus)
* **Press Information Bureau (PIB), Government of India**: Official government press releases for Cabinet approvals, FDI policy announcements, IN-SPACe authorizations, and budget allocations.
  * [PIB Cabinet Release: IN-SPACe Establishment (June 2020)](https://pib.gov.in/PressReleasePage.aspx?PRID=1633917)
  * [PIB Release: First IN-SPACe Authorizations (June 2022)](https://pib.gov.in/PressReleasePage.aspx?PRID=1836798)
  * [PIB Cabinet Release: Indian Space Policy 2023 (April 2023)](https://pib.gov.in/PressReleasePage.aspx?PRID=1914304)
  * [PIB Cabinet Release: Amended FDI Policy for Space (Feb 2024)](https://pib.gov.in/PressReleasePage.aspx?PRID=2007817)
  * [PIB Cabinet Release: ₹1,000 Crore Space VC Fund (Oct 2024)](https://pib.gov.in/PressReleasePage.aspx?PRID=2067272)
* **eGazette & Ministry of Finance Notifications**:
  * [FEMA Non-Debt Instruments Amendment Rules (Press Note 1 of 2024)](https://egazette.gov.in/WriteReadData/2024/253723.pdf)
* **ISRO & IN-SPACe Official Portals**:
  * [Indian Space Policy 2023 PDF](https://www.isro.gov.in/media_isro/pdf/IndianSpacePolicy2023.pdf)
  * [IN-SPACe Norms, Guidelines and Procedures (NGP)](https://www.inspace.gov.in/inspace?id=inspace_ngp)
  * [Draft Space Activities Bill 2017 Archive](https://www.isro.gov.in/SpaceActivitiesBill2017.html)

### United States (Comparator 1)
* **U.S. Congress (Congress.gov)**:
  * [Commercial Space Launch Act of 1984 (Public Law 98-575)](https://www.congress.gov/bill/98th-congress/house-bill/3942)
  * [US Commercial Space Launch Competitiveness Act of 2015 (Public Law 114-90)](https://www.congress.gov/bill/114th-congress/house-bill/2262)
* **Federal Register & FAA/AST**:
  * [14 CFR Part 450 Streamlined Licensing Final Rule](https://www.federalregister.gov/documents/2020/12/10/2020-22042/streamlined-launch-and-reentry-licensing-requirements)
  * [Space Policy Directive-1](https://www.federalregister.gov/documents/2017/12/14/2017-27025/white-house-space-policy-directive-1)
* **NASA**:
  * [Artemis Accords Portal](https://www.nasa.gov/artemisaccords)

### Luxembourg (Comparator 2)
* **Journal Officiel du Grand-Duché de Luxembourg (Legilux)**:
  * [Loi du 20 juillet 2017 sur l'exploration et l'utilisation des ressources de l'espace](https://legilux.public.lu/eli/etat/leg/loi/2017/07/20/a674/jo)
* **Luxembourg Space Agency (LSA)**:
  * [SpaceResources.lu Initiative Announcement](https://space-agency.public.lu/en/news-media/news/2016/SpaceResources_initiativ.html)
  * [Creation of Luxembourg Space Agency (2018)](https://space-agency.public.lu/en/news-media/news/2018/LSA_creation.html)

### United Arab Emirates (Comparator 3)
* **UAE Space Agency (UAESA) & UAE Legislation Portal**:
  * [Federal Law No. (12) of 2019 Regarding Regulation of Space Sector](https://space.gov.ae/page/regulations)
  * [UAE Space Agency Strategic Regulations](https://space.gov.ae/page/policy-and-regulations)

---

## 2. Inferences, Precision & Assumptions Log

| Event ID | Field | Inferred / Approximated Value | Rationale & Primary Source Reference |
|---|---|---|---|
| `space-activities-bill-draft-2020` | `date` | `2020-11-01` | Exact day of internal DoS draft revision is not specified in gazette; set to `2020-11-01` with `date_precision: month` following parliamentary submission references. |
| `inspace-ngp-guidelines-2023` | `date` | `2023-10-04` | IN-SPACe published the NGP portal document in October 2023; exact public release timestamp confirmed via PIB and portal metadata. |
| `fdi-policy-space-cabinet-2024` | `date` | `2024-02-21` | PIB released Cabinet approval notice on Feb 21, 2024. FEMA rules formalizing this were notified on April 16, 2024 (`fdi-policy-fema-notification-2024`), creating a explicit 55-day policy-to-regulation enactment lag. |
| `us-csla-1984` | `date` | `1984-10-30` | Enactment date signed into law by President Reagan as recorded on Congress.gov. |

---

## 3. Data Integrity Principles
1. **No Copied Text**: All summaries in `description` fields are original syntheses by policy analysts.
2. **Primary Citation**: Government gazette or press releases are prioritized over news media.
3. **Traceable Precedents**: The `supersedes_event_id` column explicitly maps evolution from draft bills to final policy instruments.
