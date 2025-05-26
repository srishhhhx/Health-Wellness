import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import joblib            # works for either joblib or pickle dumps

# ───────────────────────────
# Page config
# ───────────────────────────
st.set_page_config(
    page_title="Wellness Calculator",
    page_icon="🌿",
    layout="wide"
)

# ───────────────────────────
# CSS tweaks
# ───────────────────────────
st.markdown("""
<style>
    .main > div { padding-top: 1rem; }
    .stMetric { background:#f8f9fa;padding:1rem;border-radius:.5rem;border:1px solid #e9ecef; }
    .metric-container, .gauge-container {
        background:#f8f9fa;padding:1.5rem;border-radius:.5rem;border:1px solid #e9ecef;
        height:400px;display:flex;flex-direction:column;
    }
    .metric-container { justify-content:space-between; }
    .gauge-container { justify-content:center;text-align:center; }
    .score-large { font-size:3rem;font-weight:bold;margin:1rem 0; }
    .score-excellent { color:#28a745; }
    .score-good      { color:#ffc107; }
    .score-poor      { color:#dc3545; }
</style>
""", unsafe_allow_html=True)

# ───────────────────────────
# Load Random-Forest model once per session
# ───────────────────────────
@st.cache_resource(show_spinner="Loading wellness model…")
def load_model():
    return joblib.load("models/model1.pkl")   # file sits next to app.py

rf_model = load_model()

# ───────────────────────────
# Helpers
# ───────────────────────────
def calculate_wellness_score(sleep_hours, steps, mood_rating):
    """
    Predict a 0-100 wellness score using the trained model.
    Column names must match exactly what was used during training.
    """
    X = pd.DataFrame(
        [[sleep_hours, steps, mood_rating]],
        columns=["Sleep", "Steps", "Mood"]  # ✔ exact match
    )
    score = rf_model.predict(X)[0]
    return round(float(score), 1)


def create_slick_gauge(score):
    """Return a Plotly half-circle gauge for the given score."""
    if score <= 40:
        color, status = "#ef4444", "Needs Attention"
    elif score <= 70:
        color, status = "#f59e0b", "Good Progress"
    else:
        color, status = "#10b981", "Excellent"

    fig = go.Figure(go.Indicator(
        mode   = "gauge+number",
        value  = score,
        title  = {'text': f"<b>{status}</b>",
                  'font': {'size': 22, 'color': '#1f2937'}},
        number = {'font': {'size': 54, 'color': color, 'family': 'Arial Black'},
                  'suffix': '<span style="font-size:24px;color:#6b7280">/100</span>'},
        gauge  = {
            'axis': {'range': [0, 100], 'tickwidth': 2,
                     'tickcolor': "#e5e7eb",
                     'tickfont': {'size': 12, 'color': '#6b7280'}},
            'bar': {'color': color, 'thickness': 0.25,
                    'line': {'color': '#ffffff', 'width': 2}},
            'bgcolor': "#ffffff",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 40],  'color': '#fef2f2'},
                {'range': [40, 70], 'color': '#fffbeb'},
                {'range': [70, 100],'color': '#ecfdf5'}
            ],
            'threshold': {'line': {'color': color, 'width': 6},
                          'thickness': 0.8, 'value': score},
        }
    ))

    fig.update_layout(
        height=350,
        margin=dict(l=30, r=30, t=60, b=30),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, Arial", size=14)
    )
    return fig

# ───────────────────────────
# UI
# ───────────────────────────
st.title("🌿 Wellness Calculator")
st.write("Track your daily wellness metrics")

col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown("### Your Metrics")
    sleep_hours = st.slider("Sleep Hours", 0.0, 12.0, 7.5, 0.5,
                             help="Recommended: 7-9 hours")
    steps       = st.slider("Daily Steps", 0, 25_000, 8_000, 500,
                             help="Recommended: 10 000+ steps")
    mood_rating = st.slider("Mood Rating", 1, 10, 7, 1,
                             help="1 = Very low, 10 = Excellent")

with col2:
    score = calculate_wellness_score(sleep_hours, steps, mood_rating)
    st.plotly_chart(create_slick_gauge(score),
                    use_container_width=True,
                    config={'displayModeBar': False})

# ───────────────────────────
# Footer / feedback
# ───────────────────────────
st.markdown("---")
if   score <= 40: st.error("🚨 Focus on improving your wellness habits")
elif score <= 70: st.warning("📈 You're making good progress!")
else:             st.success("🎉 Outstanding wellness habits!")

st.info("💡 **Tip:** Small daily improvements lead to significant wellness gains over time.")
st.caption("This calculator provides general wellness insights and should not replace professional medical advice.")
