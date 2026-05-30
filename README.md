# 🧠 AI-Powered-Business-Insights-Copilot

An intelligent business analytics assistant that combines **data-driven analytics**, **validation guardrails**, and **LLM-powered explanations** to transform raw business datasets into actionable insights.

Built using **Python, Streamlit, Pandas, Plotly, and Groq LLM**, this project enables users to interact with business data through natural language queries and receive reliable, explainable insights.

---

## 🚀 Features

### 📊 Business Analytics

* Sales Trend Analysis
* Marketing Impact Analysis
* ROI Analysis
* Region-wise Performance Analysis
* Marketing Channel Analysis
* Campaign Performance Analysis
* General Business Overview

### 🤖 AI-Powered Insights

* Natural language business queries
* Human-readable explanations generated using Groq LLM
* Structured and explainable insight generation

### 🛡️ Validation Guardrails

* Correlation strength validation
* Confidence scoring
* Weak-data detection
* Prevention of misleading conclusions

### 📈 Interactive Visualizations

* Dynamic Bar Charts
* Scatter Plots with Trendlines
* KPI Dashboard
* Comparative Analysis Charts

### 💬 Conversational Interface

* Chat-style interaction
* Quick question suggestions
* Analysis history tracking

---

## 🏗️ Architecture

```text
User Query
     │
     ▼
Intent Detection
     │
     ▼
Data Processing (Pandas)
     │
     ▼
Validation & Guardrails
     │
     ▼
Confidence Scoring
     │
     ▼
Template-Based Insight
     │
     ▼
Groq LLM Explanation
     │
     ▼
Interactive Dashboard
```

### Controlled Hybrid Architecture

```text
Pandas  → Truth Layer
Python  → Decision Logic & Guardrails
Groq    → Human-Friendly Explanation Layer
```

This architecture ensures that all conclusions remain grounded in actual computed data while leveraging AI only for explanation.

---

## 🛠️ Tech Stack

| Technology  | Purpose                    |
| ----------- | -------------------------- |
| Python      | Backend Logic              |
| Streamlit   | Web Application            |
| Pandas      | Data Analysis              |
| Plotly      | Interactive Visualizations |
| Groq LLM    | AI Explanations            |
| Statsmodels | Trendline Analysis         |

---

## 📂 Project Structure

```text
AI-Powered-Business-Insights-Copilot/
│
├── app.py
├── config.py
├── data_layer.py
├── intent_engine.py
├── analysis_engine.py
├── llm_layer.py
├── visualizations.py
├── requirements.txt
├── improved_business_dataset.csv
└── README.md
```

---

## 📌 Supported Queries

### Sales Analysis

```text
Which category has the highest sales?
Show sales trends.
Why did sales drop?
```

### Marketing Analysis

```text
Does marketing spend impact sales?
What is the correlation between marketing and sales?
```

### ROI Analysis

```text
Which category has the highest ROI?
Compare ROI across categories.
```

### Region Analysis

```text
Which region performs best?
Show region-wise sales performance.
```

### Marketing Channel Analysis

```text
Which marketing channel gives the best ROI?
```

### Campaign Analysis

```text
Which campaign type performs best?
```

### General Overview

```text
Give me a business overview.
```

---

## 📊 Dashboard Highlights

### KPI Metrics

* Average Monthly Sales
* Average Marketing Spend
* Best ROI Category
* Highest ROI Value
* Marketing-Sales Correlation

### Visual Analytics

* Category Performance Charts
* ROI Comparison Charts
* Marketing Spend Analysis
* Scatter Plot Trend Analysis

### Insight Engine

* Data-Grounded Insights
* AI-Powered Explanations
* Confidence Levels
* Data Validation Warnings

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/AI-Powered-Business-Insights-Copilot.git

cd AI-Powered-Business-Insights-Copilot
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Groq API

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

### 5. Add Dataset

Place your dataset file:

```text
improved_business_dataset.csv
```

Required Columns:

```text
Category
monthly_sales
marketing_spend
ROI
Region
Marketing_Channel
Campaign_Type
```

### 6. Run Application

```bash
streamlit run app.py
```

---

## 🔍 Example Workflow

1. User asks:

```text
Which marketing channel gives the highest ROI?
```

2. Intent Detection identifies:

```text
CHANNEL_ANALYSIS
```

3. Analysis Engine computes:

```text
Average ROI by Marketing Channel
```

4. Validation checks data quality.

5. Confidence score is calculated.

6. Groq generates a concise explanation.

7. Dashboard displays:

   * Data Table
   * Charts
   * Insights
   * AI Explanation

---

## 🛡️ Reliability Features

### Correlation Guardrails

Blocks misleading conclusions when correlations are too weak.

### Confidence Scoring

Every insight is assigned:

* High Confidence
* Medium Confidence
* Low Confidence

### Explainable AI

The LLM receives only structured summaries and computed statistics, ensuring explanations remain grounded in actual data.

---

## 🎯 Future Enhancements

* Time-Series Forecasting
* Dataset Upload Support
* PDF Report Generation
* Advanced Business KPIs
* User Authentication
* Multi-Dataset Analytics
* Real-Time Dashboard Updates

---

## 👨‍💻 Author

**Drup Patil**

B.Tech Artificial Intelligence & Machine Learning



## ⭐ Support

If you found this project useful, consider giving it a **Star ⭐** on GitHub and sharing it with others.

---

### Made with ❤️ using Python, Streamlit, Plotly, and Groq AI
