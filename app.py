# ==============================================================================
# COURSE CODE    : UECS3183
# COURSE TITLE   : Data Visualisation Techniques
# ASSIGNMENT     : Assignment 2 (Interactive Dashboard)
# STUDENT NAME   : Tee Hue Leng
# STUDENT ID     : 2206851
# PROGRAMME      : Bachelor of Software Engineering (SE)
# ==============================================================================

# ==============================================================================
# DASHBOARD GENERATION & EXECUTION INSTRUCTIONS:
# ==============================================================================
# 1. PREREQUISITES & DEPENDENCIES:
#    Ensure you have Python installed along with the required visualization 
#    and UI libraries. Run the following command in your terminal if needed:
#    pip install streamlit pandas numpy plotly streamlit-option-menu
#
# 2. DATASET PLACEMENT:
#    Place the dataset file named "Rotten Tomatoes Movies.csv" in the exact 
#    same directory/folder where this Python script is saved.
#
# 3. RUNNING THE APPLICATION:
#    Open your terminal or command prompt, navigate to your script directory,
#    and execute the Streamlit application using the command:
#    streamlit run app.py
#
# 4. INTERACTIVE FEATURES:
#    - Use the visible 'Composing Desk' expander panel at the top of the main screen 
#      to filter records by year span, genres, critical consensus tiers, MPAA content 
#      ratings and search queries.
#    - Use the top horizontal menu bar to navigate across different visual analytics 
#      sections (Trends, Audit Matrix, Demographics, Studio Radar, etc.).
# ==============================================================================

import os
import time
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_option_menu import option_menu

# ------------------------------------------------------------------------------
# 1. STREAMLIT PAGE CONFIGURATION & DYNAMIC LUXURY EDITORIAL STYLING
# ------------------------------------------------------------------------------
# Sets up the general browser tab configuration, page title, icon, and expands 
# the layout to wide-screen mode to accommodate multi-column dashboards.
st.set_page_config(
    page_title="The Cinematic Gazette | Rotten Tomatoes",
    page_icon="🎟️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Injects custom Cascading Style Sheets (CSS) to implement a vintage newspaper 
# visual theme (Parchment background, custom typography using Cinzel and Plus Jakarta 
# Sans fonts, card shadows, and smooth page load transitions).
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        --bg-parchment: #f4f1ea;
        --surface-card: #ffffff;
        --surface-subtle: #eae5d9;
        --border-ink: #1c1b18;
        --ink-main: #141311;
        --ink-muted: #5c5952;
        --crimson-stamp: #b82311;
        --gold-medal: #c28e21;
        --sage-green: #3b5343;
    }

    html, body, .stApp {
        background-color: var(--bg-parchment) !important;
        color: var(--ink-main) !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    header[data-testid="stHeader"], div[data-testid="stToolbar"] {
        display: none !important;
    }

    .main .block-container {
        max-width: 1600px !important;
        width: 100% !important;
        padding: 2.5rem 3rem 6rem !important;
        animation: fadeInPage 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    @keyframes fadeInPage {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .gazette-masthead {
        border-top: 4px solid var(--border-ink);
        border-bottom: 4px double var(--border-ink);
        padding: 1.8rem 0 1.2rem 0;
        margin-bottom: 2rem;
        text-align: center;
        background: var(--surface-card);
        box-shadow: 0 10px 35px rgba(0,0,0,0.06);
        width: 100%;
        position: relative;
        overflow: hidden;
        animation: slideDownMasthead 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    .gazette-masthead::after {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(184,35,17,0.05), transparent);
        animation: shimmerWave 6s infinite;
    }

    @keyframes shimmerWave {
        0% { left: -100%; }
        20% { left: 100%; }
        100% { left: 100%; }
    }

    @keyframes slideDownMasthead {
        from { opacity: 0; transform: translateY(-25px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .masthead-title {
        font-family: 'Cinzel', serif;
        font-size: clamp(3rem, 5.5vw, 4.8rem);
        font-weight: 900;
        letter-spacing: -0.5px;
        line-height: 1;
        text-transform: uppercase;
        color: var(--ink-main);
        margin: 0;
    }

    .masthead-subbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 1.5px solid var(--border-ink);
        border-bottom: 1.5px solid var(--border-ink);
        padding: 8px 16px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 14px;
        background: var(--surface-subtle);
    }

    .gazette-story-banner {
        background: var(--surface-card);
        border: 2px solid var(--border-ink);
        border-left: 6px solid var(--crimson-stamp);
        border-radius: 6px;
        padding: 1.1rem 1.4rem;
        margin-bottom: 1.8rem;
        box-shadow: 4px 4px 0px 0px var(--border-ink);
        animation: fadeInPage 0.8s ease backwards;
    }

    .story-banner-tag {
        font-size: 0.72rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: var(--crimson-stamp);
        margin-bottom: 0.4rem;
    }

    .story-banner-text {
        font-size: 0.88rem;
        line-height: 1.55;
        color: var(--ink-main);
    }

    .print-metric-card {
        background: var(--surface-card);
        border: 2px solid var(--border-ink);
        border-radius: 6px;
        padding: 1.3rem;
        box-shadow: 4px 4px 0px 0px var(--border-ink);
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        height: 100%;
        position: relative;
        animation: popInCard 0.5s cubic-bezier(0.16, 1, 0.3, 1) backwards;
    }

    .print-metric-card:nth-child(1) { animation-delay: 0.1s; }
    .print-metric-card:nth-child(2) { animation-delay: 0.15s; }
    .print-metric-card:nth-child(3) { animation-delay: 0.2s; }
    .print-metric-card:nth-child(4) { animation-delay: 0.25s; }
    .print-metric-card:nth-child(5) { animation-delay: 0.3s; }

    @keyframes popInCard {
        from { opacity: 0; transform: scale(0.9) translateY(15px); }
        to { opacity: 1; transform: scale(1) translateY(0); }
    }

    .print-metric-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 8px 12px 25px rgba(28,27,24,0.12), 4px 4px 0px 0px var(--border-ink);
        border-color: var(--crimson-stamp);
    }

    .print-metric-label {
        font-size: 0.7rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: var(--ink-muted);
        margin-bottom: 0.4rem;
    }

    .print-metric-val {
        font-family: 'Cinzel', serif;
        font-size: 2.4rem;
        line-height: 1;
        font-weight: 700;
        color: var(--ink-main);
        transition: color 0.3s ease;
    }

    .print-metric-card:hover .print-metric-val {
        color: var(--crimson-stamp);
    }

    .film-card {
        background: var(--surface-card);
        border: 2px solid var(--border-ink);
        border-radius: 6px;
        box-shadow: 5px 5px 0px 0px var(--border-ink);
        overflow: hidden;
        transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
        animation: fadeInCard 0.6s ease backwards;
    }

    @keyframes fadeInCard {
        from { opacity: 0; transform: translateY(20px); scale: 0.96; }
        to { opacity: 1; transform: translateY(0); scale: 1; }
    }

    .film-card:hover {
        transform: translateY(-6px) scale(1.01);
        box-shadow: 10px 14px 30px rgba(28,27,24,0.15), 6px 6px 0px 0px var(--crimson-stamp);
        border-color: var(--crimson-stamp);
    }

    .film-poster {
        width: 100%;
        height: 290px;
        object-fit: cover;
        border-bottom: 2px solid var(--border-ink);
        background: #111;
        transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .film-card:hover .film-poster {
        transform: scale(1.06) rotate(0.5deg);
    }

    .film-body {
        padding: 1rem;
    }

    .film-title {
        font-family: 'Cinzel', serif;
        font-size: 1.15rem;
        font-weight: 700;
        line-height: 1.2;
        color: var(--ink-main);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        transition: color 0.2s ease;
    }

    .film-card:hover .film-title {
        color: var(--crimson-stamp);
    }

    .stButton > button {
        background: var(--border-ink) !important;
        color: #ffffff !important;
        border: 2px solid var(--border-ink) !important;
        border-radius: 6px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        box-shadow: 3px 3px 0px 0px #b82311 !important;
        transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 6px 8px 20px rgba(184,35,17,0.3), 4px 4px 0px 0px #b82311 !important;
        background: #b82311 !important;
    }

    .stButton > button:active {
        transform: translateY(1px) scale(0.98);
        box-shadow: 1px 1px 0px 0px #b82311 !important;
    }
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# 2. DATA LOADING & CLEANING PIPELINE
# ------------------------------------------------------------------------------
# Uses st.cache_data to load and preprocess the raw Rotten Tomatoes dataset efficiently, 
# preventing redundant file reads on user interaction.
@st.cache_data(show_spinner="🎬 Assembling cinematic archives...")
def load_and_clean_data():
    # Define potential relative pathways to check for the dataset file
    csv_paths = [
        "Rotten Tomatoes Movies.csv",
        os.path.join(os.path.dirname(__file__), "Rotten Tomatoes Movies.csv")
    ]

    df = None
    for path in csv_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            break

    # Stop execution and notify the user if the CSV data file cannot be located
    if df is None:
        st.error("⚠️ Dataset file 'Rotten Tomatoes Movies.csv' was not found in the application directory.")
        st.stop()

    # Clean text columns by handling missing entries (NaN values) and stripping whitespace
    df['movie_title'] = df['movie_title'].fillna('Unknown Title').astype(str).str.strip()
    df['directors'] = df['directors'].fillna('Unknown').astype(str).str.strip()
    df['studio_name'] = df['studio_name'].fillna('Independent / Other').astype(str).str.strip()
    df['genre'] = df['genre'].fillna('Drama').astype(str)
    df['cast'] = df['cast'].fillna('Unknown Cast').astype(str)
    df['critics_consensus'] = df['critics_consensus'].fillna('No consensus recorded.')
    df['movie_info'] = df['movie_info'].fillna('No synopsis available.')
    
    # Process multi-genre strings into iterable lists and extract the primary genre for categorization
    df['genre_list'] = df['genre'].apply(lambda x: [g.strip() for g in str(x).split(',') if g.strip()])
    df['primary_genre'] = df['genre_list'].apply(lambda x: x[0] if len(x) > 0 else 'Drama')

    # Convert rating columns to valid numeric types and handle null values safely
    df['tomatometer_rating'] = pd.to_numeric(df['tomatometer_rating'], errors='coerce').fillna(0).astype(int)
    df['audience_rating'] = pd.to_numeric(df['audience_rating'], errors='coerce')
    df['audience_rating_clean'] = df['audience_rating'].fillna(df['tomatometer_rating']).astype(int)
    
    # Parse release date strings into datetime objects to extract release years and decades
    dt_series = pd.to_datetime(df['in_theaters_date'], format='%d/%m/%Y', errors='coerce')
    df['release_year'] = dt_series.dt.year.fillna(2000).astype(int)
    df['decade'] = (df['release_year'] // 10 * 10).astype(str) + 's'

    df['tomatometer_status'] = df['tomatometer_status'].fillna('Rotten').str.strip()
    df['rating_clean'] = df['rating'].fillna('Not Rated').astype(str).str.strip().str.rstrip(')')
    
    # Set up poster image URL mappings with fallback Unsplash placeholders for missing entries
    if 'poster_path' not in df.columns and 'Poster Path' in df.columns:
        df['poster_path'] = df['Poster Path']
    elif 'poster_path' not in df.columns:
        df['poster_path'] = None
    df['poster_url'] = df['poster_path'].fillna('https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=300&auto=format&fit=crop&q=60')

    # Calculate metrics measuring discrepancies between critic and audience scores
    df['score_difference'] = df['audience_rating_clean'] - df['tomatometer_rating']
    df['abs_score_difference'] = df['score_difference'].abs()
    df['runtime_clean'] = pd.to_numeric(df['runtime_in_minutes'], errors='coerce').fillna(100)

    # Assign qualitative editorial consensus tags based on predefined rating thresholds
    def assign_consensus(row):
        c, a = row['tomatometer_rating'], row['audience_rating_clean']
        if c >= 75 and a >= 75: return 'Universal Acclaim'
        elif c >= 70 and a <= 55: return 'Critic Darling'
        elif a >= 70 and c <= 55: return 'Cult Classic'
        elif c < 50 and a < 50: return 'Universal Flop'
        else: return 'Moderate Consensus'

    df['consensus_category'] = df.apply(assign_consensus, axis=1)
    return df

df_raw = load_and_clean_data()


# ------------------------------------------------------------------------------
# 3. VISIBLE COMPOSING DESK (ARCHIVE FILTERING CONSOLE)
# ------------------------------------------------------------------------------
# Renders an interactive sidebar/expander panel acting as a "Composing Desk" 
# where users can filter the dataset dynamically by year span, genres, consensus tiers, etc.
with st.expander("🖨️ Open Composing Desk (Archive Filtering Console)", expanded=True):
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        min_yr = int(df_raw['release_year'].min())
        max_yr = int(df_raw['release_year'].max())
        selected_year_range = st.slider("Publication Year Span", min_value=min_yr, max_value=max_yr, value=(1980, max_yr))
        
        all_genres = sorted(list(set([g for sublist in df_raw['genre_list'] for g in sublist])))
        selected_genres = st.multiselect("Genre Categories", options=all_genres, default=['Drama', 'Comedy', 'Action & Adventure', 'Mystery & Suspense'])
        if not selected_genres: selected_genres = all_genres

    with col_f2:
        status_options = ['Certified Fresh', 'Fresh', 'Rotten']
        selected_statuses = st.multiselect("Critical Consensus Tier", options=status_options, default=status_options)
        if not selected_statuses: selected_statuses = status_options

        rating_options = sorted(df_raw['rating_clean'].unique().tolist())
        selected_mpaa = st.multiselect("MPAA Content Rating", options=rating_options, default=rating_options)
        if not selected_mpaa: selected_mpaa = rating_options

    with col_f3:
        disconnect_mode = st.selectbox("Editorial Disconnect Focus", [
            "All Archived Records",
            "High Disconnect (|Critic - Audience| ≥ 25 pts)",
            "Audience Over-Loved (Audience +20 pts)",
            "Critics Over-Loved (Critic +20 pts)"
        ])

        search_query = st.text_input("Search Archives (Title/Director/Studio)", value="", placeholder="e.g., Spielberg, Nolan...")


# ------------------------------------------------------------------------------
# 4. FILTERING ENGINE
# ------------------------------------------------------------------------------
# Applies boolean masking to filter the master dataframe based on user widget selections
mask = (
    (df_raw['release_year'] >= selected_year_range[0]) &
    (df_raw['release_year'] <= selected_year_range[1]) &
    (df_raw['tomatometer_status'].isin(selected_statuses)) &
    (df_raw['rating_clean'].isin(selected_mpaa))
)
df_filtered = df_raw[mask].copy()
df_filtered = df_filtered[df_filtered['genre_list'].apply(lambda gl: any(g in selected_genres for g in gl))]

# Filters records further based on specific critic-audience score discrepancy presets
if disconnect_mode == "High Disconnect (|Critic - Audience| ≥ 25 pts)":
    df_filtered = df_filtered[df_filtered['abs_score_difference'] >= 25]
elif disconnect_mode == "Audience Over-Loved (Audience +20 pts)":
    df_filtered = df_filtered[df_filtered['score_difference'] >= 20]
elif disconnect_mode == "Critics Over-Loved (Critic +20 pts)":
    df_filtered = df_filtered[df_filtered['score_difference'] <= -20]

# Filters records by text matching across movie titles, directors, or studio names
if search_query.strip():
    q = search_query.strip().lower()
    df_filtered = df_filtered[
        df_filtered['movie_title'].str.lower().str.contains(q) |
        df_filtered['directors'].str.lower().str.contains(q) |
        df_filtered['studio_name'].str.lower().str.contains(q)
    ]

# Halts app execution and alerts the user if no records match the chosen filter combination
if df_filtered.empty:
    st.warning("⚠️ No records match your active editorial filters. Please revise your parameters in the composing desk.")
    st.stop()


# ------------------------------------------------------------------------------
# 5. GAZETTE MASTHEAD & KPIS
# ------------------------------------------------------------------------------
# Renders the main newspaper header (masthead) containing student metadata and assignment details
st.markdown("""
<div class="gazette-masthead">
    <div style="font-size: 0.7rem; font-weight: 800; text-transform: uppercase; letter-spacing: 3px; color: #5c5952; margin-bottom: 6px;">
        UECS3183 Data Visualisation Techniques • Assignment 2 • Student ID: 2206851
    </div>
    <h1 class="masthead-title">The Cinematic Gazette</h1>
    <div class="masthead-subbar">
        <span><b>Editor:</b> Tee Hue Leng</span>
        <span><b>Edition:</b> Global Film Archives (1914–2019)</span>
        <span><b>Status:</b> Verified & Published</span>
    </div>
</div>

<div class="gazette-story-banner">
    <div class="story-banner-tag">📜 Editorial Mission & Analytical Story Objective</div>
    <div class="story-banner-text">
        <b>Core Objective:</b> To investigate the longitudinal evolution of cinematic reception and systematically analyze the divergence between professional film critics (<i>Tomatometer</i>) and everyday movie audiences across more than a century of filmmaking (1914–2019). Through interactive, multi-dimensional visual analytics, this dashboard tracks historical trends, identifies genre discordances, benchmarks studio consistency and decodes what transforms a film into <i>Universal Acclaim</i>, a <i>Critic Darling</i>, or an audience-championed <i>Cult Classic</i>.
    </div>
</div>
""", unsafe_allow_html=True)

# Calculates summary performance statistics across the filtered dataset
k1, k2, k3, k4, k5 = st.columns(5)
total_movies = len(df_filtered)
avg_critic = df_filtered['tomatometer_rating'].mean()
avg_audience = df_filtered['audience_rating_clean'].mean()
certified_pct = (df_filtered['tomatometer_status'] == 'Certified Fresh').sum() / total_movies * 100 if total_movies > 0 else 0
top_genre = df_filtered['primary_genre'].mode()[0] if not df_filtered.empty else "N/A"

# Displays KPI values within formatted newspaper-style metric cards
with k1:
    st.markdown(f'<div class="print-metric-card"><div class="print-metric-label">Filtered Archives</div><div class="print-metric-val">{total_movies:,}</div></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="print-metric-card"><div class="print-metric-label">Mean Critic</div><div class="print-metric-val" style="color: #b82311;">{avg_critic:.1f}%</div></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="print-metric-card"><div class="print-metric-label">Mean Audience</div><div class="print-metric-val" style="color: #c28e21;">{avg_audience:.1f}%</div></div>', unsafe_allow_html=True)
with k4:
    st.markdown(f'<div class="print-metric-card"><div class="print-metric-label">Certified Fresh</div><div class="print-metric-val" style="color: #3b5343;">{certified_pct:.1f}%</div></div>', unsafe_allow_html=True)
with k5:
    st.markdown(f'<div class="print-metric-card"><div class="print-metric-label">Top Genre</div><div class="print-metric-val" style="font-size: 1.4rem; line-height: 2.3rem;">{top_genre}</div></div>', unsafe_allow_html=True)

st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# 6. STACKED ICON-ON-TOP NAVIGATION BAR
# ------------------------------------------------------------------------------
# Implements an intuitive horizontal navigation menu using `streamlit-option-menu` 
# allowing users to switch seamlessly between analytical views.
selected_nav = option_menu(
    menu_title=None,
    options=["Trends", "Audit Matrix", "Demographics", "Studio Radar", "Box Office Vibe", "Director Hall", "Spotlight", "Arena", "Roulette", "Gallery"],
    icons=["graph-up", "intersect", "pie-chart", "radar", "cash-coin", "award", "search", "shield-shaded", "dice-5", "images"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "6px !important", 
            "background-color": "#eae5d9", 
            "border": "2.5px solid #1c1b18", 
            "border-radius": "12px", 
            "box-shadow": "5px 5px 0px 0px #1c1b18", 
            "margin-bottom": "35px",
            "width": "100% !important",
            "max-width": "100% !important"
        },
        "icon": {
            "color": "#b82311", 
            "font-size": "18px",
            "display": "block",
            "margin": "0 auto 4px auto"
        }, 
        "nav-link": {
            "font-family": "Cinzel, serif", 
            "font-size": "10px", 
            "letter-spacing": "0.3px",
            "text-transform": "uppercase", 
            "font-weight": "700", 
            "color": "#141311", 
            "padding": "10px 0px",
            "margin": "0px 1px",
            "border-radius": "8px",
            "display": "flex",
            "flex-direction": "column",
            "align-items": "center",
            "text-align": "center",
            "flex": "1 1 0px",
            "transition": "all 0.25s ease",
            "--hover-color": "#dfd9cb"
        },
        "nav-link-selected": {
            "background-color": "#1c1b18", 
            "color": "#ffffff", 
            "font-weight": "900",
            "box-shadow": "0 4px 12px rgba(0,0,0,0.15)"
        }
    }
)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 7. CONTENT RENDERED BASED ON THE NAVIGATION SELECTION
# ------------------------------------------------------------------------------

# Section 1: Trends View (Visualizes longitudinal changes in critical ratings, audience ratings, and annual release counts)
if selected_nav == "Trends":
    st.markdown("### Longitudinal Production & Critical Reception Trends")
    yearly = df_filtered.groupby('release_year').agg(
        avg_critic=('tomatometer_rating', 'mean'),
        avg_audience=('audience_rating_clean', 'mean'),
        count=('movie_title', 'count')
    ).reset_index()

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=yearly['release_year'], y=yearly['avg_critic'], name="Critic Rating (%)", line=dict(color="#b82311", width=3), mode='lines+markers'), secondary_y=False)
    fig.add_trace(go.Scatter(x=yearly['release_year'], y=yearly['avg_audience'], name="Audience Rating (%)", line=dict(color="#c28e21", width=3, dash='dash'), mode='lines'), secondary_y=False)
    fig.add_trace(go.Bar(x=yearly['release_year'], y=yearly['count'], name="Annual Volume", marker=dict(color="#3b5343", opacity=0.35)), secondary_y=True)
    
    fig.update_layout(
        template='plotly_white', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,1)',
        font=dict(family="Plus Jakarta Sans", color="#141311"), height=480, margin=dict(t=20, b=20, l=20, r=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

# Section 2: Audit Matrix View (An interactive animated scatter plot displaying year-by-year critical vs audience ratings)
elif selected_nav == "Audit Matrix":
    st.markdown("### The Dual-Rating Audit Matrix (Animated Year-by-Year Evolution)")
    st.markdown("<p style='font-size:0.85rem; color:#5c5952;'>Use the playback controls and timeline slider below to animate year-by-year critical vs. audience ratings.</p>", unsafe_allow_html=True)
    
    min_matrix_yr = int(df_filtered['release_year'].min())
    max_matrix_yr = int(df_filtered['release_year'].max())

    # Maintains state for the year animation loop
    if 'audit_year' not in st.session_state:
        st.session_state['audit_year'] = min_matrix_yr
    if 'is_playing' not in st.session_state:
        st.session_state['is_playing'] = False

    # Layout for playback buttons and timeline control slider
    c_play, c_pause, c_slider = st.columns([1, 1, 8])
    with c_play:
        if st.button("▶ Play", use_container_width=True):
            st.session_state['is_playing'] = True
    with c_pause:
        if st.button("⏸ Pause", use_container_width=True):
            st.session_state['is_playing'] = False
    with c_slider:
        selected_audit_year = st.slider(
            "Audit Year Timeline", 
            min_value=min_matrix_yr, 
            max_value=max_matrix_yr, 
            value=st.session_state['audit_year'],
            label_visibility="collapsed"
        )
    
    if selected_audit_year != st.session_state['audit_year']:
        st.session_state['audit_year'] = selected_audit_year

    audit_year_df = df_filtered[df_filtered['release_year'] == st.session_state['audit_year']]
    
    fig_scatter = px.scatter(
        audit_year_df, x='tomatometer_rating', y='audience_rating_clean',
        color='tomatometer_status', hover_name='movie_title',
        color_discrete_map={'Certified Fresh': '#b82311', 'Fresh': '#3b5343', 'Rotten': '#8c887d'},
        template='plotly_white', height=500,
        range_x=[-5, 105], range_y=[-5, 105],
        title=f"Movie Releases & Ratings in Year {st.session_state['audit_year']} (Total: {len(audit_year_df)} films)"
    )
    fig_scatter.add_vline(x=60, line_dash="dash", line_color="#141311")
    fig_scatter.add_hline(y=60, line_dash="dash", line_color="#141311")
    
    fig_scatter.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(255,255,255,1)', 
        font=dict(family="Plus Jakarta Sans", color="#141311"), 
        margin=dict(t=40, b=20, l=20, r=20)
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Handles automated year increments when play is activated
    if st.session_state['is_playing']:
        if st.session_state['audit_year'] < max_matrix_yr:
            st.session_state['audit_year'] += 1
            time.sleep(0.4)
            st.rerun()
        else:
            st.session_state['is_playing'] = False

# Section 3: Demographics View (Visualizes primary genre distribution volumes and movie runtime distributions across quality tiers)
elif selected_nav == "Demographics":
    st.markdown("### Genre Frequency & Runtime Analytics")
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        genre_counts = df_filtered['primary_genre'].value_counts().reset_index()
        genre_counts.columns = ['Genre', 'Count']
        fig_genre = px.bar(genre_counts.head(10), x='Count', y='Genre', orientation='h', template='plotly_white', color='Count', color_continuous_scale='Reds', title="Top Primary Genres by Volume")
        fig_genre.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,1)', font=dict(family="Plus Jakarta Sans", color="#141311"), yaxis=dict(categoryorder='total ascending'), height=400)
        st.plotly_chart(fig_genre, use_container_width=True)
    with col_g2:
        top_genres = df_filtered['primary_genre'].value_counts().head(6).index.tolist()
        box_data = df_filtered[df_filtered['primary_genre'].isin(top_genres)]
        fig_box = px.box(box_data, x='primary_genre', y='runtime_clean', color='tomatometer_status', color_discrete_map={'Certified Fresh': '#b82311', 'Fresh': '#3b5343', 'Rotten': '#8c887d'}, template='plotly_white', title="Runtime Spread by Quality Tier")
        fig_box.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,1)', font=dict(family="Plus Jakarta Sans", color="#141311"), height=400)
        st.plotly_chart(fig_box, use_container_width=True)

# Section 4: Studio Radar View (Provides multi-metric comparative radar charts for major production studios)
elif selected_nav == "Studio Radar":
    st.markdown("### 🏢 Interactive Studio Performance Radar & Benchmarking")
    st.markdown("<p style='font-size:0.85rem; color:#5c5952;'>Compare major production studios across multiple metrics simultaneously using radar coordinates.</p>", unsafe_allow_html=True)
    
    studio_counts = df_filtered['studio_name'].value_counts()
    valid_studios = studio_counts[studio_counts >= 15].index.tolist()
    if len(valid_studios) < 3:
        valid_studios = studio_counts.head(5).index.tolist()
        
    selected_radar_studios = st.multiselect("Select Studios to Benchmark (Max 4):", options=valid_studios, default=valid_studios[:min(3, len(valid_studios))])
    
    if selected_radar_studios:
        radar_fig = go.Figure()
        categories = ['Mean Critic Score', 'Mean Audience Score', 'Certified Fresh %', 'Catalog Volume (Scaled)']
        
        for studio in selected_radar_studios[:4]:
            sub_df = df_filtered[df_filtered['studio_name'] == studio]
            m_crit = sub_df['tomatometer_rating'].mean()
            m_aud = sub_df['audience_rating_clean'].mean()
            cert_pct = (sub_df['tomatometer_status'] == 'Certified Fresh').sum() / len(sub_df) * 100
            vol_scaled = min(100, len(sub_df) * 2)
            
            radar_fig.add_trace(go.Scatterpolar(
                r=[m_crit, m_aud, cert_pct, vol_scaled],
                theta=categories,
                fill='toself',
                name=studio
            ))
            
        radar_fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            template='plotly_white',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(255,255,255,1)',
            font=dict(family="Plus Jakarta Sans", color="#141311"),
            height=450,
            margin=dict(t=30, b=30, l=30, r=30)
        )
        st.plotly_chart(radar_fig, use_container_width=True)
    else:
        st.info("Please select at least one studio above to render the radar chart.")

# Section 5: Box Office Vibe View (Explores catalog production volume by studio and runtime-to-rating correlations)
elif selected_nav == "Box Office Vibe":
    st.markdown("### 💰 Box Office Volume & Financial Analytics")
    st.markdown("<p style='font-size:0.85rem; color:#5c5952;'>Explore catalog distribution volumes, runtime vs. rating correlations, and studio outputs.</p>", unsafe_allow_html=True)
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        studio_vol = df_filtered['studio_name'].value_counts().head(10).reset_index()
        studio_vol.columns = ['Studio', 'Movie Count']
        fig_st = px.bar(
            studio_vol, x='Movie Count', y='Studio', orientation='h', 
            template='plotly_white', title="Top Studios by Catalog Output",
            color='Movie Count', color_continuous_scale='Reds'
        )
        fig_st.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,1)', font=dict(family="Plus Jakarta Sans", color="#141311"), yaxis=dict(categoryorder='total ascending'), height=400, coloraxis_showscale=False, margin=dict(t=30, b=20, l=20, r=20))
        st.plotly_chart(fig_st, use_container_width=True)
    with col_b2:
        fig_scatter_runtime = px.scatter(
            df_filtered.sample(min(len(df_filtered), 1000), random_state=42),
            x='runtime_clean', y='tomatometer_rating',
            color='tomatometer_status', color_discrete_map={'Certified Fresh': '#b82311', 'Fresh': '#3b5343', 'Rotten': '#8c887d'},
            template='plotly_white', title="Runtime vs. Critic Rating Correlation"
        )
        fig_scatter_runtime.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,1)', font=dict(family="Plus Jakarta Sans", color="#141311"), height=400, margin=dict(t=30, b=20, l=20, r=20))
        st.plotly_chart(fig_scatter_runtime, use_container_width=True)

# Section 6: Director Hall View (Ranks top-performing film directors based on average critical scores and catalog volume)
elif selected_nav == "Director Hall":
    st.markdown("### 🏆 Director Hall of Fame & Critical Success Ranking")
    st.markdown("<p style='font-size:0.85rem; color:#5c5952;'>Highlighting acclaimed directors based on average critic scores and total film volume.</p>", unsafe_allow_html=True)
    
    director_stats = df_filtered[df_filtered['directors'] != 'Unknown'].groupby('directors').agg(
        movie_count=('movie_title', 'count'),
        avg_critic=('tomatometer_rating', 'mean'),
        avg_audience=('audience_rating_clean', 'mean')
    ).reset_index()
    
    director_filtered = director_stats[director_stats['movie_count'] >= 2].sort_values(by='avg_critic', ascending=False)
    
    if director_filtered.empty:
        director_filtered = director_stats.sort_values(by='avg_critic', ascending=False)
        
    top_directors = director_filtered.head(15)
    
    fig_dir = px.bar(
        top_directors, x='avg_critic', y='directors', orientation='h',
        text='movie_count', template='plotly_white',
        title="Top Rated Directors (Min. 2 Films in Filter)",
        color='avg_critic', color_continuous_scale='Reds'
    )
    fig_dir.update_traces(texttemplate='Films: %{text}', textposition='outside')
    fig_dir.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,1)',
        font=dict(family="Plus Jakarta Sans", color="#141311"),
        yaxis=dict(categoryorder='total ascending'),
        height=500, margin=dict(t=30, b=20, l=20, r=40)
    )
    st.plotly_chart(fig_dir, use_container_width=True)

# Section 7: Spotlight View (Provides deep-dive reviews, movie metadata, synopses, and external YouTube trailer links)
elif selected_nav == "Spotlight":
    st.markdown("### 🔍 Feature Film Spotlight & Trailer Integration")
    spot_titles = df_filtered.sort_values(by='tomatometer_rating', ascending=False)['movie_title'].tolist()
    selected_spotlight = st.selectbox("Select Film Title for Detailed Review:", options=spot_titles, index=0)
    
    movie_spot = df_filtered[df_filtered['movie_title'] == selected_spotlight].iloc[0]
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    sc1, sc2, sc3 = st.columns([3.5, 4.5, 4])
    with sc1:
        st.image(movie_spot['poster_url'], use_container_width=True)
        yt_link = f"https://www.youtube.com/results?search_query={movie_spot['movie_title'].replace(' ', '+')}+{movie_spot['release_year']}+official+trailer"
        st.markdown(f'<a href="{yt_link}" target="_blank" style="text-decoration:none;"><div style="background:#D3D3D3; color:#00008B; text-align:center; padding:11px; border-radius:6px; font-weight:700; font-size:0.85rem; margin-top:12px; border: 1px solid #A9A9A9;">▶ Watch Trailer on YouTube</div></a>', unsafe_allow_html=True)
    with sc2:
        st.markdown(f"## {movie_spot['movie_title']} ({movie_spot['release_year']})")
        st.markdown(f"**Director:** {movie_spot['directors']} | **Studio:** {movie_spot['studio_name']}")
        st.markdown(f"**MPAA Rating:** `{movie_spot['rating_clean']}` | **Runtime:** `{int(movie_spot['runtime_clean'])} mins`")
        st.markdown(f"**Genre:** {movie_spot['genre']}")
        st.markdown(f"**Cast:** {movie_spot['cast']}")
        st.markdown("---")
        st.markdown(f"**Synopsis:** {movie_spot['movie_info']}")
    with sc3:
        st.markdown("### Critical Consensus")
        st.info(f"\"{movie_spot['critics_consensus']}\"")
        st.markdown(f"""
        <div style="background:#eae5d9; border:2px solid #141311; padding:15px; margin-top:15px; border-radius:6px;">
            <div style="font-weight:800; text-transform:uppercase; font-size:0.75rem; letter-spacing:1px;">Evaluation Ratings</div>
            <div style="display:flex; justify-content:space-between; margin-top:10px; font-size:1.3rem; font-family: Cinzel; font-weight: 700;">
                <span style="color:#b82311;">Critic: {movie_spot['tomatometer_rating']}%</span>
                <span style="color:#c28e21;">Audience: {movie_spot['audience_rating_clean']}%</span>
            </div>
            <div style="margin-top:8px; font-size:0.8rem; font-weight:700; color:#5c5952;">Consensus Tag: {movie_spot['consensus_category']}</div>
        </div>
        """, unsafe_allow_html=True)

# Section 8: Arena View (Facilitates side-by-side comparative analysis between two selected films)
elif selected_nav == "Arena":
    st.markdown("### ⚔️ Head-to-Head Contender Comparison Arena")
    comp_titles = df_filtered['movie_title'].tolist()
    cc1, cc2 = st.columns(2)
    with cc1:
        mov_a_name = st.selectbox("Select Contender Alpha:", options=comp_titles, index=0)
        mov_a = df_filtered[df_filtered['movie_title'] == mov_a_name].iloc[0]
    with cc2:
        default_b = min(1, len(comp_titles)-1)
        mov_b_name = st.selectbox("Select Contender Beta:", options=comp_titles, index=default_b)
        mov_b = df_filtered[df_filtered['movie_title'] == mov_b_name].iloc[0]

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    bc1, bc_mid, bc2 = st.columns([5, 2, 5])
    with bc1:
        st.markdown(f'<div class="film-card"><img src="{mov_a["poster_url"]}" class="film-poster"><div class="film-body"><div class="film-title">{mov_a["movie_title"]}</div><div style="font-size:0.75rem; font-weight:700; color:#5c5952; margin-top:4px;">{mov_a["release_year"]} • {mov_a["primary_genre"]}</div><div style="display:flex; justify-content:space-between; margin-top:10px; font-weight:700;"><span style="color:#b82311;">Crit: {mov_a["tomatometer_rating"]}%</span><span style="color:#c28e21;">Aud: {mov_a["audience_rating_clean"]}%</span></div></div></div>', unsafe_allow_html=True)
    with bc_mid:
        st.markdown('<div style="display:flex; height:100%; justify-content:center; align-items:center;"><h1 style="font-family:Cinzel; font-size:3rem; margin:0; font-weight:900;">VS</h1></div>', unsafe_allow_html=True)
    with bc2:
        st.markdown(f'<div class="film-card"><img src="{mov_b["poster_url"]}" class="film-poster"><div class="film-body"><div class="film-title">{mov_b["movie_title"]}</div><div style="font-size:0.75rem; font-weight:700; color:#5c5952; margin-top:4px;">{mov_b["release_year"]} • {mov_b["primary_genre"]}</div><div style="display:flex; justify-content:space-between; margin-top:10px; font-weight:700;"><span style="color:#b82311;">Crit: {mov_b["tomatometer_rating"]}%</span><span style="color:#c28e21;">Aud: {mov_b["audience_rating_clean"]}%</span></div></div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    comparison_df = pd.DataFrame({
        'Evaluation Metric': ['Critic Score (%)', 'Audience Score (%)', 'Runtime (Minutes)'],
        mov_a['movie_title']: [mov_a['tomatometer_rating'], mov_a['audience_rating_clean'], mov_a['runtime_clean']],
        mov_b['movie_title']: [mov_b['tomatometer_rating'], mov_b['audience_rating_clean'], mov_b['runtime_clean']]
    })
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(name=mov_a['movie_title'], x=comparison_df['Evaluation Metric'], y=comparison_df[mov_a['movie_title']], marker_color='#b82311'))
    fig_comp.add_trace(go.Bar(name=mov_b['movie_title'], x=comparison_df['Evaluation Metric'], y=comparison_df[mov_b['movie_title']], marker_color='#c28e21'))
    fig_comp.update_layout(barmode='group', template='plotly_white', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,1)', font=dict(family="Plus Jakarta Sans", color="#141311"), height=350, margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig_comp, use_container_width=True)

# Section 9: Roulette View (A gamified recommendation tool that picks a movie based on selected user moods)
elif selected_nav == "Roulette":
    st.markdown("### 🎲 Cinematic Recommendation Roulette")
    st.markdown("<p style='font-size:0.85rem; color:#5c5952;'>Can't decide what movie to watch? Spin the wheel based on your mood and let the archives choose for you!</p>", unsafe_allow_html=True)
    
    col_r1, col_r2 = st.columns([4, 8])
    with col_r1:
        mood = st.selectbox("Select Your Current Viewing Mood:", [
            "Universal Acclaim (Must Watch Masterpieces)",
            "Cult Classics (Audience Favorites)",
            "Critic Darlings (Intellectual / Prestige)",
            "Universal Flops (Guilty Pleasures / Trash Cinema)",
            "Total Random Roll"
        ])
        
        spin_btn = st.button("🎲 Spin the Roulette Reel!", use_container_width=True)
        
    with col_r2:
        if spin_btn or 'roulette_pick' not in st.session_state:
            if "Universal Acclaim" in mood:
                pool = df_filtered[df_filtered['consensus_category'] == 'Universal Acclaim']
            elif "Cult Classics" in mood:
                pool = df_filtered[df_filtered['consensus_category'] == 'Cult Classic']
            elif "Critic Darlings" in mood:
                pool = df_filtered[df_filtered['consensus_category'] == 'Critic Darling']
            elif "Universal Flops" in mood:
                pool = df_filtered[df_filtered['consensus_category'] == 'Universal Flop']
            else:
                pool = df_filtered
                
            if pool.empty:
                pool = df_filtered
            st.session_state['roulette_pick'] = pool.sample(1).iloc[0]
            
        r_pick = st.session_state['roulette_pick']
        
        st.markdown(f"""
        <div class="film-card" style="padding: 22px; display: flex; gap: 20px; align-items: center;">
            <img src="{r_pick['poster_url']}" style="width: 145px; height: 210px; object-fit: cover; border: 2px solid #141311;">
            <div>
                <span style="background: #b82311; color: #fff; padding: 3px 10px; font-size: 0.7rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px;">Selected For You</span>
                <h2 style="font-family: Cinzel; font-size: 1.8rem; margin: 8px 0 4px 0;">{r_pick['movie_title']} ({r_pick['release_year']})</h2>
                <p style="font-size: 0.8rem; font-weight: 700; color: #5c5952; margin-bottom: 8px;">Director: {r_pick['directors']} | Genre: {r_pick['primary_genre']}</p>
                <p style="font-size: 0.85rem; line-height: 1.4; color: #141311; margin-bottom: 12px;">{r_pick['movie_info'][:160]}...</p>
                <div style="font-family: Cinzel; font-weight: 700; font-size: 0.95rem;">
                    <span style="color: #b82311; margin-right: 20px;">Critic: {r_pick['tomatometer_rating']}%</span>
                    <span style="color: #c28e21;">Audience: {r_pick['audience_rating_clean']}%</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Section 10: Gallery View (Displays an immersive grid showcasing featured film posters and sorting options)
elif selected_nav == "Gallery":
    st.markdown("### 📰 Front Page Featured Film Showcase")
    gc1, gc2 = st.columns(2)
    with gc1:
        gallery_sort = st.selectbox("Sort Gallery By:", options=["Highest Critic Score", "Highest Audience Score", "Biggest Discrepancy", "Newest Releases"])
    with gc2:
        gallery_limit = st.select_slider("Number of Posters to Display:", options=[8, 12, 16, 24, 36], value=12)

    gal_df = df_filtered.copy()
    if gallery_sort == "Highest Critic Score": gal_df = gal_df.sort_values(by='tomatometer_rating', ascending=False)
    elif gallery_sort == "Highest Audience Score": gal_df = gal_df.sort_values(by='audience_rating_clean', ascending=False)
    elif gallery_sort == "Biggest Discrepancy": gal_df = gal_df.sort_values(by='abs_score_difference', ascending=False)
    elif gallery_sort == "Newest Releases": gal_df = gal_df.sort_values(by='release_year', ascending=False)

    display_sample = gal_df.head(gallery_limit)
    cols = st.columns(4)
    for idx, (_, row) in enumerate(display_sample.iterrows()):
        with cols[idx % 4]:
            st.markdown(f"""
            <div class="film-card">
                <img src="{row['poster_url']}" class="film-poster">
                <div class="film-body">
                    <div class="film-title">{row['movie_title']}</div>
                    <div style="font-size: 0.75rem; font-weight: 700; color: #5c5952; margin-top: 4px; text-transform: uppercase;">{row['release_year']} • {row['primary_genre']}</div>
                    <div style="display: flex; justify-content: space-between; margin-top: 10px; font-size: 0.8rem; font-weight: 700; border-top: 1px solid #141311; padding-top: 6px;">
                        <span style="color: #b82311;">Crit: {row['tomatometer_rating']}%</span>
                        <span style="color: #c28e21;">Aud: {row['audience_rating_clean']}%</span>
                    </div>
                </div>
            </div>
            <div style="height: 18px;"></div>
            """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 8. EXPORT DATA SECTION
# ------------------------------------------------------------------------------
# Provides an expander panel allowing users to view the raw filtered tabular records and download them as a CSV file.
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
with st.expander("📁 Access Full Filtered Archives Table & CSV Export"):
    export_cols = ['movie_title', 'release_year', 'rating_clean', 'genre', 'directors', 'studio_name', 'tomatometer_status', 'tomatometer_rating', 'audience_rating_clean', 'consensus_category']
    st.dataframe(df_filtered[export_cols], use_container_width=True, height=350)
    
    csv_bytes = df_filtered[export_cols].to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Filtered Gazette Archive (.CSV)", data=csv_bytes, file_name="cinematic_gazette_archives.csv", mime="text/csv")