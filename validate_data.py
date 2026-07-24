#!/usr/bin/env python3
"""
Data Validation Script for India Space Policy Tracker
Validates schema, date formats, enums, URL validity, referential integrity, and required fields.
"""

import sys
import re
from pathlib import Path
import pandas as pd

# Define paths relative to repo root
REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
POLICY_EVENTS_PATH = DATA_DIR / "policy_events.csv"
REGIMES_PATH = DATA_DIR / "regimes.csv"

# Enum definitions as per specification
VALID_DATE_PRECISION = {"day", "month", "year"}
VALID_CATEGORIES = {"institutional", "regulatory", "authorization", "funding", "launch_milestone"}
VALID_SOURCE_TYPES = {"official_gazette", "press_release", "news", "academic"}
VALID_STATUSES = {"enacted", "draft", "proposed", "superseded"}
REQUIRED_EVENT_COLUMNS = [
    "event_id", "country", "date", "date_precision", "category",
    "title", "description", "actors", "source_url", "source_type",
    "status", "supersedes_event_id"
]
REQUIRED_REGIME_COLUMNS = [
    "country", "regulator", "fdi_cap_satellites", "fdi_cap_launch_vehicles",
    "fdi_cap_ground_segment", "liability_framework", "licensing_model", "resource_rights"
]

def validate_policy_events():
    errors = []
    warnings = []

    if not POLICY_EVENTS_PATH.exists():
        return [f"File not found: {POLICY_EVENTS_PATH}"], []

    df = pd.read_csv(POLICY_EVENTS_PATH, dtype=str).fillna("")
    
    # Column presence
    missing_cols = set(REQUIRED_EVENT_COLUMNS) - set(df.columns)
    if missing_cols:
        errors.append(f"policy_events.csv missing required columns: {missing_cols}")
        return errors, warnings

    event_ids = set()

    for idx, row in df.iterrows():
        row_num = idx + 2  # 1-indexed header + row index
        
        # event_id validation
        e_id = row["event_id"].strip()
        if not e_id:
            errors.append(f"Row {row_num}: Missing event_id")
        elif e_id in event_ids:
            errors.append(f"Row {row_num}: Duplicate event_id '{e_id}'")
        else:
            event_ids.add(e_id)

        # Country validation
        country = row["country"].strip()
        if not country:
            errors.append(f"Row {row_num} ({e_id}): Missing country")

        # Date format YYYY-MM-DD
        date_str = row["date"].strip()
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
            errors.append(f"Row {row_num} ({e_id}): Invalid date format '{date_str}'. Expected YYYY-MM-DD")

        # Date precision enum
        precision = row["date_precision"].strip()
        if precision not in VALID_DATE_PRECISION:
            errors.append(f"Row {row_num} ({e_id}): Invalid date_precision '{precision}'. Must be one of {VALID_DATE_PRECISION}")

        # Category enum
        cat = row["category"].strip()
        if cat not in VALID_CATEGORIES:
            errors.append(f"Row {row_num} ({e_id}): Invalid category '{cat}'. Must be one of {VALID_CATEGORIES}")

        # Title presence
        if not row["title"].strip():
            errors.append(f"Row {row_num} ({e_id}): Title is empty")

        # Description length and quality check
        desc = row["description"].strip()
        if not desc:
            errors.append(f"Row {row_num} ({e_id}): Description is empty")
        elif len(desc.split()) < 5:
            warnings.append(f"Row {row_num} ({e_id}): Description is very short ({len(desc.split())} words)")

        # Actors presence
        if not row["actors"].strip():
            warnings.append(f"Row {row_num} ({e_id}): Actors field is empty")

        # Source URL check
        url = row["source_url"].strip()
        if not url:
            errors.append(f"Row {row_num} ({e_id}): Missing source_url")
        elif not (url.startswith("http://") or url.startswith("https://")):
            errors.append(f"Row {row_num} ({e_id}): Invalid source_url '{url}'. Must start with http:// or https://")

        # Source type enum
        s_type = row["source_type"].strip()
        if s_type not in VALID_SOURCE_TYPES:
            errors.append(f"Row {row_num} ({e_id}): Invalid source_type '{s_type}'. Must be one of {VALID_SOURCE_TYPES}")

        # Status enum
        status = row["status"].strip()
        if status not in VALID_STATUSES:
            errors.append(f"Row {row_num} ({e_id}): Invalid status '{status}'. Must be one of {VALID_STATUSES}")

    # Supersedes event_id referential integrity check
    for idx, row in df.iterrows():
        row_num = idx + 2
        e_id = row["event_id"].strip()
        sup_id = row["supersedes_event_id"].strip()
        if sup_id and sup_id not in event_ids:
            errors.append(f"Row {row_num} ({e_id}): supersedes_event_id '{sup_id}' does not exist in policy_events.csv")

    return errors, warnings


def validate_regimes():
    errors = []
    warnings = []

    if not REGIMES_PATH.exists():
        return [f"File not found: {REGIMES_PATH}"], []

    df = pd.read_csv(REGIMES_PATH, dtype=str).fillna("")

    missing_cols = set(REQUIRED_REGIME_COLUMNS) - set(df.columns)
    if missing_cols:
        errors.append(f"regimes.csv missing required columns: {missing_cols}")
        return errors, warnings

    if len(df) == 0:
        errors.append("regimes.csv is empty")

    for idx, row in df.iterrows():
        row_num = idx + 2
        country = row["country"].strip()
        if not country:
            errors.append(f"Row {row_num}: Missing country in regimes.csv")
        for col in REQUIRED_REGIME_COLUMNS:
            if not row[col].strip():
                warnings.append(f"Row {row_num} ({country}): Column '{col}' is empty in regimes.csv")

    return errors, warnings


def main():
    print("==========================================")
    print(" INDIA SPACE POLICY TRACKER - DATA VALIDATION")
    print("==========================================")
    
    event_errors, event_warnings = validate_policy_events()
    regime_errors, regime_warnings = validate_regimes()

    all_errors = event_errors + regime_errors
    all_warnings = event_warnings + regime_warnings

    if all_warnings:
        print(f"\n[WARNINGS: {len(all_warnings)}]")
        for w in all_warnings:
            print(f"  - {w}")

    if all_errors:
        print(f"\n[FAILED: {len(all_errors)} Errors Found]")
        for e in all_errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("\n[SUCCESS] All data validation checks passed cleanly!")
        sys.exit(0)

if __name__ == "__main__":
    main()
