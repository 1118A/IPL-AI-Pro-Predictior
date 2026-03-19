import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.model.predictor import MatchPredictor
from src.model.upcoming import get_proactive_predictions

st.set_page_config(page_title="IPL AI Pro Predictor", page_icon="🏏", layout="wide")

# PREMIUM CUSTOM CSS: Glassmorphism, Animations, Dark Theme Focus
st.markdown("""
<style>
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #161b22;
        border-radius: 8px 8px 0px 0px;
        color: white;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #238636 !important;
        font-weight: bold;
    }
    div.stButton > button {
        background-color: #238636;
        color: white;
        border-radius: 6px;
        border: 1px solid rgba(240, 246, 252, 0.1);
        padding: 5px 16px;
        font-weight: bold;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #2ea043;
        border-color: #8b949e;
        transform: scale(1.02);
    }
    .glass-card {
        background: rgba(22, 27, 34, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(10px);
    }
    .win-prob-title {
        font-size: 24px;
        font-weight: bold;
        color: #58a6ff;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 1.2rem;
        font-weight: bold;
        color: #3fb950;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: white; margin-bottom: 5px;'>🏏 IPL AI Strategy Engine</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8b949e; margin-bottom: 30px;'>Advanced predictive analytics powered by machine learning and real-time match context.</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔥 UPCOMING SCHEDULE (AUTO)", "⚙️ CUSTOM PREDICTOR"])

# ----------------- TAB 1: UPCOMING SCHEDULE -----------------
with tab1:
    st.markdown("<h3 style='color: white;'>Predicting Upcoming Scheduled Matches</h3>", unsafe_allow_html=True)
    
    if st.button("Fetch & Analyze Next Matches", key="auto_fetch"):
        with st.spinner("Connecting to Cricket APIs, fetching weather, and engaging Deep Learning Models..."):
            try:
                upcoming_data = get_proactive_predictions()
                if not upcoming_data:
                    st.warning("No upcoming matches found or error connecting to Database.")
                else:
                    for i, match_info in enumerate(upcoming_data):
                        pred = match_info['prediction']
                        weather = match_info['weather']

                        # Safe team name split
                        match_parts = pred['match'].split(" vs ", 1)
                        teamA = match_parts[0].strip() if len(match_parts) == 2 else pred['match']
                        teamB = match_parts[1].strip() if len(match_parts) == 2 else ''

                        # Safe probability access with float cast
                        prob_A = round(float(pred['probabilities'].get(teamA, 50.0)), 2)
                        prob_B = round(float(pred['probabilities'].get(teamB, 50.0)), 2)

                        # Safe key players access with fallback
                        kp = pred.get('key_players', [])
                        kp_html = ''.join(
                            f'<li>{p["name"]} (Score: {p["impact_score"]})</li>'
                            for p in kp[:2]
                        ) if kp else '<li>Player data not available for this match</li>'

                        risk_color = '#d73a49' if pred['risk_level'] == 'High' else '#dbab09' if pred['risk_level'] == 'Medium' else '#28a745'

                        st.markdown(f"""
                        <div class="glass-card">
                            <h2 style="color: white; margin-top:0;">{pred['match']}</h2>
                            <p style="color: #8b949e; margin-bottom: 20px;">
                                📅 <b>Date:</b> {match_info['date']} &nbsp;|&nbsp;
                                🏟️ <b>Venue:</b> {match_info['venue']} &nbsp;|&nbsp;
                                ☁️ <b>Weather:</b> {weather.get('condition','N/A')} ({weather.get('temp','?')}°C)
                            </p>
                            <hr style="border-color: rgba(255,255,255,0.1);"/>
                            <div class="win-prob-title">Win Probabilities</div>
                            <div style="display: flex; gap: 20px; margin-bottom: 15px;">
                                <div><span class="metric-label">{teamA}</span><br><span class="metric-value">{prob_A}%</span></div>
                                <div><span class="metric-label">{teamB}</span><br><span class="metric-value">{prob_B}%</span></div>
                            </div>
                            <hr style="border-color: rgba(255,255,255,0.1);"/>
                            <div style="display: flex; gap: 40px; margin-bottom: 20px;">
                                <div><span class="metric-label">Safe Pick</span><br><span style="color: white; font-weight: bold;">{pred['picks']['safe']}</span></div>
                                <div><span class="metric-label">Value Pick</span><br><span style="color: white; font-weight: bold;">{pred['picks']['value']}</span></div>
                                <div><span class="metric-label">Promo Pick</span><br><span style="color: white; font-weight: bold;">{pred['picks']['promo']}</span></div>
                            </div>
                            <span class="metric-label">Key Impact Players</span>
                            <ul style="color: #c9d1d9; margin-top: 5px;">{kp_html}</ul>
                            <div style="margin-top: 15px;">
                                <span style="background-color: rgba(255,255,255,0.1); padding: 5px 10px; border-radius: 4px; font-size: 0.9em; border-left: 4px solid {risk_color};">
                                    Investment Risk: <b>{pred['risk_level']}</b>
                                </span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            except Exception as e:
                import traceback
                st.error(f"Critical System Error: {str(e)}")
                st.code(traceback.format_exc())


# ----------------- TAB 2: CUSTOM PREDICTOR -----------------
with tab2:
    st.markdown("<h3 style='color: white;'>Custom Match Analysis</h3>", unsafe_allow_html=True)
    teams = ['CSK', 'MI', 'RCB', 'KKR', 'DC', 'RR', 'PBKS', 'SRH', 'GT', 'LSG']
    pitch_types = ['Batting Friendly', 'Bowling Friendly', 'Balanced', 'Spin Friendly']
    venue_sizes = ['Small', 'Medium', 'Large']
    weather_conditions = ['Clear', 'Cloudy', 'Rain Probable']

    col1, col2 = st.columns(2)

    with col1:
        teamA = st.selectbox("Select Team A", teams, index=0)
        teamB = st.selectbox("Select Team B", teams, index=1)
        toss_winner = st.selectbox("Toss Winner", [teamA, teamB])
        
    with col2:
        pitch_type = st.selectbox("Pitch Type", pitch_types)
        venue_size = st.selectbox("Venue Size", venue_sizes)
        weather_cond = st.selectbox("Weather Forecast", weather_conditions)

    if st.button("Generate Strategy Blueprint", use_container_width=True):
        if teamA == teamB:
            st.error("Please select two different teams for a match!")
        else:
            with st.spinner("Compiling Historical Analytics..."):
                try:
                    predictor = MatchPredictor()
                    result = predictor.predict(teamA, teamB, toss_winner, pitch_type, weather_cond, venue_size)

                    # Safe probability cast
                    prob_A = round(float(result['probabilities'].get(teamA, 50.0)), 2)
                    prob_B = round(float(result['probabilities'].get(teamB, 50.0)), 2)

                    # Safe key players with fallback
                    kp2 = result.get('key_players', [])
                    kp2_html = ''.join(
                        f'<li>{p["name"]} (Score: {p["impact_score"]})</li>'
                        for p in kp2[:2]
                    ) if kp2 else '<li>Player data not available</li>'

                    st.markdown(f"""
                        <div class="glass-card">
                            <h2 style="color: white; margin-top:0;">{result['match']}</h2>
                             <hr style="border-color: rgba(255,255,255,0.1);"/>
                             <div class="win-prob-title">Win Probabilities</div>
                             <div style="display: flex; gap: 20px; margin-bottom: 15px;">
                                 <div><span class="metric-label">{teamA}</span><br><span class="metric-value">{prob_A}%</span></div>
                                 <div><span class="metric-label">{teamB}</span><br><span class="metric-value">{prob_B}%</span></div>
                             </div>
                             <hr style="border-color: rgba(255,255,255,0.1);"/>
                            <div style="display: flex; gap: 40px; margin-bottom: 20px;">
                                <div><span class="metric-label">Safe Pick</span><br><span style="color: white; font-weight: bold;">{result['picks']['safe']}</span></div>
                                <div><span class="metric-label">Value Pick</span><br><span style="color: white; font-weight: bold;">{result['picks']['value']}</span></div>
                                <div><span class="metric-label">Promo Pick</span><br><span style="color: white; font-weight: bold;">{result['picks']['promo']}</span></div>
                            </div>
                             <span class="metric-label">Key Impact Players</span>
                             <ul style="color: #c9d1d9; margin-top: 5px;">{kp2_html}</ul>
                        </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    import traceback
                    st.error(f"Error generating strategy: {str(e)}")
                    st.code(traceback.format_exc())
