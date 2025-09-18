# 🌍 Climate Risk Platform

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)  
[![Conda](https://img.shields.io/badge/Conda-Env-green.svg)](https://docs.conda.io/)

## 📌 Overview
The **Climate Risk Platform** is a data science project that combines **historical climate data** and **real-time weather forecasts** to analyze climate risks.  
It is designed as a portfolio-ready project for demonstrating end-to-end skills in:

- Data collection from APIs (Meteostat, Open-Meteo, etc.)
- Preprocessing & cleaning
- Exploratory Data Analysis (EDA)
- Modeling & risk analysis
- Visualization & dashboards
- Deployment-ready structure

This project aims to serve as a foundation for building **climate impact dashboards** for cities, agriculture, or infrastructure planning.

---

## 📂 Project Structure

climate-risk-platform/
│── data/
│ ├── raw/ # Raw API data (ignored in Git)
│ ├── processed/ # Clean CSVs for analysis (ignored in Git)
│── notebooks/
│ ├── 01_eda.ipynb # EDA: Historical vs. Live comparison
│── src/
│ ├── crp/
│ │ ├── data/
│ │ │ ├── fetch_openmeteo.py
│ │ │ ├── fetch_meteostat.py
│ │ │ ├── preprocess.py
│── .gitignore
│── README.md
│── environment.yml



---

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/aaitdads/climate-risk-platform.git
cd climate-risk-platform
```
### 2. Create environment
```bash
conda env create -f environment.yml
conda activate climate-risk
```
### 3. Register environment for Jupyter
```bash
python -m ipykernel install --user --name=climate-risk --display-name "Python (climate-risk)"
```

### 🔑 API Keys

Meteostat API (via RapidAPI) → put in .env as:
```bash
RAPIDAPI_KEY=your_key_here
```

Open-Meteo API → free, no key needed.

Never commit your .env file (it’s ignored by .gitignore).

## 🚀 Usage

Fetch data
# Live forecast from Open-Meteo
```bash
python src/crp/data/fetch_openmeteo.py --lat 48.8566 --lon 2.3522 --name paris
```
# Historical data from Meteostat
```bash
python src/crp/data/fetch_meteostat.py --lat 48.8566 --lon 2.3522 \
  --start 2024-01-01 --end 2024-12-31 --name paris --granularity both
```
# Preprocess into clean CSVs
```bash
python src/crp/data/preprocess.py --source openmeteo --file data/raw/open_meteo/paris_openmeteo_*.json --name paris_live
python src/crp/data/preprocess.py --source meteostat --file data/raw/meteostat/paris_meteostat_*.json --name paris_hist
```
# Run EDA

Open the notebook:

jupyter notebook notebooks/01_eda.ipynb

# 📊 Example Outputs

Historical Analysis: Long-term temperature and precipitation trends.

Live Forecast: Next 24h temperature and humidity predictions.

(plots will be added here)

# 🛠️ Roadmap

 Setup repo & environment

 Fetch Meteostat + Open-Meteo data

 Preprocessing pipeline

 EDA (historical vs live)

 Risk modeling (climate anomalies, heatwaves, floods)

 Dashboard (Streamlit / Dash)

 Deployment

# 👤 Author & Contact

AIT DADS AYMANE – Data Scientist

🌐 LinkedIn : https://www.linkedin.com/in/aymane-ait-dads/

📧 Aymane.Ait-dads@eurecom.fr

🐙 GitHub : https://github.com/aaitdads

# If you find this project useful or want to collaborate, feel free to connect with me!