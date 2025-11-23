We are gathering data from an API that speaks JSON.
We will use python and simple libraries.
We will use curl and here is an example call that outputs JSON:

``` 
curl --globoff "https://stats-api.mlssoccer.com/matches/seasons/MLS-SEA-0001KA?match_date[gte]=2026-02-16&match_date[lte]=2026-02-23&competition_id=MLS-COM-000001&per_page=100&sort=planned_kickoff_time:asc,home_team_name:asc" \
  -H "Accept: application/json" \
  -H "User-Agent: curl"
```

Starting at 2026-02-16, increment the calls by 7 days, effectively getting one week at a time. Save the JSON repsonse in the data directory with the filename pattern week-N.json where N is the number of the week. There are only 34 weeks in the 2026 MLS season and the last date with games will be 2026-11-07.

Once we have collected the data for every week in JSON format, we will process that data to generate a CSV. The CSV will have the following headers:
Match Week, Match Date, Home Team, Away Team, Game Time

These headers will be derived from the following fields in the JSON data:
match_day, planned_kickoff_time, home_team_short_name, away_team_short_name,planned_kickoff_time

planned_kickoff_time contains the date and time in the format: "2026-10-26T01:00:00Z"
