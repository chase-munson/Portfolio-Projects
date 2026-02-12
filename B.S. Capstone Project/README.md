# Analysis of Flight Delays Compared to Weather in the Domestic Flight Market

## Project Overview
This project investigates the correlation between domestic flight delays and changing weather patterns within the United States domestic airline market. As severe weather events become more frequent across different U.S. regions, this research aims to determine if weather contributes significantly to delay frequency. This analysis provides data-driven insights to help airlines decide whether to adjust scheduling or prioritize further weather-impact research.

## Research Question & Hypotheses
* **Research Question:** Is there a correlation between domestic flight delays and globally changing weather patterns?
* **Null Hypothesis ($H_0$):** There is no correlation between weather and domestic flight delays.
* **Alternative Hypothesis ($H_a$):** Weather will positively correlate with domestic airline delays.

## Data Source
* **Dataset:** "Flight Delay" hosted on Kaggle, sourced from official government data.
* **Timeframe:** 2018–2024.
* **Size:** Approximately 30,132,672 rows and 29 columns.
* **Key Fields:** `FlightDate`, `Year`, `OriginCity`, `DestCity`, and `WeatherDelay` (measured in minutes).

## Methodology
The project utilizes the **CRISP-DM** (Cross-Industry Process for Data Mining) methodology:

1.  **Business Understanding:** Defining the impact of weather on airline operations.
2.  **Data Understanding:** Collecting and verifying dataset quality.
3.  **Data Preparation:** Cleaning the dataset, handling missing values, and performing data transformations (e.g., creating `CleanDates` for statistical analysis).
4.  **Modeling:** Performing statistical analysis via the **Pearson Correlation Test**.
5.  **Evaluation:** Analyzing results to determine statistical significance and null hypothesis rejection.
6.  **Deployment:** Creating visualizations and documenting findings in a final report.

## Technologies & Tools
* **Language:** Python
* **Libraries:**
    * **Pandas & NumPy:** Data cleaning and transformation.
    * **SciPy:** Statistical testing (Pearson Correlation).
    * **Matplotlib & Seaborn:** Data visualization.
* **Environment:** Jupyter Notebook
* **Version Control:** GitHub

## Key Findings
The Pearson Correlation Test was conducted using an alpha value of 0.05.

| Statistic (r-value) | P-Value |
| :--- | :--- |
| 0.04109091354365808 | 7.378745366859716e-144 |

* **Statistical Significance:** The p-value is significantly lower than 0.05, providing enough evidence to reject the null hypothesis and support the alternative hypothesis.
* **Correlation:** While minimal, the statistical result suggests a positive correlation, indicating that weather delays are increasing over time.
* **Visual Evidence:** Bar charts and histograms confirmed increasing average delay lengths and frequency year-over-year.

## Conclusions & Recommendations
* **Conclusion:** The analysis supports the conclusion that weather-related flight delays in the domestic market are increasing.
* **Recommendations:**
    1.  **Prioritize Research:** Airlines should emphasize researching this trend further to mitigate impacts on profit margins.
    2.  **Predictive Modeling:** Implement machine learning algorithms to proactively predict weather delays and offer early flight changes to consumers.

---
**Author:** Chase Munson
**Institution:** Western Governors University
