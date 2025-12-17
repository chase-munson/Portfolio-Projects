This project focused on a public dataset from: https://ourworldindata.org/covid-deaths.

The data was loaded into a local Microsoft SQL development database and manipulated with SQL Queries to pull the required information for use in Tableau Public via multiple Excel files.

The Excel files were adjusted by removing NULL values and replacing them with 0 to avoid conflicts in Tableau Public. Furthermore, Tableau Table 4.xlsx had the date column adjusted to display as a short date after it was noticed that the values were not displaying correctly.

After exporting the data required, visualizations were made in Tableau Public, which resulted in the dashboard at this [link](https://public.tableau.com/views/COVIDDataExploration_17660107005600/COVIDDataExploration?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link).
