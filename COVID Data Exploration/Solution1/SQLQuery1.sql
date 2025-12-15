SELECT *
FROM Portfolio_Project..CovidDeaths
WHERE continent IS NOT NULL
ORDER BY 3,4


SELECT *
FROM Portfolio_Project..CovidVaccinations
ORDER BY 3,4


SELECT location, date, total_cases, new_cases, total_deaths, population
FROM Portfolio_Project..CovidDeaths
WHERE continent IS NOT NULL
ORDER BY 1,2


-- Looking at Total Cases vs. Total Deaths
-- Shows likelihood of death if you contract COVID in your country
SELECT location, date, total_cases, total_deaths, (total_deaths/total_cases) * 100 AS death_percentage
FROM Portfolio_Project..CovidDeaths
WHERE continent IS NOT NULL
AND location LIKE '%states%'
ORDER BY 1,2


-- Lookng at Total Cases vs. Population
-- Shows percentage of Population that got COVID
SELECT location, date, total_cases, population, (total_cases/population) * 100 AS percent_population_infected
FROM Portfolio_Project..CovidDeaths
WHERE continent IS NOT NULL
--AND location LIKE '%states%'
ORDER BY 1,2


-- Looking at Countries with Highest Infection Rate compared to Population
SELECT location, population, MAX(total_cases) AS highest_infection_count, 
	MAX((total_cases/population)) * 100 AS percent_population_infected
FROM Portfolio_Project..CovidDeaths
WHERE continent IS NOT NULL
--AND location LIKE '%states%'
GROUP BY location, population
ORDER BY percent_population_infected DESC


-- Showing Countries with the Highest Death Count per Population
SELECT location, MAX(CAST(total_deaths AS INT)) AS Total_Death_Count
FROM Portfolio_Project..CovidDeaths
WHERE continent IS NOT NULL
--AND location LIKE '%states%'
GROUP BY location, population
ORDER BY Total_Death_Count DESC


-- Showing Continent with the Highest Death Count per Population
SELECT continent, MAX(CAST(total_deaths AS INT)) AS Total_Death_Count
FROM Portfolio_Project..CovidDeaths
WHERE continent IS NOT NULL
--AND location LIKE '%states%'
GROUP BY continent
ORDER BY Total_Death_Count DESC

-- Correct way as per instructions, but not used for later parts of project
-- Showing Continent with the Highest Death Count per Population
SELECT location, MAX(CAST(total_deaths AS INT)) AS Total_Death_Count
FROM Portfolio_Project..CovidDeaths
WHERE continent IS NULL
--AND location LIKE '%states%'
GROUP BY location
ORDER BY Total_Death_Count DESC


-- Global Numbers by Date
SELECT date, SUM(new_cases) AS total_cases, 
	SUM(cast(new_deaths AS INT)) AS total_deaths, 
	SUM(CAST(new_deaths AS INT)) / SUM(new_cases) * 100 AS death_percentage
FROM Portfolio_Project..CovidDeaths
WHERE continent IS NOT NULL
--AND location LIKE '%states%'
GROUP BY date
ORDER BY 1,2


-- Global Numbers Total
SELECT SUM(new_cases) AS total_cases, 
	SUM(cast(new_deaths AS INT)) AS total_deaths, 
	SUM(CAST(new_deaths AS INT)) / SUM(new_cases) * 100 AS death_percentage
FROM Portfolio_Project..CovidDeaths
WHERE continent IS NOT NULL
--AND location LIKE '%states%'
--GROUP BY date
ORDER BY 1,2


-- Looking at Total Population vs Vaccinations
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(CAST(vac.new_vaccinations AS INT)) OVER (PARTITION BY dea.location ORDER BY dea.location,
dea.date) AS rolling_people_vaccinated
--(rolling_people_vaccinated/population) * 100
FROM Portfolio_Project..CovidDeaths dea
JOIN Portfolio_Project..CovidVaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL
ORDER BY 2, 3


--WITH CTE
WITH population_vs_vaccination (continent, location, date, population, new_vaccinations, rolling_people_vaccinated) AS
(
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(CAST(vac.new_vaccinations AS INT)) OVER (PARTITION BY dea.location ORDER BY dea.location,
dea.date) AS rolling_people_vaccinated
--(rolling_people_vaccinated/population) * 100
FROM Portfolio_Project..CovidDeaths dea
JOIN Portfolio_Project..CovidVaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL
-- ORDER BY 2, 3
)
SELECT *, (rolling_people_vaccinated/population) * 100
FROM population_vs_vaccination


--TEMP TABLE
DROP TABLE IF EXISTS #percent_population_vaccinated
CREATE TABLE #percent_population_vaccinated
(
continent nvarchar(255),
location nvarchar(255),
date datetime,
population numeric,
new_vaccinations numeric,
rolling_people_vaccinated numeric
)
INSERT INTO #percent_population_vaccinated
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(CAST(vac.new_vaccinations AS INT)) OVER (PARTITION BY dea.location ORDER BY dea.location,
dea.date) AS rolling_people_vaccinated
--(rolling_people_vaccinated/population) * 100
FROM Portfolio_Project..CovidDeaths dea
JOIN Portfolio_Project..CovidVaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL
-- ORDER BY 2, 3

SELECT *, (rolling_people_vaccinated/population) * 100
FROM #percent_population_vaccinated

-- Creating view to store data for later visualizations
DROP VIEW IF EXISTS percent_population_vaccinated

CREATE VIEW percent_population_vaccinated AS
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(CAST(vac.new_vaccinations AS INT)) OVER (PARTITION BY dea.location ORDER BY dea.location,
dea.date) AS rolling_people_vaccinated
--(rolling_people_vaccinated/population) * 100
FROM Portfolio_Project..CovidDeaths dea
JOIN Portfolio_Project..CovidVaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL
--ORDER BY 2, 3

SELECT * FROM percent_population_vaccinated

