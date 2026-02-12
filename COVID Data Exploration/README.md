# COVID Data Exploration

## Overview
This project was designed to execute and document a complete **end-to-end data analysis pipeline**. The primary objective was to demonstrate the technical workflow of migrating raw data from a relational database into a functional business intelligence tool. Rather than focusing solely on complex queries, this project emphasizes the architectural process of data extraction, transformation, and visualization.

---

## 🛠 Technical Stack
| Category | Tool |
| :--- | :--- |
| **Database** | Microsoft SQL Server |
| **Interface** | SQL Server Management Studio (SSMS) |
| **Data Cleaning** | Microsoft Excel |
| **Visualization** | Tableau |

---

## 🚀 Project Workflow



### 1. Data Acquisition & Ingestion
* Imported the comprehensive **Our World in Data** COVID-19 dataset into a local Microsoft SQL Server development environment.
* Configured database schemas to ensure data integrity during the initial load.

### 2. Data Transformation (SQL)
* Utilized **SQL Server Management Studio (SSMS)** to perform data exploration and filtering.
* Developed specific queries to isolate key metrics (deaths, infection rates, etc.) required for high-level visualizations.

### 3. Data Cleaning & Final Adjustments
* Exported query results to **Microsoft Excel** for final data auditing.
* Standardized the dataset by handling NULL values (converting to 0) to ensure accurate calculations within the visualization software.

### 4. Visualization & Reporting
* Imported the cleaned dataset into **Tableau**.
* Built a series of interactive visualizations and compiled them into a final **Tableau Dashboard** for stakeholder review.

---

## 📊 Results

### Interactive Dashboard
Check out the final results here: **[View COVID-19 Data Dashboard](https://public.tableau.com/views/COVIDDataExploration_17660107005600/COVIDDataExploration?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)**

### Dashboard Preview
![COVID-19 Dashboard Screenshot](https://github.com/chase-munson/Portfolio-Projects/blob/main/COVID%20Data%20Exploration/Tableau%20Tables/COVID%20Data%20Exploration.png)

---

## 📚 Credits & Resources
* **Dataset:** [Our World in Data - Coronavirus (COVID-19) Deaths](https://ourworldindata.org/coronavirus)
* **Learning Pathway:** Alex the Analyst (SQL Data Exploration & Tableau Visualization Series)

---
**Author:** Chase Munson


