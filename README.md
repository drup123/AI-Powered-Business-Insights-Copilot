# 🧠 AI-Powered Business Insights Copilot

An intelligent business analytics assistant that combines React.js, Python analytics, validation guardrails, and LLM-powered explanations to transform raw business datasets into actionable insights.

Built using React.js, Python, Pandas, Plotly, FastAPI, and Groq LLM, this project enables users to interact with business data through natural language queries and receive reliable, explainable business insights.

---

# 🚀 Features

## 📊 Business Analytics

* Sales Trend Analysis
* Marketing Impact Analysis
* ROI Analysis
* Region-wise Performance Analysis
* Marketing Channel Analysis
* Campaign Performance Analysis
* General Business Overview

## ⚛️ React-Based Frontend

* Responsive React.js dashboard
* Interactive business analytics interface
* Real-time API communication
* Dynamic chart rendering
* User-friendly analytics experience

## 🤖 AI-Powered Insights

* Natural language business queries
* Human-readable explanations generated using Groq LLM
* Structured and explainable insight generation

## 🛡️ Validation Guardrails

* Correlation strength validation
* Confidence scoring
* Weak-data detection
* Prevention of misleading conclusions

## 📈 Interactive Visualizations

* Dynamic Bar Charts
* Scatter Plots with Trendlines
* KPI Dashboard
* Comparative Analysis Charts

## 💬 Conversational Interface

* Chat-style interaction
* Quick question suggestions
* Analysis history tracking

---

# 🏗️ Architecture

User Query

↓

React.js Frontend

↓

FastAPI Backend

↓

Intent Detection

↓

Data Processing (Pandas)

↓

Validation & Guardrails

↓

Confidence Scoring

↓

Template-Based Insight

↓

Groq LLM Explanation

↓

Interactive Dashboard

---

## Controlled Hybrid Architecture

### React.js

Frontend Presentation Layer

### FastAPI

API Communication Layer

### Pandas

Truth Layer

### Python

Decision Logic & Guardrails

### Groq LLM

Human-Friendly Explanation Layer

This architecture ensures that all conclusions remain grounded in actual computed data while leveraging AI only for explanation.

---

# 🛠️ Tech Stack

| Technology  | Purpose                    |
| ----------- | -------------------------- |
| React.js    | Frontend Application       |
| FastAPI     | Backend APIs               |
| Python      | Business Logic             |
| Pandas      | Data Analysis              |
| Plotly      | Interactive Visualizations |
| Groq LLM    | AI Explanations            |
| Statsmodels | Trendline Analysis         |

---

# 📂 Project Structure

```text
AI-Powered-Business-Insights-Copilot/
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   └── services/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── data_layer.py
│   ├── intent_engine.py
│   ├── analysis_engine.py
│   ├── llm_layer.py
│   └── visualizations.py
│
├── requirements.txt
├── improved_business_dataset.csv
└── README.md
```

---

# 📌 Supported Queries

## Sales Analysis

* Which category has the highest sales?
* Show sales trends.
* Why did sales drop?

## Marketing Analysis

* Does marketing spend impact sales?
* What is the correlation between marketing and sales?

## ROI Analysis

* Which category has the highest ROI?
* Compare ROI across categories.

## Region Analysis

* Which region performs best?
* Show region-wise sales performance.

## Marketing Channel Analysis

* Which marketing channel gives the best ROI?

## Campaign Analysis

* Which campaign type performs best?

## General Overview

* Give me a business overview.

---

# 📊 Dashboard Highlights

## KPI Metrics

* Average Monthly Sales
* Average Marketing Spend
* Best ROI Category
* Highest ROI Value
* Marketing-Sales Correlation

## Visual Analytics

* Category Performance Charts
* ROI Comparison Charts
* Marketing Spend Analysis
* Scatter Plot Trend Analysis

## Insight Engine

* Data-Grounded Insights
* AI-Powered Explanations
* Confidence Levels
* Data Validation Warnings

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/AI-Powered-Business-Insights-Copilot.git
cd AI-Powered-Business-Insights-Copilot
```

## 2. Install Frontend Dependencies

```bash
cd frontend
npm install
npm run dev
```

## 3. Create Python Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

## 4. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

## 5. Configure Groq API

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

## 6. Run Backend

```bash
uvicorn app:app --reload
```

## 7. Run Frontend

```bash
npm run dev
```

---

# 🔍 Example Workflow

User asks:

> Which marketing channel gives the highest ROI?

Intent Detection identifies:

> CHANNEL_ANALYSIS

Analysis Engine computes:

* Average ROI by Marketing Channel
* Validation checks data quality
* Confidence score calculation

Groq generates:

* Business explanation
* Supporting insights

Dashboard displays:

* Data Table
* Interactive Charts
* Business Insights
* AI Explanation

---

# 🛡️ Reliability Features

## Correlation Guardrails

Blocks misleading conclusions when correlations are too weak.

## Confidence Scoring

Every insight is assigned:

* High Confidence
* Medium Confidence
* Low Confidence

## Explainable AI

The LLM receives only structured summaries and computed statistics, ensuring explanations remain grounded in actual data.

---

# 🎯 Future Enhancements

* Time-Series Forecasting
* Dataset Upload Support
* PDF Report Generation
* Advanced Business KPIs
* User Authentication
* Multi-Dataset Analytics
* Real-Time Dashboard Updates

---

# 👨‍💻 Author

**Drup Patil**

B.Tech Artificial Intelligence & Machine Learning

---

# ⭐ Support

If you found this project useful, consider giving it a Star ⭐ on GitHub and sharing it with others.

Made with ❤️ using React.js, Python, FastAPI, Plotly, and Groq AI.
