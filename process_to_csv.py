#!/usr/bin/env python3
"""
Process collected JSON data into a CSV file.
"""
import json
import csv
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from glob import glob

# Configuration
DATA_DIR = "data"
OUTPUT_FILE = "mls_2026_schedule.csv"

def parse_kickoff_time(kickoff_str):
    """Parse ISO datetime string and convert to Pacific time."""
    # Parse UTC time
    dt_utc = datetime.fromisoformat(kickoff_str.replace('Z', '+00:00'))

    # Convert to Pacific timezone
    dt_pacific = dt_utc.astimezone(ZoneInfo('America/Los_Angeles'))

    # Format date and time
    match_date = dt_pacific.strftime("%Y-%m-%d")
    game_time = dt_pacific.strftime("%-I:%M %p")  # 12-hour format with AM/PM

    # Determine if PST or PDT
    timezone = dt_pacific.strftime("%Z")  # Will be PST or PDT

    return match_date, game_time, timezone

def process_json_files():
    """Process all JSON files and extract match data."""
    matches = []

    # Find all week*.json files and sort them
    json_files = sorted(glob(os.path.join(DATA_DIR, "week*.json")),
                       key=lambda x: int(os.path.basename(x).replace('week', '').replace('.json', '')))

    for json_file in json_files:
        print(f"Processing {json_file}...")

        with open(json_file, 'r') as f:
            data = json.load(f)

        # Extract matches from the schedule
        if 'schedule' in data:
            for match in data['schedule']:
                match_date, game_time, timezone = parse_kickoff_time(match['planned_kickoff_time'])

                match_info = {
                    'Match Week': match['match_day'],
                    'Match Date': match_date,
                    'Home Team': match['home_team_short_name'],
                    'Away Team': match['away_team_short_name'],
                    'Game Time': game_time,
                    'Timezone': timezone
                }
                matches.append(match_info)

    return matches

def write_csv(matches):
    """Write matches to CSV file."""
    if not matches:
        print("No matches found!")
        return

    fieldnames = ['Match Week', 'Match Date', 'Home Team', 'Away Team', 'Game Time', 'Timezone']

    with open(OUTPUT_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(matches)

    print(f"\n✓ CSV file created: {OUTPUT_FILE}")
    print(f"  Total matches: {len(matches)}")

def main():
    """Main processing function."""
    print("Processing JSON files to CSV...\n")

    matches = process_json_files()
    write_csv(matches)

if __name__ == "__main__":
    main()
