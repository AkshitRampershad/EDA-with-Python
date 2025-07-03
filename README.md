# Indicators of Heavy Traffic on I-94

This project analyzes traffic and weather data to identify key indicators of heavy traffic volume on the westbound I-94 Interstate highway near Minneapolis–Saint Paul.

---

## Project Overview

The goal is to explore and identify factors that influence heavy traffic on I-94 using a dataset collected hourly from 2012 to 2018. The analysis focuses on:

- Time indicators such as month, day of the week, and time of day  
- Weather indicators such as weather conditions and temperature

---

## Dataset

The dataset used in this project is the [Metro Interstate Traffic Volume dataset](https://archive.ics.uci.edu/ml/datasets/Metro+Interstate+Traffic+Volume) from the UCI Machine Learning Repository.

- **Source:** Traffic data recorded near the midpoint between Minneapolis and Saint Paul  
- **Timeframe:** October 2012 - September 2018  
- **Granularity:** Hourly traffic and weather data  
- **Size:** 48,204 rows and 9 columns  
- **Important Columns:**  
  - `date_time`: Timestamp for each hourly record  
  - `traffic_volume`: Number of vehicles passing the station  
  - Weather-related columns: `temp`, `rain_1h`, `snow_1h`, `clouds_all`, `weather_main`, `weather_description`

---

## Key Findings

### Time Indicators of Heavy Traffic

- Traffic volume is generally heavier during **warm months** (March–October) than cold months (November–February).  
- Traffic is heavier on **business days (Monday–Friday)** compared to weekends.  
- **Rush hours** during business days are around **7 AM** and **4 PM**, with traffic volumes exceeding 6,000 vehicles per hour.

### Weather Indicators of Heavy Traffic

Certain weather types correlate with heavier traffic:

- Shower snow  
- Light rain and snow  
- Proximity thunderstorm with drizzle

These conditions may encourage more drivers to use cars rather than alternative transportation.

---

## Analysis Highlights

- Visualization of traffic volume distributions for daytime vs. nighttime  
- Examination of traffic volume trends by month, day of the week, and hour of the day  
- Correlation analysis between weather variables and traffic volume  
- Bar charts showing average traffic volume by weather main type and detailed weather descriptions

---

## How to Use

1. Clone the repository.  
2. Install required Python libraries (`pandas`, `matplotlib`).  
3. Load the dataset (`Metro_Interstate_Traffic_Volume.csv`).  
4. Run the Jupyter notebook or Python script to reproduce the analysis and visualizations.

---

## Dependencies

- Python 3.x  
- pandas  
- matplotlib

---

## References

- [UCI Machine Learning Repository - Metro Interstate Traffic Volume](https://archive.ics.uci.edu/ml/datasets/Metro+Interstate+Traffic+Volume)  
- [Wikipedia - Interstate 94](https://en.wikipedia.org/wiki/Interstate_94)  
- [Traffic Construction Article 2016](https://www.crainsdetroit.com/article/20160728/NEWS/160729841/weekend-construction-i-96-us-23-bridge-work-i-94-lane-closures-i-696)

