# 🤖 IPL Automated Strategy & Prediction AI - V2

A fully automated AI agent that analyzes the past 2 years of IPL match data, connects to real APIs, scrapes deep micro-stats, and provides win probabilities, safe/value strategies, and promotional picks for decision-making.

---

## 🚀 Setup Guide

**1. Clone or Download the repository.**

**2. Set up the virtual environment & configure:**
```bash
python -m venv venv
.\venv\Scripts\activate   # On Windows
pip install -r requirements.txt
```

**3. API Integrations (Important):**
The system is built to use **CricAPI** and **OpenWeatherMap**. 
If you do not have API keys right now, **do not worry!** The systems have built-in realistic mock-fallback generation that acts essentially identically for testing the pipeline.
To insert your real keys, open `src/config.py` and modify:
```python
CRIC_API_KEY = "your_real_key_here"       # Get from cricapi.com
WEATHER_API_KEY = "your_real_key_here"    # Get from openweathermap.org
```

**4. Initialize the Data and Train the ML Model:**
Run the daily automation script to pull data (or generate mocks), build the SQLite database (`data/predictor.db`), engineer deep features, and train the Machine Learning engine.
```bash
python src/automation/updater.py
```

**5. Start the AI Dashboard:**
```bash
streamlit run src/app/dashboard.py
```

---

## 📊 Example Output (As seen on Dashboard)
```text
Match: CSK vs MI
Win Probability: CSK (64.5%) | MI (35.5%)

Safe Pick: CSK
Value Pick: MI
Promo Pick: MI (High first-over aggression)

Key Players:
- Player_CSK_1: Impact Score 9.2
- Player_MI_5: Impact Score 8.8

Risk Level: Low
```

---
*Disclaimer: This is an AI Probability Tool and does not guarantee gambling outcomes.*
