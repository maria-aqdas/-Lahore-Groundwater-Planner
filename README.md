# 💧 Lahore Groundwater & Rainwater Harvesting Planner

**Smart City Hackathon 2026 — Devpost / Code for Pakistan**
Theme: City Intelligence

## The Problem

Lahore's groundwater is disappearing fast, and most residents can't see it happening.

- The city's water table dropped from **31 ft to 79 ft** deep between 2004–2024 (a 48 ft drop in 20 years)
- Some areas like **Gulberg** have gone from ~125 ft to over **300 ft**, with pockets as deep as 800 ft
- Lahore's decline rate (2.5–4 ft/year) is the highest of any district in Punjab
- Annual withdrawal already exceeds natural recharge by ~15%
- If the trend continues, studies project the city could run out of accessible groundwater by **2040**

Meanwhile, ~36 billion litres of rainwater is wasted into drains every year instead of being captured.

## The Solution

An AI-powered planning tool that:
1. **Visualizes risk** — an interactive map of Lahore townships color-coded by groundwater risk level
2. **Generates a recharge plan** — select any town and plot size, and Gemini AI generates a practical, three-part plan grounded in real cited data:
   - Recharge Well & Rainwater Harvesting Design
   - Proposed Layout & Sizing Guidance
   - Policy Summary
3. **Visual insights** — charts showing risk severity by town and the city's historical water table decline trend

## How It Works

1. Town-level risk data (compiled from public news reporting and research) is loaded from an Excel file
2. Towns are plotted on an interactive Folium map, color-coded by risk
3. User selects a town + plot size + language (English / Urdu / Bilingual)
4. The app sends the town's real data + city-wide facts to Google's Gemini API as grounding context
5. Gemini returns a structured plan (JSON), which is displayed as three separate cards

## Tech Stack

- **Frontend:** Streamlit
- **AI:** Google Gemini API (`google-genai`)
- **Maps:** Folium / streamlit-folium
- **Charts:** Plotly
- **Data:** Pandas, Excel (openpyxl)

## Data Sources

Compiled from public reporting and published research: Express Tribune, Dawn, Daily Times, ScienceDirect, and OSTI/IAEA groundwater studies. Full source notes are in the `lahore_groundwater_risk_data.xlsx` file's "Read Me" tab.

## Running Locally

1. Clone this repo and open the folder
2. Create a virtual environment and activate it
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_key_here
   ```
5. Run the app:
   ```
   streamlit run app.py
   ```

## Deploying on Streamlit Community Cloud

1. Push this repo to GitHub (see steps below)
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click "New app", select this repo and `app.py` as the main file
4. Under "Advanced settings" → "Secrets", add:
   ```
   GEMINI_API_KEY = "your_key_here"
   ```
5. Deploy — Streamlit will give you a public link to share with judges

## Project Files

- `app.py` — main Streamlit application
- `lahore_groundwater_risk_data.xlsx` — town-level risk data + city-wide facts
- `requirements.txt` — Python dependencies
- `docs/pitch-deck.pdf` — presentation deck (add your exported Gamma deck here)

## Submission

Built solo for the Smart City Hackathon 2026 (Lahore Garrison University, hosted by Code for Pakistan).
