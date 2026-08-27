# 💧 AI-Powered Groundwater Planner
### *Saving Lahore's Water — One Drop at a Time* 🌊

[![Made with Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Powered by Gemini](https://img.shields.io/badge/Powered%20by-Gemini%20AI-4285F4?logo=google&logoColor=white)](https://ai.google.dev)
[![Hackathon](https://img.shields.io/badge/Smart%20City%20Hackathon-2026-1f6f8b)](https://smartcityhackathon.devpost.com)

📊 **View the pitch deck:** [AI-Powered-Groundwater-Planner.pdf](./AI-Powered-Groundwater-Planner.pdf)
🚀 **Live demo:** _[ Streamlit app link here ](https://hj7jncivzeudjokhaiyph5.streamlit.app/)_

---

## 🚨 The Problem

Lahore's groundwater is disappearing fast — and most people can't see it happening.

| ⏰ 20 Years Ago | 📉 Today | ⚠️ By 2040 |
|---|---|---|
| Water was just **31 ft** deep | Now **79 ft** deep, and falling | Could have **no accessible groundwater** left |

- 🏙️ **Gulberg** has gone from ~125 ft to over **300 ft** — some pockets as deep as **800 ft**
- 📈 Lahore's decline rate (**2.5–4 ft/year**) is the highest of any district in Punjab
- 💧 Withdrawal already exceeds natural recharge by **~15%**
- 🌧️ **36 billion litres** of rainwater is wasted into drains every year, uncaptured

---

## 💡 My Solution

An AI-powered planning tool that turns raw risk data into action:

| Feature | What it does |
|---|---|
| 🗺️ **Risk Map** | Interactive map of Lahore townships, color-coded by groundwater risk |
| 🔮 **AI Recharge Planner** | Pick a town + plot size → Gemini AI generates a real, grounded action plan |
| 📊 **Data Insights** | Charts showing risk severity by town + historical water table decline trend |
| 🌐 **Bilingual Output** | Get results in English, Urdu, or both |

Each AI-generated plan comes in **3 clear parts**:
1. 💧 **Recharge Well & Rainwater Harvesting Design**
2. 📐 **Proposed Layout & Sizing Guidance**
3. 📋 **Policy Summary**

---

## ⚙️ How It Works

```
📡 Collect Data  →  🤖 Feed to AI  →  🗺️ Generate Map  →  🏙️ City Planning
```

1. Town-level risk data (from cited public reports & research) loads from an Excel file
2. Towns are plotted on an interactive Folium map, color-coded by risk level
3. User selects a town, plot size, and language
4. The app sends that town's real data + city-wide facts to **Google Gemini** as grounding context
5. Gemini returns a structured plan (JSON) → rendered as three separate, easy-to-read cards

---

## 🏆 Why This Matters

| 🕐 10+ | 💧 36B | 🌍 100+ |
|---|---|---|
| Extra years of usable water for Lahore | Litres of rainwater that could be captured yearly | Other water-stressed cities this approach could scale to |

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **AI:** Google Gemini API (`google-genai`)
- **Maps:** Folium / streamlit-folium
- **Charts:** Plotly
- **Data:** Pandas, Excel (openpyxl)

## 📚 Data Sources

Compiled from public reporting and published research: Express Tribune, Dawn, Daily Times, ScienceDirect, and OSTI/IAEA groundwater studies. Full source notes are in `lahore_groundwater_risk_data.xlsx` under the "Read Me" tab.

---

## 🚀 Running Locally

```bash
# 1. Clone this repo and open the folder
# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\Activate.ps1      # Windows PowerShell

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your Gemini API key
#    Copy .env.example to .env and paste your key inside

# 5. Run the app
streamlit run app.py
```

## ☁️ Deploying on Streamlit Community Cloud

1. Push this repo to GitHub ✅ (already done!)
2. Go to [share.streamlit.io](https://share.streamlit.io) → sign in with GitHub
3. Click **"New app"** → select this repo → set `app.py` as the main file
4. Under **Advanced settings → Secrets**, add:
   ```
   GEMINI_API_KEY = "your_key_here"
   ```
5. Click **Deploy** 🚀 — get a shareable public link for judges

---

## 📁 Project Files

| File | Purpose |
|---|---|
| `app.py` | Main Streamlit application |
| `lahore_groundwater_risk_data.xlsx` | Town-level risk data + city-wide facts |
| `requirements.txt` | Python dependencies |
| `AI-Powered-Groundwater-Planner.pdf` | 📊 Pitch deck / presentation |

---

## 🙋‍♀️ Submission

Built solo 💪 for the **Smart City Hackathon 2026** — Lahore Garrison University, hosted by **Code for Pakistan** 🇵🇰

**Theme:** City Intelligence 🏙️
