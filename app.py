"""
Lahore Groundwater & Rainwater Harvesting Planner
--------------------------------------------------
Ye app 3 kaam karti hai:
1. Excel file se Lahore ke towns ka groundwater risk data load karti hai
2. Un towns ko ek interactive map (Folium) par color-coded dikhati hai
3. User jab koi town select kare, Gemini AI us town ke real data ke
   context ke sath ek "recharge well design + policy summary" generate karti hai
"""

import os
import json
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from google import genai
from dotenv import load_dotenv
import plotly.graph_objects as go

# ---------- STEP 1: Setup ----------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="Lahore Groundwater Planner",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Custom styling (isse UI professional lagti hai) ----------
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #0b3d59 0%, #1f6f8b 100%);
        padding: 1.8rem 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .main-header h1 { margin: 0; font-size: 1.9rem; }
    .main-header p { margin: 0.3rem 0 0 0; opacity: 0.9; }
    div[data-testid="stMetric"] {
        background-color: #f4f8fa;
        border: 1px solid #dbe8ee;
        border-radius: 10px;
        padding: 0.8rem;
    }
    div[data-testid="stMetric"] * {
        color: #0b3d59 !important;
    }
    button[data-testid="stNumberInputStepDown"],
    button[data-testid="stNumberInputStepUp"] {
        display: none !important;
    }
    .result-card {
        background-color: #f8fbfc;
        border-left: 4px solid #1f6f8b;
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>💧 Lahore Groundwater & Rainwater Harvesting Planner</h1>
    <p>AI-powered aquifer risk map + recharge planning tool — Smart City Hackathon 2026</p>
</div>
""", unsafe_allow_html=True)

# ---------- STEP 2: Data load karo ----------
DATA_FILE = "lahore_groundwater_risk_data.xlsx"

@st.cache_data
def load_data():
    towns_df = pd.read_excel(DATA_FILE, sheet_name="Lahore Groundwater Risk")
    facts_df = pd.read_excel(DATA_FILE, sheet_name="City-Wide Facts")
    return towns_df, facts_df

try:
    towns_df, facts_df = load_data()
except FileNotFoundError:
    st.error(f"'{DATA_FILE}' nahi mili. Ye file app.py wale folder me hona chahiye.")
    st.stop()

risk_colors = {
    "Critical": "darkred",
    "High": "orange",
    "Medium-High": "beige",
    "Low-Medium": "lightgreen",
    "Low": "green",
}

# ---------- STEP 3: Key stats row (top) ----------
critical_count = (towns_df["Risk Level"] == "Critical").sum()
high_count = towns_df["Risk Level"].isin(["Critical", "High"]).sum()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Towns Tracked", len(towns_df))
m2.metric("High/Critical Risk Zones", int(high_count))
m3.metric("Avg. Decline Rate", "2.5–4 ft/yr")
m4.metric("Projected Depletion", "by 2040")

st.divider()

# ---------- STEP 4: Sidebar — legend + about ----------
with st.sidebar:
    st.subheader("🗺️ Risk Legend")
    for level, color in risk_colors.items():
        st.markdown(
            f'<span style="color:{color}; font-size:1.3rem;">●</span> {level}',
            unsafe_allow_html=True,
        )
    st.divider()
    st.subheader("ℹ️ About")
    st.caption(
        "Data compiled from public reporting & research (Express Tribune, "
        "Dawn, Daily Times, ScienceDirect, OSTI/IAEA). See the Excel 'Read Me' "
        "tab for full source notes and confidence levels."
    )

# ---------- STEP 5: Map + Generator side by side ----------
col1, col2 = st.columns([1.3, 1])

with col1:
    st.subheader("Risk Map — Lahore Townships")
    m = folium.Map(location=[31.52, 74.33], zoom_start=11, tiles="OpenStreetMap")

    for _, row in towns_df.iterrows():
        color = risk_colors.get(row["Risk Level"], "gray")
        folium.CircleMarker(
            location=[row["Approx Lat"], row["Approx Lon"]],
            radius=11,
            popup=folium.Popup(
                f"<b>{row['Town/Area']}</b><br>Risk: {row['Risk Level']}<br>{row['Groundwater Finding']}",
                max_width=280,
            ),
            tooltip=row["Town/Area"],
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
            weight=2,
        ).add_to(m)

    st_folium(m, width=700, height=480)

with col2:
    st.subheader("🔮 Recharge Plan Generator")
    selected_town = st.selectbox("Select town:", towns_df["Town/Area"].tolist())
    land_size = st.number_input("Plot/land size (square feet)", min_value=100, value=1000, step=100)
    output_language = st.radio(
        "Output language:",
        ["English", "Urdu", "English + Urdu (Bilingual)"],
        horizontal=True,
    )

    town_row = towns_df[towns_df["Town/Area"] == selected_town].iloc[0]
    st.info(f"**{selected_town}** — Risk: **{town_row['Risk Level']}**\n\n{town_row['Groundwater Finding']}")

    generate = st.button("Generate Recharge & Policy Plan", type="primary", use_container_width=True)

    if generate:
        if not api_key:
            st.error("GEMINI_API_KEY not found. Check your .env file.")
        else:
            facts_text = "\n".join(
                f"- {r['Metric']}: {r['Value']}" for _, r in facts_df.iterrows()
            )

            language_instruction = {
                "English": "Write everything in English.",
                "Urdu": "Write everything in Urdu script (اردو).",
                "English + Urdu (Bilingual)": (
                    "For every section, first give the content in English, then repeat the "
                    "same content in Urdu script (اردو) directly below it, clearly labeled."
                ),
            }[output_language]

            prompt = f"""
You are an urban water-management assistant helping plan groundwater recharge
solutions for Lahore, Pakistan.

Selected area: {town_row['Town/Area']}
Risk level: {town_row['Risk Level']}
Local finding: {town_row['Groundwater Finding']}
Plot size: {land_size} square feet

City-wide facts for context:
{facts_text}

{language_instruction}

Respond ONLY with a valid JSON object (no markdown code fences, no extra text)
with exactly these three keys:

- "recharge_design": A short, practical write-up of a recharge well &
  rainwater harvesting approach sized roughly for this plot. Use general
  engineering guidance, not exact certified specs, since this is a hackathon
  prototype.
- "layout_sizing": A short, practical write-up proposing a rough layout and
  sizing guidance for fitting this on the given plot size (e.g. how much area
  a recharge pit or harvesting tank might reasonably occupy).
- "policy_summary": 3-4 bullet points (as a single string with line breaks)
  that a resident or developer in this area should know, referencing the real
  risk context above.

Keep each section concise and clearly grounded in the facts given above.
Use simple, everyday words — avoid technical jargon so a general reader can
easily understand it.
"""
            with st.spinner("Generating recharge plan..."):
                try:
                    client = genai.Client(api_key=api_key)
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt,
                        config={"response_mime_type": "application/json"},
                    )
                    raw_text = getattr(response, "text", None)

                    if raw_text and raw_text.strip():
                        try:
                            data = json.loads(raw_text)
                        except json.JSONDecodeError:
                            st.warning("The model's response wasn't valid JSON. Showing raw output below:")
                            st.write(raw_text)
                            data = None

                        if data:
                            st.session_state["plan_data"] = data
                    else:
                        st.warning("The model returned an empty response. Raw response below for debugging:")
                        st.write(response)
                except Exception as e:
                    st.error(f"Could not get a response from the AI: {e}")

    if "plan_data" in st.session_state:
        data = st.session_state["plan_data"]

        st.markdown("#### 💧 Recharge Design")
        with st.container(border=True):
            st.markdown(data.get("recharge_design", "Not available."))

        st.markdown("#### 📐 Layout & Sizing")
        with st.container(border=True):
            st.markdown(data.get("layout_sizing", "Not available."))

        st.markdown("#### 📋 Policy Summary")
        with st.container(border=True):
            st.markdown(data.get("policy_summary", "Not available."))

st.divider()
st.subheader("📈 Data Insights")

chart1, chart2 = st.columns(2)

with chart1:
    severity_map = {"Critical": 5, "High": 4, "Medium-High": 3, "Low-Medium": 2, "Low": 1}
    chart_df = towns_df.copy()
    chart_df["Severity Score"] = chart_df["Risk Level"].map(severity_map)
    chart_df = chart_df.sort_values("Severity Score", ascending=True)

    fig_bar = go.Figure(go.Bar(
        x=chart_df["Severity Score"],
        y=chart_df["Town/Area"],
        orientation="h",
        marker_color=[risk_colors.get(r, "gray") for r in chart_df["Risk Level"]],
        text=chart_df["Risk Level"],
        textposition="auto",
    ))
    fig_bar.update_layout(
        title="Groundwater Risk by Town",
        xaxis_title="Risk severity (1 = Low, 5 = Critical)",
        yaxis_title="",
        height=420,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with chart2:
    years_recorded = [2004, 2024]
    depth_recorded = [31, 79]
    yearly_rate = (depth_recorded[1] - depth_recorded[0]) / (years_recorded[1] - years_recorded[0])
    projected_2040 = depth_recorded[1] + yearly_rate * (2040 - years_recorded[1])

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=years_recorded, y=depth_recorded, mode="lines+markers",
        name="Recorded", line=dict(color="#1f6f8b", width=3), marker=dict(size=9),
    ))
    fig_line.add_trace(go.Scatter(
        x=[years_recorded[1], 2040], y=[depth_recorded[1], projected_2040], mode="lines+markers",
        name="Projected (if trend continues)", line=dict(color="#e36c09", width=3, dash="dash"),
    ))
    fig_line.update_layout(
        title="Lahore Water Table Depth — Trend & Projection",
        xaxis_title="Year",
        yaxis_title="Depth to water table (ft)",
        height=420,
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(fig_line, use_container_width=True)

st.caption(
    "Bar chart reflects town-level risk classification from the dataset. "
    "Line chart's 2004 and 2024 points are from cited reports; the dashed "
    "segment is a straight-line extrapolation for illustration, not an official projection."
)

st.divider()
st.caption(
    "Data source: public news reporting & published groundwater research "
    "(Express Tribune, Dawn, Daily Times, ScienceDirect, OSTI/IAEA) — see Excel 'Read Me' tab for details."
)