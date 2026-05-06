import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Zepto Customer Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #6C63FF; }
    .metric-label { font-size: 0.9rem; color: #888; margin-top: 4px; }
    .section-title { font-size: 1.2rem; font-weight: 600; color: #333; margin-bottom: 12px; }
    h1 { color: #6C63FF !important; }
</style>
""", unsafe_allow_html=True)

# ── Load Data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel("Zepto_Dataset.xlsx", parse_dates=["created_date"])
    df["year"]  = df["created_date"].dt.year
    df["month"] = df["created_date"].dt.to_period("M").astype(str)
    df["age_group"] = pd.cut(
        df["age"],
        bins=[17, 25, 35, 45, 60],
        labels=["18–25", "26–35", "36–45", "46–60"]
    )
    return df

df = load_data()

# ── Sidebar Filters ──────────────────────────────────────────────────────────
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Zepto_logo.svg/320px-Zepto_logo.svg.png", width=150)
st.sidebar.title("🔍 Filters")

years = sorted(df["year"].unique())
sel_years = st.sidebar.multiselect("Year", years, default=years)

states = sorted(df["state"].unique())
sel_states = st.sidebar.multiselect("State", states, default=states)

genders = sorted(df["gender"].unique())
sel_gender = st.sidebar.multiselect("Gender", genders, default=genders)

age_min, age_max = int(df["age"].min()), int(df["age"].max())
sel_age = st.sidebar.slider("Age Range", age_min, age_max, (age_min, age_max))

# ── Apply Filters ────────────────────────────────────────────────────────────
fdf = df[
    df["year"].isin(sel_years) &
    df["state"].isin(sel_states) &
    df["gender"].isin(sel_gender) &
    df["age"].between(sel_age[0], sel_age[1])
]

# ── Header ───────────────────────────────────────────────────────────────────
st.title("🛒 Zepto Customer Analytics Dashboard")
st.markdown(f"Showing **{len(fdf):,}** customers out of {len(df):,} total")
st.divider()

# ── KPI Cards ────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">{len(fdf):,}</div>
        <div class="metric-label">Total Customers</div></div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">{fdf['age'].mean():.1f}</div>
        <div class="metric-label">Avg Age</div></div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">{fdf['city'].nunique()}</div>
        <div class="metric-label">Cities Covered</div></div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">{fdf['state'].nunique()}</div>
        <div class="metric-label">States Covered</div></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 1: Gender Pie + Age Distribution ────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown('<p class="section-title">👥 Gender Distribution</p>', unsafe_allow_html=True)
    gender_counts = fdf["gender"].value_counts().reset_index()
    gender_counts.columns = ["Gender", "Count"]
    fig = px.pie(gender_counts, names="Gender", values="Count",
                 color_discrete_sequence=["#6C63FF", "#FF6584", "#43BCCD"],
                 hole=0.45)
    fig.update_layout(margin=dict(t=20, b=20), height=300, legend=dict(orientation="h"))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<p class="section-title">🎂 Age Group Distribution</p>', unsafe_allow_html=True)
    age_data = fdf["age_group"].value_counts().sort_index().reset_index()
    age_data.columns = ["Age Group", "Count"]
    fig2 = px.bar(age_data, x="Age Group", y="Count",
                  color="Count", color_continuous_scale="Purples",
                  text="Count")
    fig2.update_traces(textposition="outside")
    fig2.update_layout(margin=dict(t=20, b=20), height=300, coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

# ── Row 2: Top States Bar + Monthly Signups ─────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.markdown('<p class="section-title">🗺️ Top 10 States by Customers</p>', unsafe_allow_html=True)
    top_states = fdf["state"].value_counts().head(10).reset_index()
    top_states.columns = ["State", "Count"]
    fig3 = px.bar(top_states, x="Count", y="State", orientation="h",
                  color="Count", color_continuous_scale="Viridis",
                  text="Count")
    fig3.update_traces(textposition="outside")
    fig3.update_layout(margin=dict(t=20, b=20), height=350,
                       yaxis=dict(categoryorder="total ascending"),
                       coloraxis_showscale=False)
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.markdown('<p class="section-title">📅 Monthly Customer Signups</p>', unsafe_allow_html=True)
    monthly = fdf.groupby("month").size().reset_index(name="Signups")
    monthly = monthly.sort_values("month")
    fig4 = px.line(monthly, x="month", y="Signups",
                   markers=True, line_shape="spline",
                   color_discrete_sequence=["#6C63FF"])
    fig4.update_layout(margin=dict(t=20, b=20), height=350,
                       xaxis=dict(tickangle=45))
    st.plotly_chart(fig4, use_container_width=True)

# ── Row 3: City Top 10 + Gender × Age Group ─────────────────────────────────
col5, col6 = st.columns(2)

with col5:
    st.markdown('<p class="section-title">🏙️ Top 10 Cities by Customers</p>', unsafe_allow_html=True)
    top_cities = fdf["city"].value_counts().head(10).reset_index()
    top_cities.columns = ["City", "Count"]
    fig5 = px.bar(top_cities, x="City", y="Count",
                  color="Count", color_continuous_scale="Teal",
                  text="Count")
    fig5.update_traces(textposition="outside")
    fig5.update_layout(margin=dict(t=20, b=20), height=320, coloraxis_showscale=False)
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    st.markdown('<p class="section-title">📊 Gender vs Age Group Heatmap</p>', unsafe_allow_html=True)
    heatmap_data = fdf.groupby(["age_group", "gender"]).size().unstack(fill_value=0)
    fig6 = px.imshow(heatmap_data,
                     color_continuous_scale="Purples",
                     text_auto=True, aspect="auto")
    fig6.update_layout(margin=dict(t=20, b=20), height=320)
    st.plotly_chart(fig6, use_container_width=True)

# ── Row 4: Year-wise signups ──────────────────────────────────────────────────
st.markdown('<p class="section-title">📈 Year-wise Customer Growth by Gender</p>', unsafe_allow_html=True)
yearly_gender = fdf.groupby(["year", "gender"]).size().reset_index(name="Count")
fig7 = px.bar(yearly_gender, x="year", y="Count", color="gender", barmode="group",
              color_discrete_sequence=["#6C63FF", "#FF6584", "#43BCCD"],
              text="Count")
fig7.update_traces(textposition="outside")
fig7.update_layout(margin=dict(t=20, b=20), height=320)
st.plotly_chart(fig7, use_container_width=True)

# ── Raw Data Table ────────────────────────────────────────────────────────────
with st.expander("📄 View Raw Data"):
    st.dataframe(fdf.drop(columns=["year","month","age_group"]), use_container_width=True, height=300)
    csv = fdf.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Filtered Data as CSV", csv, "zepto_filtered.csv", "text/csv")

st.caption("Built with Streamlit & Plotly | Zepto Customer Dataset 2023–2024")
