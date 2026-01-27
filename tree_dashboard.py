import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker
import pydeck as pdk

st.markdown("""
    <style>
        .stApp {
            background-color: #F2F2F2 !important;
        }
        div.block-container {
            background-color: #F2F2F2 !important;
            padding-top: 2rem;
        }
        section[data-testid="stSidebar"] {
            background-color: #E6E6E6 !important;
        }
        div[data-testid="stToolbar"], div[data-testid="stDecoration"], div[data-testid="stStatusWidget"] {
            background-color: #F2F2F2 !important;
        }
    </style>
""", unsafe_allow_html=True)

plt.style.use("seaborn-v0_8-darkgrid")

COLOR_PRIMARY = "#2E8B57"
COLOR_ACCENT = "#FF7F50"
COLOR_DARK = "#1F4E79"
CHART_BG = "#F2F2F2"

sns.set_palette([COLOR_PRIMARY, COLOR_ACCENT])

@st.cache_data
def get_data():
    tree = pd.read_csv("data/Tree Data.csv")
    df = tree[(tree['tree_dbh'] < 40)]
    return df

df = get_data()

st.title("🌳 Tree Impact on NYC Sidewalks")

borough_options = ['All'] + list(df['borough'].unique())
selected_borough = st.sidebar.radio("Select Borough:", borough_options)

species_options = ['All'] + sorted(df['spc_common'].dropna().unique())
selected_species = st.sidebar.selectbox("Select Tree Species:", species_options)

df_select = df.copy() if selected_borough == 'All' else df[df['borough'] == selected_borough].copy()

if selected_species != 'All':
    df_select = df_select[df_select['spc_common'] == selected_species].copy()

df_select["sidewalk_damage"] = (df_select["sidewalk"] == "Damage").astype(int)

tree_count = df_select.shape[0]
average_dbh = round(df_select["tree_dbh"].mean(), 2) if tree_count > 0 else 0
damage_count = df_select[df_select["sidewalk_damage"] == 1].shape[0]
risk = round((damage_count / tree_count) * 100, 2) if tree_count > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("🌲 Tree Count", f"{tree_count:,}")
col2.metric("📏 Avg Diameter", f"{average_dbh} in")
col3.metric("⚠️ Damage Risk", f"{risk}%")

st.markdown(
    f"""
    <div style="padding:15px; background-color:#E8F5E9; border-radius:8px; margin-top:10px;">
        <h4 style="margin-bottom:5px;">Key Insight</h4>
        <p style="margin:0;">
            In <b>{selected_borough if selected_borough != 'All' else 'NYC'}</b>, the sidewalk damage risk is 
            <b>{risk}%</b> among <b>{tree_count:,}</b> trees, with an average diameter of 
            <b>{average_dbh} inches</b>.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

with st.container():

    species_stats = df_select.groupby("spc_common")["tree_dbh"].agg(["count", "mean"])
    top_species_stats = species_stats.sort_values("count", ascending=False).head(10)

    top_species_stats = top_species_stats.iloc[::-1]
    fig1, ax = plt.subplots(figsize=(10, 6), facecolor=CHART_BG)
    ax.set_facecolor(CHART_BG)

    colors = plt.cm.Greens(np.linspace(0.4, 0.9, len(top_species_stats)))
    bars = ax.bar(top_species_stats.index, top_species_stats["count"], color=colors)

    ax.set_xticks(range(len(top_species_stats.index)))
    ax.set_xticklabels(top_species_stats.index, rotation=35, ha="right", fontsize=11)
    ax.set_xlabel("Tree Species", fontsize=12)
    ax.set_ylabel("Tree Count", fontsize=12)
    ax.set_title("Top 10 Tree Species", fontsize=18, fontweight="bold")

    for i, bar in enumerate(bars):
        avg_dbh = round(top_species_stats["mean"].iloc[i], 1)
        ax.annotate(
            f"{avg_dbh}\"",
            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            fontsize=10,
            color=COLOR_DARK,
        )

    st.pyplot(fig1)

with st.container():
    custom_palette = {"0": "lightgreen", "1": "darkgreen"}
    fig2, ax = plt.subplots(figsize=(8, 5), facecolor=CHART_BG)
    ax.set_facecolor(CHART_BG)

    sns.boxplot(data=df_select, x="sidewalk_damage", y="tree_dbh", palette=custom_palette, ax=ax)

    ax.set_xlabel("Sidewalk Damage (0 = No, 1 = Yes)", fontsize=12)
    ax.set_ylabel("Tree Diameter (inches)", fontsize=12)
    ax.set_title("Tree Diameter Distribution by Sidewalk Damage", fontsize=14, fontweight="bold")

    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%d″"))
    ax.tick_params(axis="both", labelsize=10)

    fig2.tight_layout()
    st.pyplot(fig2)

with st.container():

    borough_risk = df_select.groupby("borough").agg(
        total_trees=("tree_dbh", "count"),
        damaged_trees=("sidewalk_damage", "sum"),
    )

    borough_risk["risk_pct"] = (borough_risk["damaged_trees"] / borough_risk["total_trees"]) * 100
    borough_risk_sorted = borough_risk.sort_values("risk_pct")

    fig3, ax = plt.subplots(figsize=(10, 6), facecolor=CHART_BG)
    ax.set_facecolor(CHART_BG)

    colors = plt.cm.Greens(np.linspace(0.4, 0.9, len(borough_risk_sorted)))

    bars = ax.bar(
        borough_risk_sorted.index,
        borough_risk_sorted["risk_pct"],
        color=colors,
        edgecolor="black",
    )

    ax.set_title("Sidewalk Damage Risk by Borough", fontsize=18, fontweight="bold")
    ax.set_ylabel("Damage Risk (%)", fontsize=12)
    ax.set_xlabel("Borough", fontsize=12)
    ax.set_xticks(range(len(borough_risk_sorted.index)))
    ax.set_xticklabels(borough_risk_sorted.index, rotation=35, ha="right")

    for i, bar in enumerate(bars):
        value = borough_risk_sorted["risk_pct"].iloc[i]
        ax.annotate(
            f"{value:.1f}%",
            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            fontsize=10,
            color=COLOR_DARK,
        )

    st.pyplot(fig3)

