# CTA "L" Train Delay Data Pipeline

An end-to-end data pipeline that captures live Chicago Transit Authority (CTA)
"L" train positions, stores them for analysis, and visualizes on-time
performance (OTP) trends across the system.

## Problem

The CTA does not publish a ready-made OTP (on-time performance) dataset, but
it does expose a live Train Tracker API. To analyze delay patterns by line,
station, and time of day, that live feed first has to be captured, stored,
and rolled up into something query-able and visualizable.

## Approach

- **Ingestion:** a Python script polls the CTA Train Tracker API every 60
  seconds for all 8 rail lines and writes each train's position/status to a
  local SQLite database (`scripts/cta_train_tracker.py`). The API key is
  read from a `.env` file, never hardcoded.
- **Deployment:** the ingestion script runs continuously on a small cloud VM
  (GCP e2-micro) as a systemd service, so data collection survives reboots
  and doesn't depend on a laptop staying on.
- **Storage rotation:** a companion script rotates and uploads the monthly
  SQLite database to cloud storage on a schedule (`rotate_db.sh` +
  systemd timer), keeping the working database from growing unbounded.
- **Schedule data:** `scripts/gtfs_refresh.py` checks weekly for updated CTA
  GTFS schedule data and archives new versions to cloud storage, for future
  use correlating scheduled vs. actual arrival times.
- **Analysis & visualization:** the collected data is loaded into Power BI
  (via the SQLite ODBC driver) and Tableau, with a date/time dimension table,
  delay-rate DAX measures, and dashboards showing delay rate by line, top
  delayed stations, a 7-day rolling trend, and an hour-by-day-of-week heatmap.

## Results

Based on ~2 million observations collected May 7 – June 1, 2026 (one API
snapshot per active train per minute):

- System-wide delay rate, plus delay rate broken out by line and by station,
  surfaced in a filterable Power BI dashboard (date/month slicers, 7-day
  rolling average trend line).
- The **Purple Line** had the highest line-level delay rate (2.01%), driven
  by a May 9 service disruption and a May 26 track fire near Belmont.
- **Ashland/63rd** was the highest-delay station overall, at 15.52%.
- An hour-of-day × day-of-week heatmap highlights when delays cluster across
  the week.

See `visuals/cta_data_visuals_powerbi.pbix` for the full Power BI dashboard,
and `visuals/CTA Data Visuals v2.twb` for the Tableau version (the more
recent iteration of the dashboard; `CTA Data Visuals.twb` is kept as the
earlier version).

## How to run

1. From the repo root, create a virtual environment and install this
   project's dependencies:
   ```bash
   cd "CTA Train Delay Analysis"
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
2. Get a free API key from the [CTA Train Tracker API](https://www.transitchicago.com/developers/traintrackerapi/)
   and create a `.env` file in this folder:
   ```
   API_KEY=your_key_here
   ```
3. Run the ingestion script (runs continuously, polling every 60 seconds):
   ```bash
   python scripts/cta_train_tracker.py
   ```
   This creates/updates `data/cta_train_tracker_data.db`.
4. (Optional) Refresh CTA's GTFS schedule data on a schedule:
   ```bash
   python scripts/gtfs_refresh.py
   ```
5. Open `visuals/cta_data_visuals_powerbi.pbix` in Power BI Desktop (or
   `visuals/CTA Data Visuals v2.twb` in Tableau) and point the data source
   at your `.db` file to explore the dashboards.

## Project layout

```
scripts/     ingestion and maintenance scripts
data/        SQLite database(s) produced by the ingestion script
notebooks/   exploratory data analysis
visuals/     Power BI (.pbix, ~41MB) and Tableau (.twb) dashboards
documents/   project journal, dashboard build documentation, and CTA API
             reference guides (Train Tracker API docs, OTP pipeline guide)
```

**Note on file sizes:** `visuals/cta_data_visuals_powerbi.pbix` is ~41MB —
well under GitHub's 100MB hard limit, and it's the actual working dashboard
file rather than sample/placeholder data, so it's kept as-is. The raw
monthly ingestion databases (hundreds of MB to ~1GB each) and a ~1GB derived
CSV used for Tableau prep are **not** included here; they live outside
version control given their size.

## Status

Data collection and both dashboards are functional. GTFS schedule data is
being collected for a planned future iteration that layers scheduled vs.
actual arrival times into the delay analysis.
