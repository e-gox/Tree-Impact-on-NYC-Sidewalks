# import matplotlib.ticker as mticker
# import numpy as np
# import pandas as pd
# import streamlit as st
# import matplotlib.pyplot as plt
#
# @st.cache_data
# def get_data():
#     tree = pd.read_csv(r"C:\Users\ergig\OneDrive\Documents\Projects\Tree Data.csv")
#     df = tree[(tree['tree_dbh'] < 40) & (tree['status'] == 'Alive')]
#     return df
#
# df = get_data()
#
# st.title("New York City Tree Analysis")
#
# borough_options = ['All'] + list(df['borough'].unique())
# selected_borough = st.sidebar.radio("Select Borough:", borough_options)
#
# species_options = ['All'] + sorted(df['spc_common'].dropna().unique())
# selected_species = st.sidebar.selectbox("Select Tree Species:", species_options)
#
# # Filter by borough
# if selected_borough == 'All':
#     df_select = df.copy()
# else:
#     df_select = df[df['borough'] == selected_borough]
#
# # Further filter by species
# if selected_species != 'All':
#     df_select = df_select[df_select['spc_common'] == selected_species]
#
# average_dbh = round(df_select['tree_dbh'].mean(),2)
# tree_count = df_select.shape[0]
# damage_count = df_select[df_select['sidewalk'] == 'Damage'].shape[0]
# risk = round((damage_count / df_select.shape[0]) * 100, 2)
# first_column,second_column,third_column = st.columns(3)
#
# with first_column:
#     st.metric(label="Tree Count:", value=f"{tree_count:,}")
# with second_column:
#     st.metric(label="Average Diameter:", value=f"{average_dbh} Inches")
# with third_column:
#     st.metric("Risk:", value=f"{risk} % ")
# st.divider()
#
# species_stats = df_select.groupby('spc_common')['tree_dbh'].agg(['count', 'mean'])
# top_species_stats = species_stats.sort_values('count', ascending=False).head(10)
#
# fig1, ax = plt.subplots(figsize=(10, 6))
# bars = ax.bar(top_species_stats.index, top_species_stats['count'], color='forestgreen')
#
# ax.set_xticks(range(len(top_species_stats.index)))
# ax.set_xticklabels(top_species_stats.index, rotation=45, ha='right')
# ax.set_xlabel("Species", fontsize=12)
# ax.set_ylabel("Tree Count", fontsize=12)
# ax.set_title("Top 10 Tree Species with Average Diameter", fontsize=14, fontweight='bold')
#
# # Add average diameter labels
# for i, bar in enumerate(bars):
#     avg_dbh = round(top_species_stats['mean'].iloc[i], 1)
#     ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5, f"{avg_dbh}\"",
#             ha='center', va='bottom', fontsize=10, fontweight='bold', color='darkred')
#
# # Add gridlines and format y-axis
# ax.yaxis.grid(True, linestyle='--', alpha=0.5)
# ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))
#
# fig1.tight_layout()
# st.pyplot(fig1)
#
# # Create damage flag
# df_select['sidewalk_damage'] = (df_select['sidewalk'] == 'Damage').astype(int)
#
# # Create boxplot
# fig2, ax = plt.subplots(figsize=(8, 5))
# df_select.boxplot(column='tree_dbh', by='sidewalk_damage', ax=ax, grid=False, boxprops=dict(color='darkblue'))
#
# # Remove default title
# plt.suptitle("")
#
# # Improve axis labels and title
# ax.set_xlabel('Sidewalk Damage (0 = No, 1 = Yes)', fontsize=12)
# ax.set_ylabel('Tree Diameter (inches)', fontsize=12)
# ax.set_title('Tree Diameter Distribution by Sidewalk Damage', fontsize=14, fontweight='bold')
#
# # Add gridlines for readability
# ax.yaxis.grid(True, linestyle='--', alpha=0.5)
#
# # Format y-axis ticks with inches
# ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%d″'))
#
# # Optional: adjust tick label font size
# ax.tick_params(axis='both', labelsize=10)
#
# # Tight layout
# fig2.tight_layout()
#
# # Display in Streamlit
# st.pyplot(fig2)
#
# # Step 1: Group and calculate risk
# borough_risk = df_select.groupby('borough').agg(
#     total_trees=('tree_dbh', 'count'),
#     damaged_trees=('sidewalk_damage', 'sum')
# )
# borough_risk['risk_pct'] = (borough_risk['damaged_trees'] / borough_risk['total_trees']) * 100
#
# # Step 2: Sort by ascending risk
# borough_risk_sorted = borough_risk.sort_values('risk_pct')
#
# # Step 3: Plot
# fig3, ax = plt.subplots(figsize=(10, 6))
# bars = ax.bar(borough_risk_sorted.index, borough_risk_sorted['risk_pct'], color='coral', edgecolor='black')
#
# # Title and labels
# ax.set_title("Sidewalk Damage Risk by Borough (Ascending)", fontsize=14, fontweight='bold')
# ax.set_xlabel("Borough", fontsize=12)
# ax.set_ylabel("Damage Risk (%)", fontsize=12)
#
# # Rotate x-axis labels
# ax.set_xticks(range(len(borough_risk_sorted.index)))
# ax.set_xticklabels(borough_risk_sorted.index, rotation=45, ha='right')
#
# # Add gridlines
# ax.yaxis.grid(True, linestyle='--', alpha=0.5)
#
# # Format y-axis ticks
# ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f%%'))
#
# # Add percentage labels above bars
# for i, bar in enumerate(bars):
#     value = borough_risk_sorted['risk_pct'].iloc[i]
#     ax.text(
#         bar.get_x() + bar.get_width() / 2,
#         bar.get_height() - 2,  # slightly below the top
#         f"{value:.1f}%",
#         ha='center',
#         va='top',
#         fontsize=10,
#         fontweight='bold',
#         color='darkred'  # white text for contrast
#     )
#
# # Tight layout
# fig3.tight_layout()
#
# # Display in Streamlit
# st.pyplot(fig3)
#
#

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk

# ---------------------------------------------------------
# GLOBAL STYLING — FIXED BACKGROUND FOR STREAMLIT 1.30+
# ---------------------------------------------------------

st.markdown("""
    <style>
        /* Entire app background */
        .stApp {
            background-color: #F2F2F2 !important;
        }

        /* Main content area */
        div.block-container {
            background-color: #F2F2F2 !important;
            padding-top: 2rem;
        }

        /* Sidebar background */
        section[data-testid="stSidebar"] {
            background-color: #E6E6E6 !important;
        }

        /* Remove white bars at top */
        div[data-testid="stToolbar"], div[data-testid="stDecoration"], div[data-testid="stStatusWidget"] {
            background-color: #F2F2F2 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Softer, modern chart theme
plt.style.use("seaborn-v0_8-darkgrid")

# Unified color palette
COLOR_PRIMARY = "#2E8B57"   # Forest green
COLOR_ACCENT = "#FF7F50"    # Coral
COLOR_DARK = "#1F4E79"      # Deep blue
CHART_BG = "#F2F2F2"        # Matches app background

sns.set_palette([COLOR_PRIMARY, COLOR_ACCENT])

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
@st.cache_data
def get_data():
    tree = pd.read_csv(r"C:\\Users\\ergig\\OneDrive\\Documents\\Projects\\Tree Data.csv")
    df = tree[(tree['tree_dbh'] < 40) & (tree['status'] == 'Alive')]
    return df

df = get_data()

# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------
st.title("🌳 New York City Tree Health Dashboard")

# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------
borough_options = ['All'] + list(df['borough'].unique())
selected_borough = st.sidebar.radio("Select Borough:", borough_options)

species_options = ['All'] + sorted(df['spc_common'].dropna().unique())
selected_species = st.sidebar.selectbox("Select Tree Species:", species_options)

# ---------------------------------------------------------
# FILTER DATA
# ---------------------------------------------------------
df_select = df.copy() if selected_borough == 'All' else df[df['borough'] == selected_borough]
if selected_species != 'All':
    df_select = df_select[df_select['spc_common'] == selected_species]

df_select['sidewalk_damage'] = (df_select['sidewalk'] == 'Damage').astype(int)

# ---------------------------------------------------------
# METRICS
# ---------------------------------------------------------
average_dbh = round(df_select['tree_dbh'].mean(), 2)
tree_count = df_select.shape[0]
damage_count = df_select[df_select['sidewalk_damage'] == 1].shape[0]
risk = round((damage_count / tree_count) * 100, 2)

col1, col2, col3 = st.columns(3)
col1.metric("🌲 Tree Count", f"{tree_count:,}")
col2.metric("📏 Avg Diameter", f"{average_dbh} in")
col3.metric("⚠️ Damage Risk", f"{risk}%")

# ---------------------------------------------------------
# INSIGHT CARD
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# TOP SPECIES BAR CHART (GRADIENT)
# ---------------------------------------------------------
with st.container():
    st.subheader("🌱 Top 10 Tree Species")

    species_stats = df_select.groupby('spc_common')['tree_dbh'].agg(['count', 'mean'])
    top_species_stats = species_stats.sort_values('count', ascending=False).head(10)

    fig1, ax = plt.subplots(figsize=(10, 6), facecolor=CHART_BG)
    ax.set_facecolor(CHART_BG)

    colors = plt.cm.Greens(np.linspace(0.4, 0.9, len(top_species_stats)))
    bars = ax.bar(top_species_stats.index, top_species_stats['count'], color=colors)

    ax.set_xticks(range(len(top_species_stats.index)))
    ax.set_xticklabels(top_species_stats.index, rotation=35, ha='right', fontsize=11)
    ax.set_ylabel("Tree Count", fontsize=12)
    ax.set_title("Top 10 Tree Species", fontsize=18, fontweight='bold')

    for i, bar in enumerate(bars):
        avg_dbh = round(top_species_stats['mean'].iloc[i], 1)
        ax.annotate(f"{avg_dbh}\"",
                    xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 8),
                    textcoords="offset points",
                    ha='center', fontsize=10, color=COLOR_DARK)

    st.pyplot(fig1)

# ---------------------------------------------------------
# VIOLIN PLOT (MODERN DISTRIBUTION)
# ---------------------------------------------------------
with st.container():
    st.subheader("📦 Tree Diameter Distribution by Sidewalk Damage")

    fig2, ax = plt.subplots(figsize=(8, 5), facecolor=CHART_BG)
    ax.set_facecolor(CHART_BG)

    sns.violinplot(
        data=df_select,
        x='sidewalk_damage',
        y='tree_dbh',
        palette=[COLOR_PRIMARY, COLOR_ACCENT],
        ax=ax
    )

    ax.set_xticklabels(['No Damage', 'Damage'])
    ax.set_xlabel("")
    ax.set_ylabel("Tree Diameter (inches)", fontsize=12)
    ax.set_title("Diameter Distribution by Sidewalk Damage", fontsize=18, fontweight='bold')

    st.pyplot(fig2)

# ---------------------------------------------------------
# BOROUGH RISK BAR CHART
# ---------------------------------------------------------
with st.container():
    st.subheader("🏙️ Sidewalk Damage Risk by Borough")

    borough_risk = df_select.groupby('borough').agg(
        total_trees=('tree_dbh', 'count'),
        damaged_trees=('sidewalk_damage', 'sum')
    )
    borough_risk['risk_pct'] = (borough_risk['damaged_trees'] / borough_risk['total_trees']) * 100
    borough_risk_sorted = borough_risk.sort_values('risk_pct')

    fig3, ax = plt.subplots(figsize=(10, 6), facecolor=CHART_BG)
    ax.set_facecolor(CHART_BG)

    colors = ['#FF7F50' if v > borough_risk_sorted['risk_pct'].mean() else '#87CEFA'
              for v in borough_risk_sorted['risk_pct']]

    bars = ax.bar(borough_risk_sorted.index, borough_risk_sorted['risk_pct'],
                  color=colors, edgecolor='black')

    ax.set_title("Sidewalk Damage Risk by Borough", fontsize=18, fontweight='bold')
    ax.set_ylabel("Damage Risk (%)", fontsize=12)
    ax.set_xticklabels(borough_risk_sorted.index, rotation=35, ha='right')

    for i, bar in enumerate(bars):
        value = borough_risk_sorted['risk_pct'].iloc[i]
        ax.annotate(f"{value:.1f}%",
                    xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 8),
                    textcoords="offset points",
                    ha='center', fontsize=10, color=COLOR_DARK)

    st.pyplot(fig3)

# ---------------------------------------------------------
# OPTIONAL: NYC MAP
# ---------------------------------------------------------
with st.container():
    st.subheader("🗺️ Tree Density Map (Optional)")

    if 'latitude' in df_select.columns and 'longitude' in df_select.columns:
        layer = pdk.Layer(
            "HexagonLayer",
            df_select,
            get_position=['longitude', 'latitude'],
            radius=80,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        )

        view_state = pdk.ViewState(
            latitude=40.7,
            longitude=-73.9,
            zoom=9,
            pitch=40,
        )

        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
    else:
        st.info("Latitude/Longitude not available in dataset.")