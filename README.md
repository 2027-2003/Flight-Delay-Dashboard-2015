
✈️ Flight Delay Data Engineering & Analytics Dashboard
A high-performance interactive BI dashboard built with Streamlit to analyze and visualize over 5.8 million flight records from 2015. This project demonstrates end-to-end data handling, from raw ingestion to optimized visualization.

Data Engineering Architecture
This project implements a robust data pipeline designed for handling large-scale datasets efficiently:

Data Ingestion: Modular loading system using a dedicated load_data source module.

Memory Optimization: * Strict feature selection (dropping non-essential columns to reduce RAM footprint).

Type casting for categorical data (Airlines, Airport IDs) to ensure consistency.

Performance Layer: Leverages Streamlit Caching (@st.cache_data) to persist processed data in memory, significantly reducing re-computation time during user interactions.

Data Cleaning & Transformation:

Handling null values in high-variance delay columns.

Aggregating multi-million row datasets into performant business metrics (KPIs) in real-time.

Business Intelligence Features
KPI Tracking: Real-time calculation of Total Flights, Cancellation Rates, and Average Delays.

Multidimensional Analysis:

Temporal: Analysis of delays by Month and Day of the Week.

Geospatial/Logistics: Top 10 bottleneck origin airports and airline performance rankings.

Interactive Filtering: Dynamic sidebar allowing users to slice data by Airline and Date Range.

🛠️ Tech Stack
Language: Python 3.x

Processing: Pandas, NumPy

Dashboarding: Streamlit

Visualization: Matplotlib, Seaborn (Custom Dark-themed UI)
 
  Project Structure
Plaintext

├── src/
│   └── load_data.py      # Data ingestion logic & ETL functions
├── app.py                # Main Streamlit application & UI logic
├── requirements.txt      # Project dependencies
└── README.md             # Technical documentation
Getting Started
Clone the repository:

Bash

git clone https://github.com/mishal-username/flight-delay-analysis.git
Install dependencies:

Bash

pip install -r requirements.txt
Run the application:

Bash

streamlit run app.py
Engineering Insights (Roadmap)
Future iterations for this pipeline include:

Storage Migration: Moving from flat CSV files to Apache Parquet for columnar storage optimization.

Database Integration: Implementing a PostgreSQL or Snowflake backend for persistent storage.

Orchestration: Using Apache Airflow to automate the data cleaning and loading process.

Developed by Mishal Information Systems Student | Data Engineering Enthusiast
