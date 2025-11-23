# MLS 2026 Season Schedule Data Collection

This project collects the complete 2026 MLS regular season schedule from the official MLS Stats API and generates a CSV file with all match information in Pacific Time.

## Overview

The 2026 MLS season runs from February 16 through November 7, 2026. This project:
- Fetches match data from the MLS Stats API week by week
- Stores raw JSON responses for each calendar week
- Processes all data into a single CSV file with times converted to Pacific timezone

## Requirements

- Python 3.9 or higher
- Internet connection to access the MLS Stats API

## Installation

1. Install the required Python library:

```bash
pip3 install requests
```

That's it! The scripts use Python's built-in `zoneinfo` module for timezone conversions.

## Usage

### Step 1: Collect Data from API

Run the data collection script to fetch all match data:

```bash
python3 collect_data.py
```

This script will:
- Create a `data/` directory if it doesn't exist
- Fetch match data for 38 calendar weeks (Feb 16 - Nov 8, 2026)
- Save each week's data as `data/week{N}.json`
- Skip weeks that have already been downloaded
- Handle weeks with no games (returns 404) gracefully

**Note:** Some weeks will return 404 errors - this is expected! The MLS season has breaks for:
- International fixtures
- FIFA World Cup 2026 (June-July)
- Other scheduled breaks

The script takes about 20-30 seconds to run and will show progress for each week.

### Step 2: Generate CSV

Once data collection is complete, process the JSON files into a CSV:

```bash
python3 process_to_csv.py
```

This will create `mls_2026_schedule.csv` with the following columns:
- **Match Week** - The MLS matchday number (1-35)
- **Match Date** - Date in YYYY-MM-DD format
- **Home Team** - Home team short name
- **Away Team** - Away team short name
- **Game Time** - Kickoff time in 12-hour format (Pacific Time)
- **Timezone** - PST or PDT depending on the date

## Output

**Total matches:** 512 games across 35 match weeks

**Sample CSV output:**
```csv
Match Week,Match Date,Home Team,Away Team,Game Time,Timezone
1,2026-02-21,Cincinnati,Atlanta,1:30 PM,PST
1,2026-02-21,St. Louis,Charlotte,11:30 AM,PST
35,2026-11-07,Seattle,LAFC,4:00 PM,PST
```

## Data Source

All data is sourced from the official MLS Stats API:
```
https://stats-api.mlssoccer.com/matches/seasons/MLS-SEA-0001KA
```

## File Structure

```
mls2026/
├── README.md                    # This file
├── CLAUDE.md                    # Project instructions
├── collect_data.py              # Data collection script
├── process_to_csv.py            # CSV generation script
├── mls_2026_schedule.csv        # Generated CSV output
└── data/                        # Raw JSON data (29 files)
    ├── week1.json
    ├── week2.json
    └── ...
```

## Troubleshooting

**Q: Some weeks are missing from the data/ directory**
A: This is normal! Weeks 6, 16-21, 25, and 33 have no MLS games scheduled.

**Q: The CSV shows fewer than 38 weeks**
A: The CSV shows match weeks (1-35), not calendar weeks. Multiple calendar weeks can belong to the same match week due to scheduling.

**Q: Times look wrong for my timezone**
A: Times are shown in Pacific Time (PST/PDT). The `process_to_csv.py` script can be modified to use different timezones by changing `America/Los_Angeles` to your desired timezone.

## Re-running Scripts

Both scripts are safe to re-run:
- `collect_data.py` will skip weeks that already exist
- `process_to_csv.py` will overwrite the CSV file with fresh data

To force a complete re-download, delete the `data/` directory first:
```bash
rm -rf data/
python3 collect_data.py
```

## License

This project uses publicly available data from Major League Soccer's official API.

## Development

This project was developed with assistance from Claude Code, Anthropic's AI assistant for software development.
