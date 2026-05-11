# ⚡ Smart-Ev-Site-Selection: Smart Investment Decision Tool
### Data-Driven Site Selection for EV Charging Networks using Databricks & PySpark

[![Databricks](https://img.shields.io/badge/Platform-Databricks-orange?style=flat-square&logo=databricks)](https://www.databricks.com/)
[![MLflow](https://img.shields.io/badge/MLOps-MLflow-blue?style=flat-square&logo=mlflow)](https://mlflow.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red?style=flat-square&logo=streamlit)](https://streamlit.io/)

---

## 📌 Project Overview
[cite_start]"ระบบจำลองกลยุทธ์และคัดกรองทำเลสถานีชาร์จ EV อัจฉริยะเพื่อลดความเสี่ยงให้นักลงทุน" [cite: 1]
[cite_start]An end-to-end data pipeline designed to find the **"Golden Gap"** (High Demand, Low Competition) for EV charging stations in Bangkok and its vicinity. [cite: 3, 4]

### 🚀 [Live Demo on Hugging Face Spaces](https://huggingface.co/spaces/DuckerMaster/EV_Site_Optimizer)

---

## 🏗️ Architecture: Medallion Framework
[cite_start]This project follows the **Medallion Architecture** to ensure high-quality data processing: [cite: 12]

1.  [cite_start]**Bronze (Ingestion):** Raw data from OSM Overpass API, WorldPop (Population), and World Bank (Flood Risk). [cite: 17, 18]
2.  [cite_start]**Silver (Processing):** Spatial snapping to 500m x 500m grids, Zonal classification (CBD/Urban), and feature engineering. [cite: 23, 26, 29]
3.  [cite_start]**Gold (Optimization):** Multi-scenario scoring and MLflow experiment tracking. [cite: 30, 31]

---

## 🧠 Business Simulation (MLflow Runs)
[cite_start]We compared 3 strategic scenarios to identify the most viable investment paths: [cite: 16, 50]
* [cite_start]**Run A: Aggressive Demand** (Focus on high footfall) [cite: 34]
* [cite_start]**Run B: Blue Ocean** (Focus on market gaps) [cite: 35]
* [cite_start]**Run C: Safe Play** (Focus on flood safety - **Best Performance**) [cite: 36, 37]

**Key Outcome:**
* [cite_start]**Golden Gap Locations:** 2,252 sites identified [cite: 50]
* [cite_start]**Best Payback Period:** 1.51 Years [cite: 50]
* [cite_start]**Silhouette Score:** 0.5920 (High cluster stability) [cite: 50]

---

## 🛠️ Financial & ROI Logic (NB04)
[cite_start]The system calculates a dynamic Payback Period based on zonal characteristics: [cite: 3, 37]
* [cite_start]**CBD:** +20% OpEx premium due to high rent. [cite: 39, 40]
* [cite_start]**Urban:** +5% Annual revenue growth from suburban expansion. [cite: 39, 40]

---

## 💻 Tech Stack
* [cite_start]**Compute:** Databricks Community Edition [cite: 11]
* [cite_start]**Engine:** PySpark (Distributed Processing) [cite: 12]
* [cite_start]**MLOps:** MLflow (Experiment Tracking & Model Registry) [cite: 12, 52]
* [cite_start]**Storage:** Delta Lake [cite: 12]
* [cite_start]**Visualization:** Folium & Streamlit [cite: 13, 43]

---
[cite_start]*Zero Cost Declaration: All tools and data used in this project are 100% Free/Open Source.* [cite: 57]
