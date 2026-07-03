# 🛒 OmniMarket - Autonomous AI Market Intelligence Platform

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-Interactive%20Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Gemini-AI%20Powered-orange?style=for-the-badge&logo=google&logoColor=white"/>
  <img src="https://img.shields.io/badge/API-Live%20Data%20Injection-success?style=for-the-badge"/>
</p>

---

## 🚀 Overview

**OmniMarket** is an AI-powered market intelligence and autonomous data analytics platform designed to transform raw live market data into actionable business insights.

The system fetches real-time product information from external APIs, automatically constructs datasets, and enables users to perform advanced analytics using natural language commands.

Powered by **Google Gemini**, the platform autonomously generates, executes, and refines Python code to answer analytical queries, perform data cleaning, engineer features, and create visualizations.

---

## ✨ Features

### 🌐 Live API Data Ingestion

* Connects to external APIs for real-time market data.
* Dynamically generates datasets from live sources.
* Handles network failures and malformed responses gracefully.

### 🤖 Autonomous AI Analyst

* Powered by **Gemini 2.5 Flash**.
* Converts natural language requests into executable Python code.
* Self-corrects execution failures through iterative retry mechanisms.

### 📊 Intelligent Data Analytics

* Exploratory Data Analysis (EDA)
* Data Cleaning
* Feature Engineering
* Statistical Analysis
* Business Insight Generation

### 📈 Automated Visualizations

Generate charts automatically using simple prompts:

* Histograms
* Bar Charts
* Boxplots
* Scatter Plots
* Correlation Analysis
* Trend Visualizations

### 💾 Persistent Analytical Workspace

* Every transformation is saved automatically.
* Maintains dataset state throughout the session.
* Allows users to continue analysis without losing progress.

### 🎨 Interactive Dashboard

* Dataset Preview
* KPI Summary Cards
* Schema Viewer
* Analytical Timeline
* Downloadable Outputs

---

## 🏗️ System Architecture

```text
              External APIs
                     │
                     ▼
         Live Data Injection Layer
                     │
                     ▼
          Dynamic Dataset Creation
                     │
                     ▼
        Persistent Working Dataset
                     │
                     ▼
          Gemini Autonomous Agent
                     │
                     ▼
         Python Code Generation
                     │
                     ▼
         Secure Execution Sandbox
                     │
                     ▼
 Insights + Visualizations + Reports
```

---

## 🛠️ Tech Stack

| Technology        | Purpose                     |
| ----------------- | --------------------------- |
| Python            | Core Development            |
| Streamlit         | Interactive Web Application |
| Pandas            | Data Manipulation           |
| Google Gemini API | AI Reasoning Engine         |
| Matplotlib        | Data Visualization          |
| Seaborn           | Statistical Charts          |
| JSON              | Data Parsing                |
| urllib            | API Communication           |

---

## 📂 Project Structure

```bash
📦 OmniMarket
│
├── app.py                    # Main Streamlit Application
├── project1.py              # Live API ingestion pipeline
├── my_project.ipynb         # Development notebook
├── project1.ipynb           # Experimentation notebook
├── agent_working_dataset.csv
├── output_chart.png
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/OmniMarket.git

cd OmniMarket
```

### Install Dependencies

```bash
pip install streamlit pandas matplotlib seaborn google-genai
```

---

## 🔑 Configure API Key

Add your Gemini API Key:

```python
import os

os.environ["GEMINI_API_KEY"] = "YOUR_API_KEY"
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---

## 💡 Example Queries

```text
Clean missing values in the dataset.

Show the top 10 brands.

Generate a boxplot for product distribution.

Create a new feature called Profit Margin.

Display correlation between numerical variables.

Identify duplicate records and remove them.
```

---

## 🎯 Key Learnings

Through this project, I gained practical experience in:

* AI Agent Development
* Prompt Engineering
* API Integration
* Real-Time Data Pipelines
* Autonomous Code Generation
* Data Analytics Automation
* Streamlit Application Development
* Secure Code Execution
* Error Handling & Recovery
* Interactive Dashboard Design

---

## 🔮 Future Enhancements

* Multi-Agent Collaboration
* SQL Database Integration
* Report Generation (PDF/Excel)
* Cloud Deployment
* User Authentication
* RAG-based Business Intelligence
* Voice-enabled Analytics
* Advanced Forecasting Models

---

## 👨‍💻 Author

**Devika Dasari**

*Aspiring Data Analyst | AI Enthusiast | Building Intelligent Data Products*

---

⭐ If you found this project useful, don't forget to **star the repository**!
