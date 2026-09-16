# COVID-19 Data Exploration & Pipeline

## Overview

This project demonstrates a complete data analysis pipeline — from raw relational database ingestion through to a published, interactive business intelligence dashboard. Rather than focusing solely on complex queries, this project emphasizes the architectural process of data extraction, transformation, and visualization: the technical workflow a data analyst uses to turn messy source data into clean, visual insights a non-technical audience can act on.

---

## Technical Stack

| Category | Tool |
|---|---|
| **Database** | Microsoft SQL Server |
| **Interface** | SQL Server Management Studio (SSMS) |
| **Data Cleaning** | Microsoft Excel |
| **Visualization** | Tableau |

---

## Project Workflow

### 1. Data Acquisition & Ingestion
Imported the **Our World in Data** COVID-19 dataset into a local Microsoft SQL Server development environment, with database schemas configured to ensure data integrity during the initial load.

### 2. Data Transformation (SQL)
Used SQL Server Management Studio to explore and filter the data, and developed queries to isolate the key metrics (deaths, infection rates, etc.) needed for the high-level visualizations.

### 3. Data Cleaning & Final Adjustments
Exported query results to Excel for final auditing, standardizing the dataset by handling NULL values (converted to 0) to keep calculations accurate downstream in the visualization software.

### 4. Visualization & Reporting
Loaded the cleaned dataset into Tableau and built a series of interactive visualizations, compiled into a final dashboard for stakeholder review.

---

## Results

**[View Interactive Tableau Dashboard](https://public.tableau.com/views/COVIDDataExploration_17660107005600/COVIDDataExploration?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)**

![COVID-19 Dashboard Screenshot](https://github.com/chase-munson/Portfolio-Projects/blob/main/COVID%20Data%20Exploration/Tableau%20Tables/COVID%20Data%20Exploration.png)

---

## Data files

`dataset/CovidDeaths.xlsx` and `dataset/CovidVaccinations.xlsx` (~9MB each) are the cleaned, exported datasets from step 3 of the workflow above — kept in the repo so the full pipeline is reproducible end to end, not just the final dashboard. Both are comfortably under GitHub's 100MB file limit.

---

## Credits & Resources

- **Dataset:** [Our World in Data — Coronavirus (COVID-19) Deaths](https://ourworldindata.org/coronavirus)
- **Learning pathway:** Alex the Analyst (SQL Data Exploration & Tableau Visualization series)

---

**Author:** Chase Munson
