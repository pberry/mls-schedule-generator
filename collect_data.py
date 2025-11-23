#!/usr/bin/env python3
"""
Collect MLS 2026 season data from the API, one week at a time.
"""
import requests
from datetime import datetime, timedelta
import json
import os
import time

# Configuration
BASE_URL = "https://stats-api.mlssoccer.com/matches/seasons/MLS-SEA-0001KA"
START_DATE = datetime(2026, 2, 16)
END_DATE = datetime(2026, 11, 8)
TOTAL_WEEKS = 38  # Extended to cover through 2026-11-08
DATA_DIR = "data"

# Create data directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_week_data(week_num, start_date, end_date):
    """Fetch data for a specific week."""
    params = {
        "match_date[gte]": start_date.strftime("%Y-%m-%d"),
        "match_date[lte]": end_date.strftime("%Y-%m-%d"),
        "competition_id": "MLS-COM-000001",
        "per_page": "100",
        "sort": "planned_kickoff_time:asc,home_team_name:asc"
    }

    headers = {
        "Accept": "application/json",
        "User-Agent": "curl"
    }

    try:
        response = requests.get(BASE_URL, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching week {week_num}: {e}")
        return None

def main():
    """Collect data for all weeks through 2026-11-08."""
    print(f"Starting data collection for {TOTAL_WEEKS} weeks...")

    for week in range(1, TOTAL_WEEKS + 1):
        # Calculate date range for this week
        week_start = START_DATE + timedelta(days=(week - 1) * 7)
        week_end = week_start + timedelta(days=6)

        output_file = os.path.join(DATA_DIR, f"week{week}.json")

        # Skip if file already exists
        if os.path.exists(output_file):
            print(f"Week {week} already exists, skipping...")
            continue

        print(f"Fetching week {week}: {week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}...")

        data = fetch_week_data(week, week_start, week_end)

        if data:
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"  ✓ Saved to {output_file}")
        else:
            print(f"  ✗ Failed to fetch week {week}")

        # Be nice to the API
        time.sleep(0.5)

    print("\nData collection complete!")

if __name__ == "__main__":
    main()
