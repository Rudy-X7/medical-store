# 💊 Medical Store Data Engineering Pipeline & Analytics Dashboard

## 📌 Overview

This project is an end-to-end **Data Engineering Pipeline** for a medical store system. It simulates real-world pharmacy data, processes it using batch pipelines, and visualizes insights through an interactive dashboard.

The project combines:

* Data Generation
* Data Processing (ETL)
* Workflow Orchestration (Airflow)
* Data Visualization (Streamlit)

---

## 🚀 Features

* 🔄 **Automated Data Pipeline**

  * Data generation using Python scripts
  * Data cleaning and transformation

* ⚙️ **Airflow DAG**

  * Scheduled pipeline execution
  * Task orchestration (`generate_data → clean_data`)

* 📊 **Interactive Dashboard**

  * KPI Metrics (Revenue, Orders, Avg Order)
  * Filters (City, Month, Medicine)
  * Sales Trends
  * Top-selling medicines
  * Scatter analysis (Price vs Quantity)

* 🎨 **Modern UI**

  * Dark theme with gradient background
  * Styled KPI cards
  * Interactive Plotly charts

---

## 🏗️ Project Structure

```
medical-store/
│
├── airflow_dags/
│   └── medical_pipeline_dag.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── scripts/
│   ├── ingestion/
│   │   └── generate_data.py
│   └── processing/
│       └── clean_data.py
│
├── dashboard.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Tech Stack

* **Python** (Pandas)
* **Apache Airflow**
* **Streamlit**
* **Plotly**
* **Git & GitHub**

---

## 🔄 Pipeline Workflow

```
Generate Data → Clean Data → Store Processed Data → Visualize in Dashboard
```

---

## 📊 Dashboard Insights

* 💰 Revenue Analysis
* 🏆 Top Selling Medicines
* 📍 City-wise Performance
* 📈 Sales Trends Over Time
* 🔵 Price vs Demand Relationship

---

## ▶️ How to Run Locally

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/medical-store.git
cd medical-store
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Run Data Pipeline

```bash
python scripts/ingestion/generate_data.py
python scripts/processing/clean_data.py
```

---

### 4. Start Dashboard

```bash
streamlit run dashboard.py
```

---

### 5. Run Airflow (Optional)

```bash
airflow scheduler
airflow webserver --port 8080
```

---

## 🌐 Live Demo

https://medical-store-oa7ngbpuaqwebmanap2csj.streamlit.app/

---


---

## ⭐ Unique Points

* Combines **Data Engineering + Analytics**
* Uses **Airflow for orchestration**
* Implements **interactive filtering & visualization**
* Clean modular pipeline design
* Realistic synthetic dataset generation

---

## 🚀 Future Improvements

* 🔄 Kafka for real-time streaming
* ⚡ Spark for distributed processing
* ☁️ Cloud deployment (AWS/GCP)
* 🤖 Machine Learning (sales prediction)
* 📊 Power BI / advanced UI

---

## 🧠 Learning Outcomes

* Building end-to-end data pipelines
* Working with Airflow DAGs
* Designing dashboards for analytics
* Handling real-world data scenarios

---

## 👨‍💻 Author

**Rudraksh Gautam**

---

## 📜 License

This project is for educational purposes.
