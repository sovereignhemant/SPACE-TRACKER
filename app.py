import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as gg
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="India Space Policy & Regulatory Tracker",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

@st.cache_data
def load_data():
    events_df = pd.read_csv(DATA_DIR / "policy_events.csv", dtype=str).fillna("")
    regimes_df = pd.read_csv(DATA_DIR / "regimes.csv", dtype=str).fillna("")
    
    # Process dates
    events_df['parsed_date'] = pd.to_datetime(events_df['date'], errors='coerce')
    events_df = events_df.sort_values('parsed_date', ascending=True)
    return events_df, regimes_df

try:
    events_df, regimes_df = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# Custom CSS for polished aesthetics
st.markdown("""
<style>
    /* Global Styles */
    .main {
        background-color: #0b0f19;
        color: #e2e8f0;
        font-family: 'Inter', system-ui, sans-serif;
    }
    
    /* Card Container */
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.8));
        border: 1px solid rgba(51, 65, 85, 0.6);
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
    }
    
    .metric-title {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94a3b8;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #38bdf8;
    }
    
    /* Policy Event Badge */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        font-size: 0.75rem;
        font-weight: 600;
        border-radius: 9999px;
        margin-right: 0.5rem;
    }
    .badge-institutional { background-color: #1e3a8a; color: #93c5fd; }
    .badge-regulatory { background-color: #581c87; color: #e9d5ff; }
    .badge-authorization { background-color: #065f46; color: #6ee7b7; }
    .badge-funding { background-color: #854d0e; color: #fef08a; }
    .badge-launch { background-color: #991b1b; color: #fca5a5; }

    /* Custom Table Styling */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1e293b;
        border-radius: 8px 8px 0 0;
        color: #cbd5e1;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background-color: #0284c7 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_allowed_html=True if hasattr(st, "unsafe_allow_allowed_html") else True)

# Header Section
st.title("🚀 India Space Policy & Regulatory Regime Tracker")
st.markdown("""
An open, versioned dataset and comparative analytical dashboard tracking the evolution of India's commercial space policy regime 
(IN-SPACe, ISP 2023, FDI amendments) benchmarked against key international space faring nations (**United States**, **Luxembourg**, **UAE**).
""")

# Sidebar Controls
st.sidebar.image("https://img.icons8.com/isometric/100/satellite.png", width=70)
st.sidebar.title("Filter & Navigation")

view_mode = st.sidebar.radio(
    "Select View Mode",
    ["1. Interactive Timeline", "2. Regime Comparator", "3. IN-SPACe Authorizations", "4. Data & Methodology"]
)

# Filters
st.sidebar.markdown("---")
st.sidebar.subheader("Dataset Filters")
selected_countries = st.sidebar.multiselect(
    "Filter Countries",
    options=list(events_df['country'].unique()),
    default=list(events_df['country'].unique())
)

selected_categories = st.sidebar.multiselect(
    "Filter Categories",
    options=list(events_df['category'].unique()),
    default=list(events_df['category'].unique())
)

# Filtered DataFrame
filtered_events = events_df[
    (events_df['country'].isin(selected_countries)) &
    (events_df['category'].isin(selected_categories))
]

# Sidebar Quick Download
st.sidebar.markdown("---")
st.sidebar.subheader("Export Data")
st.sidebar.download_button(
    label="📥 Download policy_events.csv",
    data=events_df.to_csv(index=False),
    file_name="policy_events.csv",
    mime="text/csv"
)
st.sidebar.download_button(
    label="📥 Download regimes.csv",
    data=regimes_df.to_csv(index=False),
    file_name="regimes.csv",
    mime="text/csv"
)

# VIEW 1: TIMELINE VIEW
if view_mode == "1. Interactive Timeline":
    st.header("1. Comparative Space Policy Timeline")
    
    # Top KPI metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class="metric-card"><div class="metric-title">Total Tracked Events</div>
        <div class="metric-value">{}</div></div>""".format(len(filtered_events)), unsafe_allow_html=True)
    with col2:
        india_events = len(filtered_events[filtered_events['country'] == 'India'])
        st.markdown("""<div class="metric-card"><div class="metric-title">India Milestones</div>
        <div class="metric-value">{}</div></div>""".format(india_events), unsafe_allow_html=True)
    with col3:
        auth_events = len(filtered_events[filtered_events['category'] == 'authorization'])
        st.markdown("""<div class="metric-card"><div class="metric-title">Authorizations</div>
        <div class="metric-value">{}</div></div>""".format(auth_events), unsafe_allow_html=True)
    with col4:
        comparator_events = len(filtered_events[filtered_events['country'] != 'India'])
        st.markdown("""<div class="metric-card"><div class="metric-title">Comparator Events</div>
        <div class="metric-value">{}</div></div>""".format(comparator_events), unsafe_allow_html=True)

    # Plotly Timeline Chart
    if not filtered_events.empty:
        fig = px.scatter(
            filtered_events,
            x="parsed_date",
            y="country",
            color="category",
            symbol="status",
            hover_name="title",
            hover_data={
                "date": True,
                "category": True,
                "actors": True,
                "parsed_date": False,
                "country": False
            },
            size_max=15,
            title="Space Policy Milestones Across Regimes (2014 - Present)",
            labels={"parsed_date": "Date", "country": "Regime", "category": "Category"},
            color_discrete_map={
                "institutional": "#3b82f6",
                "regulatory": "#a855f7",
                "authorization": "#10b981",
                "funding": "#eab308",
                "launch_milestone": "#ef4444"
            }
        )
        fig.update_traces(marker=dict(size=14, line=dict(width=1, color='White')))
        fig.update_layout(
            template="plotly_dark",
            height=450,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0.6)",
            xaxis=dict(showgrid=True, gridcolor="rgba(51,65,85,0.4)"),
            yaxis=dict(showgrid=True, gridcolor="rgba(51,65,85,0.4)")
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Detailed Policy Event Log")
    
    # Search box for events
    search_term = st.text_input("🔍 Search events by keyword, actor, or title:", "")
    display_df = filtered_events.copy()
    if search_term:
        display_df = display_df[
            display_df['title'].str.contains(search_term, case=False) |
            display_df['description'].str.contains(search_term, case=False) |
            display_df['actors'].str.contains(search_term, case=False)
        ]
    
    for idx, row in display_df.iterrows():
        with st.expander(f"📌 [{row['country']}] {row['date']} — {row['title']}"):
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.write(f"**Description:** {row['description']}")
                st.write(f"**Actors Involved:** {row['actors']}")
                if row['supersedes_event_id']:
                    st.info(f"🔄 **Supersedes Prior Draft:** `{row['supersedes_event_id']}`")
            with col_b:
                st.write(f"**Category:** `{row['category']}`")
                st.write(f"**Status:** `{row['status']}`")
                st.write(f"**Source Type:** `{row['source_type']}`")
                st.markdown(f"[🔗 Primary Source Link]({row['source_url']})")

# VIEW 2: REGIME COMPARATOR
elif view_mode == "2. Regime Comparator":
    st.header("2. Side-by-Side Regulatory Regime Benchmarking")
    st.markdown("Direct comparison of regulatory models, foreign direct investment (FDI) caps, liability structures, and space resource rights.")
    
    selected_benchmarks = st.multiselect(
        "Select Regimes to Benchmark",
        options=list(regimes_df['country'].unique()),
        default=["India", "USA", "Luxembourg", "UAE"]
    )
    
    comp_df = regimes_df[regimes_df['country'].isin(selected_benchmarks)].set_index("country")
    
    if not comp_df.empty:
        # Comparison Table Matrix
        st.subheader("1. FDI Ownership Caps Comparison")
        fdi_cols = ["regulator", "fdi_cap_satellites", "fdi_cap_launch_vehicles", "fdi_cap_ground_segment"]
        st.dataframe(comp_df[fdi_cols], use_container_width=True)

        st.subheader("2. Regulatory Architecture & Liability Framework")
        legal_cols = ["licensing_model", "liability_framework", "resource_rights"]
        st.dataframe(comp_df[legal_cols], use_container_width=True)
        
        st.subheader("3. Feature Comparison Matrix Cards")
        cols = st.columns(len(selected_benchmarks))
        for idx, country in enumerate(selected_benchmarks):
            with cols[idx]:
                r = comp_df.loc[country]
                st.markdown(f"### 🛡️ {country}")
                st.markdown(f"**Regulator:** {r['regulator']}")
                st.markdown(f"**Licensing Model:** {r['licensing_model']}")
                st.markdown(f"**Satellites FDI:** `{r['fdi_cap_satellites']}`")
                st.markdown(f"**Launch Vehicles FDI:** `{r['fdi_cap_launch_vehicles']}`")
                st.markdown(f"**Ground Segment FDI:** `{r['fdi_cap_ground_segment']}`")
                st.markdown(f"**Liability:** {r['liability_framework']}")
                st.markdown(f"**Space Resource Rights:** {r['resource_rights']}")

# VIEW 3: IN-SPACE AUTHORIZATIONS TRACKER
elif view_mode == "3. IN-SPACe Authorizations":
    st.header("3. IN-SPACe Private Sector Authorizations Tracker")
    st.markdown("Running log and velocity metrics of IN-SPACe authorizations granted to non-governmental entities (NGEs) in India since 2020.")
    
    inspace_auths = events_df[
        (events_df['country'] == 'India') & 
        (events_df['category'].isin(['authorization', 'launch_milestone']))
    ].copy()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div class="metric-card"><div class="metric-title">Tracked Authorizations</div>
        <div class="metric-value">{len(inspace_auths[inspace_auths['category']=='authorization'])}</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card"><div class="metric-title">Private Launches Authorized</div>
        <div class="metric-value">{len(inspace_auths[inspace_auths['category']=='launch_milestone'])}</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="metric-card"><div class="metric-title">Key Players Authorized</div>
        <div class="metric-value">Skyroot, Agnikul, Dhruva, Digantara, Pixxel</div></div>""", unsafe_allow_html=True)
        
    # Velocity Chart
    inspace_auths['year_month'] = inspace_auths['parsed_date'].dt.to_period('M').astype(str)
    inspace_auths['cumulative_count'] = range(1, len(inspace_auths) + 1)
    
    fig_auth = px.line(
        inspace_auths,
        x="parsed_date",
        y="cumulative_count",
        markers=True,
        text="title",
        title="Cumulative IN-SPACe Authorization & Launch Velocity",
        labels={"parsed_date": "Date", "cumulative_count": "Cumulative Authorizations"}
    )
    fig_auth.update_traces(textposition="top left", marker=dict(size=10, color='#10b981'))
    fig_auth.update_layout(
        template="plotly_dark",
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.6)"
    )
    st.plotly_chart(fig_auth, use_container_width=True)
    
    st.subheader("Authorized Entity Directory")
    st.dataframe(
        inspace_auths[['date', 'category', 'title', 'actors', 'source_type', 'source_url']],
        column_config={
            "source_url": st.column_config.LinkColumn("Primary Link")
        },
        use_container_width=True
    )

# VIEW 4: DATA & METHODOLOGY
elif view_mode == "4. Data & Methodology":
    st.header("4. Data Schema & Methodology")
    st.markdown("""
    This project adheres to rigorous open policy research standards. All data points are sourced from primary gazette notifications, 
    parliamentary submissions, and official regulatory portal announcements.
    """)
    
    tab1, tab2, tab3 = st.tabs(["Raw Dataset Preview", "Methodology & Scope", "Citation Guide"])
    
    with tab1:
        st.subheader("policy_events.csv")
        st.dataframe(events_df, use_container_width=True)
        st.subheader("regimes.csv")
        st.dataframe(regimes_df, use_container_width=True)
        
    with tab2:
        st.markdown("""
        ### Scope & Sourcing Rules
        * **Primary Focus**: India commercial space regulatory regime from 2020 through 2026.
        * **Comparators**: USA (CSLA framework), Luxembourg (2017 Space Resources Law), UAE (2019 Federal Space Law).
        * **Out of Scope (v1)**: Defense/military space applications, state-level guidelines, full legislative text republishing.
        * **Integrity**: Zero un-sourced rows. Descriptions are original analytical syntheses.
        """)
        
    with tab3:
        st.markdown("""
        ### How to Cite This Dataset
        Policy researchers, think tanks, and journalists can cite this repository directly:

        > **Brydgework Policy Research (2026).** *India Space Policy & Regulatory Regime Tracker*. Version 1.0. Available at GitHub: [india-space-policy-tracker](https://github.com/brydgework/india-space-policy-tracker).

        ```bibtex
        @dataset{india_space_policy_tracker_2026,
          author       = {Brydgework Policy Research},
          title        = {India Space Policy and Regulatory Regime Tracker},
          year         = 2026,
          publisher    = {GitHub},
          url          = {https://github.com/brydgework/india-space-policy-tracker}
        }
        ```
        """)

# Footer
st.markdown("---")
st.markdown("Designed for policy analysts, researchers, and recruiters. Companion project to [india-space-budget](https://github.com/brydgework/india-space-budget).")
