from pathlib import Path
import base64
from html import escape

import pandas as pd
import plotly.express as px
import streamlit as st


ASSETS_DIR = Path(__file__).resolve().parent / "assets"
MAP_PATH = ASSETS_DIR / "SVI_geographic_map_2025.html"
LOGO_PATH = ASSETS_DIR / "logo_sbl.png"
SBL_WEBSITE = "https://sblconsultancy.it/"  
SBL_NAVY = "#1E344B"
SBL_NAVY_DARK = "#172B40"
SBL_SLATE = "#345A78"
SBL_ORANGE = "#F7931E"
SBL_SKY = "#32A7DA"
SBL_ICE = "#ECF5FA"
SBL_PAPER = "#F7FAFD"
SBL_BORDER = "#DDE6EE"

DASHBOARD_COLORS = [
    SBL_NAVY,
    SBL_ORANGE,
    SBL_SKY,
    SBL_SLATE,
    "#759CB9",
    "#E2B166",
]
px.defaults.color_discrete_sequence = DASHBOARD_COLORS
px.defaults.template = "plotly_white"


if LOGO_PATH.is_file():
    from PIL import Image
    with Image.open(LOGO_PATH) as logo_image:
        PAGE_ICON = logo_image.copy()
else:
    PAGE_ICON = "⚽"

st.set_page_config(
    page_title="SBL Consultancy | SVI Predictor",
    page_icon=PAGE_ICON,
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --sbl-navy: #1E344B;
        --sbl-deep: #172B40;
        --sbl-orange: #F7931E;
        --sbl-sky: #32A7DA;
        --sbl-paper: #F4F7FB;
        --sbl-ink: #21364C;
        --sbl-muted: #465A70;
        --sbl-line: #DCE5EF;
    }

    /* Identita' visiva: canvas chiaro anche nel browser del responsabile. */
    html, body, [data-testid="stAppViewContainer"],
    [data-testid="stMain"], .main, .stApp {
        background: var(--sbl-paper) !important;
        color: var(--sbl-ink) !important;
    }
    header[data-testid="stHeader"] {
        background: var(--sbl-paper) !important;
        box-shadow: none !important;
    }
    [data-testid="stMainBlockContainer"], .main .block-container {
        padding-top: 4.2rem !important;
        padding-bottom: 2.6rem !important;
        max-width: 1650px;
    }
    @media (max-width: 768px) {
        [data-testid="stMainBlockContainer"], .main .block-container {
            padding-top: 4rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
    }
    [data-testid="stMain"] h1,
    [data-testid="stMain"] h2,
    [data-testid="stMain"] h3,
    [data-testid="stMain"] h4 {
        color: var(--sbl-navy) !important;
        letter-spacing: -0.025em;
    }
    [data-testid="stMain"] p,
    [data-testid="stMain"] label {
        color: var(--sbl-ink);
    }

    /* Hero compatto: logo interamente visibile e cliccabile. */
    .sbl-hero {
        display: flex; align-items: center; gap: 1.15rem;
        background: #fff;
        border: 1px solid var(--sbl-line);
        border-radius: 16px;
        padding: 1.15rem 1.45rem;
        box-shadow: 0 7px 24px rgba(30, 52, 75, .07);
        margin: .25rem 0 1.1rem;
        min-height: 115px;
    }
    .sbl-logo-link { flex-shrink: 0; display: inline-flex; align-items: center; justify-content: center; }
    .sbl-logo-link img {
        width: 78px; height: 78px; max-width: 100%;
        object-fit: contain; display: block; border-radius: 12px;
    }
    .sbl-logo-link:focus-visible { outline: 3px solid var(--sbl-orange); border-radius: 12px; }
    .sbl-hero-copy { min-width: 0; }
    .sbl-eyebrow {
        color: #426480 !important; font-size: .71rem;
        letter-spacing: .16em; font-weight: 800;
        text-transform: uppercase; margin-bottom: .3rem;
    }
    .sbl-hero h1 {
        color: var(--sbl-navy) !important;
        font-size: clamp(1.45rem, 2.2vw, 2.28rem);
        font-weight: 780; line-height: 1.2;
        margin: 0 0 .42rem !important;
        overflow-wrap: anywhere;
    }
    .sbl-hero p {
        color: var(--sbl-muted) !important;
        font-size: .92rem; line-height: 1.5; margin: 0 !important;
    }
    @media (max-width: 560px) {
        .sbl-hero { gap: .75rem; padding: .85rem; min-height: auto; }
        .sbl-logo-link img { width: 55px; height: 55px; }
        .sbl-hero h1 { font-size: 1.32rem; }
        .sbl-hero p { font-size: .80rem; }
    }

    /* Sidebar coordinata: logo cliccabile ma non tagliato. */
    section[data-testid="stSidebar"] {
        background: linear-gradient(170deg, var(--sbl-navy), var(--sbl-deep)) !important;
        border-right: 3px solid var(--sbl-orange);
    }
    section[data-testid="stSidebar"] > div { background: transparent !important; }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 { color: #F7FAFE !important; }
    section[data-testid="stSidebar"] hr { border-color: rgba(255, 255, 255, .24); }
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,
    section[data-testid="stSidebar"] small { color: #D7E3EF !important; }
    .sbl-sidebar-brand { padding: .2rem 0 .4rem; }
    .sbl-sidebar-brand .sbl-logo-link img { width: 154px; height: 150px; }
    .sbl-sidebar-brand .sbl-logo-link:hover img { filter: drop-shadow(0 4px 7px rgba(255,255,255,.14)); }

    /* KPI: il label dei metric era bianco su fondo bianco nel browser del responsabile.
       Fissiamo esplicitamente anche il colore degli elementi annidati. */
    div[data-testid="stMetric"] {
        box-sizing: border-box;
        background: #fff !important;
        border: 1px solid var(--sbl-line) !important;
        border-top: 3px solid var(--sbl-orange) !important;
        border-radius: 14px !important;
        min-height: 137px;
        padding: 17px 18px !important;
        box-shadow: 0 5px 16px rgba(30,52,75,.065);
        overflow: visible !important;
    }
    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricLabel"] *,
    div[data-testid="stMetric"] [data-testid="stMetricLabel"] p {
        color: #42546A !important;
        -webkit-text-fill-color: #42546A !important;
        opacity: 1 !important;
        visibility: visible !important;
        font-size: .88rem !important;
        font-weight: 700 !important;
        line-height: 1.35 !important;
        white-space: normal !important;
        overflow: visible !important;
    }
    div[data-testid="stMetricLabel"] {
        min-height: 2.25rem;
        margin-bottom: .48rem;
    }
    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] * {
        color: var(--sbl-navy) !important;
        -webkit-text-fill-color: var(--sbl-navy) !important;
        opacity: 1 !important;
        font-weight: 750 !important;
    }
    div[data-testid="stMetricValue"] { font-size: clamp(1.35rem, 1.7vw, 2rem); }
    div[data-testid="stMetricDelta"], div[data-testid="stMetricDelta"] * {
        opacity: 1 !important;
    }

    /* Tabs leggibili e navigazione attiva nel colore aziendale. */
    div[data-testid="stTabs"] [role="tablist"] {
        gap: .25rem;
        border-bottom: 1px solid var(--sbl-line);
    }
    div[data-testid="stTabs"] [role="tab"] {
        color: #38526C !important;
        font-weight: 650 !important;
        border-radius: 8px 8px 0 0;
        padding: .65rem .9rem;
    }
    div[data-testid="stTabs"] [role="tab"]:hover {
        background: #E7F1F8 !important;
        color: var(--sbl-navy) !important;
    }
    div[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        color: var(--sbl-navy) !important;
        background: #EAF2F8 !important;
        border-bottom-color: var(--sbl-orange) !important;
        box-shadow: inset 0 -2px var(--sbl-orange);
    }
    div[data-testid="stTabs"] [role="tab"]:focus-visible { outline: 2px solid var(--sbl-orange); }

    /* Input e menu: niente dropdown nero su pagina chiara. */
    [data-testid="stMain"] div[data-baseweb="select"] > div,
    [data-testid="stMain"] div[data-baseweb="input"] > div,
    [data-testid="stMain"] div[data-baseweb="base-input"],
    [data-testid="stMain"] div[data-baseweb="select"] input,
    [data-testid="stMain"] input[type="number"] {
        background: #fff !important;
        color: var(--sbl-ink) !important;
        border-color: var(--sbl-line) !important;
    }
    [data-baseweb="popover"], [data-baseweb="popover"] > div,
    ul[role="listbox"], div[role="listbox"], [data-baseweb="menu"] {
        background: #fff !important;
        color: var(--sbl-ink) !important;
        border-color: var(--sbl-line) !important;
    }
    li[role="option"], li[role="option"] *,
    [role="option"], [role="option"] * {
        color: var(--sbl-ink) !important;
    }
    [role="option"]:hover, [role="option"][aria-selected="true"] {
        background: #E8F3FC !important;
    }
    [data-testid="stMain"] button[kind="primary"] {
        background: var(--sbl-navy) !important;
        color: #fff !important;
        border-color: var(--sbl-navy) !important;
    }
    [data-testid="stMain"] button:hover { border-color: var(--sbl-orange) !important; }
    [data-testid="stDataFrame"], [data-testid="stAlert"],
    [data-testid="stPlotlyChart"] { border-radius: 12px; }
    [data-testid="stDataFrame"], [data-testid="stPlotlyChart"] {
        border: 1px solid var(--sbl-line);
        background: #fff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

ROOT = Path(__file__).resolve().parent.parent
FINAL_DIR = ROOT / "data" / "final"

@st.cache_data
def load_csv(filename):

    path = FINAL_DIR / filename

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}"
        )

    return pd.read_csv(path, low_memory=False)


try:

    svi = load_csv(
        "sponsorship_value_index_BIGFIVE_96_2025.csv"
    )

    roi = load_csv(
        "BIG_FIVE_SOCIAL_TV_ROI_MASTER_96CLUBS_2024_25.csv"
    )

    recommendations = load_csv(
        "sponsor_club_recommendation_master_FINAL_2025.csv"
    )

    recommendations_top3 = load_csv(
        "sponsor_club_recommendation_TOP3_FINAL_2025.csv"
    )

except Exception as exc:

    st.error(
        "Unable to load the required datasets."
    )

    st.exception(exc)

    st.stop()

required_svi = [
    "club_name",
    "league",
    "predicted_sponsorship_eur_m",
    "SVI_2025",
    "svi_rank",
]

required_roi = [
    "club_name",
    "predicted_sponsorship_eur_m",
    "total_media_value_eur_m",
    "total_roi_proxy_pct",
    "league_final",
]

missing_svi = [
    col for col in required_svi
    if col not in svi.columns
]

missing_roi = [
    col for col in required_roi
    if col not in roi.columns
]

if missing_svi or missing_roi:

    st.error(
        "Some required dataset columns are missing."
    )

    st.write("Missing SVI columns:", missing_svi)
    st.write("Missing ROI columns:", missing_roi)

    st.stop()

svi = svi.copy()
roi = roi.copy()

for col in [
    "predicted_sponsorship_eur_m",
    "SVI_2025",
    "svi_rank",
]:

    svi[col] = pd.to_numeric(
        svi[col],
        errors="coerce"
    )


for col in [
    "predicted_sponsorship_eur_m",
    "total_media_value_eur_m",
    "total_roi_proxy_pct",
]:

    roi[col] = pd.to_numeric(
        roi[col],
        errors="coerce"
    )


svi = svi.sort_values(
    "svi_rank",
    ascending=True
)

if LOGO_PATH.is_file():
    LOGO_DATA_URL = (
        "data:image/png;base64,"
        + base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
    )
    SITE_LINK = escape(SBL_WEBSITE, quote=True)
    SBL_LOGO_LINK = (
        f'<a class="sbl-logo-link" href="{SITE_LINK}" '
        f'target="_blank" rel="noopener noreferrer" '
        f'aria-label="Open SBL Consultancy website" '
        f'title="Visit SBL Consultancy website">'
        f'<img src="{LOGO_DATA_URL}" alt="SBL Consultancy logo" />'
        f'</a>'
    )
else:
    SBL_LOGO_LINK = (
        '<span style="font-weight:800;color:#1E344B">SBL Consultancy</span>'
    )

with st.sidebar:

    st.markdown(
        f'<div class="sbl-sidebar-brand">{SBL_LOGO_LINK}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### SVI Predictor")
    st.caption("SBL CONSULTANCY · FOOTBALL ANALYTICS")

    st.write(
        "Interactive sponsorship analytics "
        "for European football clubs."
    )

    st.divider()

    st.subheader("Project scope")

    st.write(
        "**SVI ranking:** 2025 scoring universe "
        "(96 clubs)."
    )

    st.write(
        "**ROI analysis:** 2024/25 competition "
        "universe (96 clubs)."
    )

    st.divider()

    st.caption(
        "The dashboard presents model estimates "
        "and media-value proxies, not verified "
        "sponsorship transaction prices or "
        "realized investment returns."
    )

st.markdown(
    f"""
    <div class="sbl-hero">
        {SBL_LOGO_LINK}
        <div class="sbl-hero-copy">
            <div class="sbl-eyebrow">SBL CONSULTANCY / FOOTBALL ANALYTICS</div>
            <h1>Sponsorship Value Index Predictor</h1>
            <p>Club valuation, sponsorship ranking and estimated Social + TV media return.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

(
    overview_tab,
    svi_tab,
    club_tab,
    recommendation_tab,
    roi_tab,
    map_tab,
    quality_tab,
) = st.tabs(
    [
        "Overview",
        "SVI & Club Ranking",
        "Club Explorer",
        "Sponsor–Club Recommendation",
        "Social + TV ROI",
        "Geographic SVI Map",
        "Model & Data Quality",
    ]
)
with overview_tab:

    st.header("Project Overview")

    st.write(
        "A three-step decision-support workflow: explore the model's "
        "club sponsorship estimates, examine sponsor–club digital "
        "compatibility, and simulate a potential media-value return "
        "from the brand sponsor's perspective."
    )

    st.info(
        "The SVI ranking uses the 2025 scoring universe, while the "
        "Social + TV analysis uses the 2024/25 competition universe. "
        "Both include 96 club records but are not the same set of "
        "clubs or necessarily the same reference period."
    )

    roi_coverage_overview = (
        int(pd.to_numeric(roi["total_roi_pct"], errors="coerce").notna().sum())
        if "total_roi_pct" in roi.columns
        else 0
    )

    summary_1, summary_2, summary_3, summary_4 = st.columns(4)
    summary_1.metric("Clubs in SVI ranking", len(svi))
    summary_2.metric(
        "Sponsor profiles",
        recommendations["sponsor_entity_key"].dropna().nunique()
    )
    summary_3.metric(
        "ROI benchmark coverage",
        f"{roi_coverage_overview} / {len(roi)}"
    )
    summary_4.metric("Model input features", 40)

    st.divider()
    st.subheader("How to use the dashboard")

    workflow_1, workflow_2, workflow_3 = st.columns(3)

    with workflow_1:
        st.markdown("#### 1 · Club valuation")
        st.write(
            "Use **SVI & Club Ranking** or **Club Explorer** to compare "
            "model-predicted sponsorship values (€m) and relative SVI "
            "positions (0–100) within the 2025 scoring universe."
        )

    with workflow_2:
        st.markdown("#### 2 · Sponsor–club fit")
        st.write(
            "Choose a sponsor profile in **Sponsor–Club Recommendation**. "
            "Review the saved recommendation order and the digital and "
            "platform-mix compatibility measures; then select a club."
        )

    with workflow_3:
        st.markdown("#### 3 · Brand ROI scenario")
        st.write(
            "Transfer the selected club to **Social + TV ROI**. Enter an "
            "illustrative sponsorship fee and a hypothetical share of "
            "club media value attributable to the brand to simulate its "
            "media-value ROI proxy."
        )

    st.caption(
        "The club-level ROI benchmark uses aggregate club media value "
        "and a predicted sponsorship reference, whereas the individual "
        "brand scenario uses user-entered assumptions. Neither is a "
        "verified realized financial return."
    )

    st.divider()

    st.subheader("SVI ranking — Top 10")

    overview_top10 = svi.head(10)

    chart = px.bar(
        overview_top10.sort_values(
            "predicted_sponsorship_eur_m"
        ),
        x="predicted_sponsorship_eur_m",
        y="club_name",
        orientation="h",
        color="league",
        labels={
            "predicted_sponsorship_eur_m":
                "Predicted sponsorship (€m)",
            "club_name":
                "Club",
        },
        hover_data=[
            "SVI_2025",
            "svi_rank",
        ],
    )

    chart.update_layout(
        height=480,
        yaxis_title=None,
    )

    st.plotly_chart(
        chart,
        use_container_width=True
    )

    st.caption(
        "Top 10 within the 96-club SVI scoring "
        "universe. Values are model estimates."
    )

with svi_tab:

    st.header("Sponsorship Value Index")

    st.caption(
        "SVI is a relative 0–100 index within the 2025 scoring universe; "
        "the predicted sponsorship value is shown separately in €m. "
        "An SVI of 100 does not represent a guaranteed contract value."
    )

    st.write(
        "Explore estimated sponsorship values "
        "and club positions in the SVI ranking."
    )

    selected_leagues = st.multiselect(
        "Select leagues",
        options=sorted(
            svi["league"].dropna().unique()
        ),
        default=sorted(
            svi["league"].dropna().unique()
        ),
        key="svi_leagues",
    )

    filtered_svi = svi[
        svi["league"].isin(selected_leagues)
    ].copy()

    st.metric(
        "Clubs in selected leagues",
        len(filtered_svi)
    )

    if filtered_svi.empty:

        st.warning(
            "Select at least one league."
        )

    else:

        ranking_display = filtered_svi[
            [
                "svi_rank",
                "club_name",
                "league",
                "predicted_sponsorship_eur_m",
                "SVI_2025",
            ]
        ].rename(
            columns={
                "svi_rank": "Overall rank",
                "club_name": "Club",
                "league": "League",
                "predicted_sponsorship_eur_m":
                    "Predicted sponsorship (€m)",
                "SVI_2025": "SVI",
            }
        )

        st.dataframe(
            ranking_display,
            use_container_width=True,
            hide_index=True,
        )

        st.subheader(
            "Predicted sponsorship by club"
        )

        chart = px.bar(
            filtered_svi.head(20).sort_values(
                "predicted_sponsorship_eur_m"
            ),
            x="predicted_sponsorship_eur_m",
            y="club_name",
            color="league",
            orientation="h",
            labels={
                "predicted_sponsorship_eur_m":
                    "Predicted sponsorship (€m)",
                "club_name": "Club",
            },
        )

        chart.update_layout(
            height=650,
            yaxis_title=None,
        )

        st.plotly_chart(
            chart,
            use_container_width=True
        )

        st.caption(
            "The displayed overall ranks refer "
            "to the original 96-club ranking; "
            "league filters do not recalculate them."
        )



with club_tab:

    st.header("Club Explorer")

    st.write(
        "Select a club to explore its predicted sponsorship value, "
        "Sponsorship Value Index and position relative to league peers."
    )

    st.info(
        "Club Explorer uses the SVI scoring universe only. "
        "ROI information is intentionally kept separate because "
        "the ROI dataset refers to a different club universe."
    )

    
    club_options = sorted(
        svi["club_name"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_club = st.selectbox(
        "Select club",
        options=club_options,
        index=0,
        key="club_explorer_selection",
    )

    club_row = (
        svi.loc[
            svi["club_name"] == selected_club
        ]
        .iloc[0]
    )

    club_league = club_row["league"]

    league_data = (
        svi.loc[
            svi["league"] == club_league
        ]
        .copy()
        .sort_values(
            "predicted_sponsorship_eur_m",
            ascending=False
        )
        .reset_index(drop=True)
    )

    
    league_data["league_rank_calculated"] = (
        league_data[
            "predicted_sponsorship_eur_m"
        ]
        .rank(
            method="min",
            ascending=False
        )
        .astype(int)
    )

    selected_league_row = (
        league_data.loc[
            league_data["club_name"] == selected_club
        ]
        .iloc[0]
    )

    league_rank = int(
        selected_league_row[
            "league_rank_calculated"
        ]
    )

    league_size = len(league_data)

    st.subheader(selected_club)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Overall SVI rank",
        f"#{int(club_row['svi_rank'])}"
    )

    col2.metric(
        "Predicted sponsorship",
        f"€{club_row['predicted_sponsorship_eur_m']:.2f}m"
    )

    col3.metric(
        "SVI",
        f"{club_row['SVI_2025']:.2f}"
    )

    col4.metric(
        f"{club_league} rank",
        f"#{league_rank} / {league_size}"
    )

    
    st.divider()

    st.subheader("League Benchmark")

    league_mean = (
        league_data[
            "predicted_sponsorship_eur_m"
        ]
        .mean()
    )

    league_median = (
        league_data[
            "predicted_sponsorship_eur_m"
        ]
        .median()
    )

    club_value = float(
        club_row[
            "predicted_sponsorship_eur_m"
        ]
    )

    difference_vs_mean = (
        club_value - league_mean
    )

    difference_vs_median = (
        club_value - league_median
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "League average",
        f"€{league_mean:.2f}m",
        delta=f"{difference_vs_mean:+.2f}m club vs league average",
        delta_color="off",
    )

    col2.metric(
        "League median",
        f"€{league_median:.2f}m",
        delta=f"{difference_vs_median:+.2f}m club vs league median",
        delta_color="off",
    )

    clubs_below = int(
        (
            league_data[
                "predicted_sponsorship_eur_m"
            ]
            < club_value
        ).sum()
    )

    league_percentile = (
        clubs_below
        / league_size
        * 100
    )

    col3.metric(
        "League percentile",
        f"{league_percentile:.1f}%"
    )

    st.caption(
        "League percentile indicates the percentage of league clubs "
        "with a lower predicted sponsorship value."
    )

    st.divider()

    st.subheader(
        f"{selected_club} vs {club_league}"
    )

    chart_data = league_data.copy()

    chart_data["Selection"] = chart_data[
        "club_name"
    ].apply(
        lambda x:
        "Selected club"
        if x == selected_club
        else "League peers"
    )

    league_chart = px.bar(
        chart_data.sort_values(
            "predicted_sponsorship_eur_m",
            ascending=True
        ),
        x="predicted_sponsorship_eur_m",
        y="club_name",
        orientation="h",
        color="Selection",
        labels={
            "predicted_sponsorship_eur_m":
                "Predicted sponsorship (€m)",
            "club_name":
                "Club",
            "Selection":
                "",
        },
        hover_data={
            "SVI_2025": ":.2f",
            "svi_rank": True,
            "league_rank_calculated": True,
        },
    )

    league_chart.update_layout(
        height=max(
            500,
            league_size * 30
        ),
        yaxis_title=None,
        legend_title_text="",
    )

    st.plotly_chart(
        league_chart,
        use_container_width=True
    )

    st.divider()

    st.subheader(
        "Closest Sponsorship Competitors"
    )

    competitor_data = league_data.copy()

    competitor_data[
        "difference_from_selected_eur_m"
    ] = (
        competitor_data[
            "predicted_sponsorship_eur_m"
        ]
        - club_value
    ).abs()

    competitors = (
        competitor_data.loc[
            competitor_data[
                "club_name"
            ] != selected_club
        ]
        .sort_values(
            "difference_from_selected_eur_m"
        )
        .head(5)
    )

    competitors_display = competitors[
        [
            "league_rank_calculated",
            "club_name",
            "predicted_sponsorship_eur_m",
            "SVI_2025",
            "svi_rank",
            "difference_from_selected_eur_m",
        ]
    ].rename(
        columns={
            "league_rank_calculated":
                "League rank",

            "club_name":
                "Club",

            "predicted_sponsorship_eur_m":
                "Predicted sponsorship (€m)",

            "SVI_2025":
                "SVI",

            "svi_rank":
                "Overall rank",

            "difference_from_selected_eur_m":
                "Absolute difference (€m)",
        }
    )

    st.dataframe(
        competitors_display,
        use_container_width=True,
        hide_index=True,
    )

    
    st.divider()

    st.subheader("Club Summary")

    st.write(
        f"**{selected_club}** is ranked "
        f"**#{int(club_row['svi_rank'])} overall** "
        f"in the 96-club SVI scoring universe and "
        f"**#{league_rank} in {club_league}**."
    )

    st.write(
        f"The model estimates a sponsorship value of "
        f"**€{club_value:.2f} million**, corresponding to "
        f"an SVI score of **{club_row['SVI_2025']:.2f}**."
    )

    if difference_vs_mean > 0:

        st.write(
            f"The predicted sponsorship value is "
            f"**€{abs(difference_vs_mean):.2f} million above** "
            f"the {club_league} average."
        )

    elif difference_vs_mean < 0:

        st.write(
            f"The predicted sponsorship value is "
            f"**€{abs(difference_vs_mean):.2f} million below** "
            f"the {club_league} average."
        )

    else:

        st.write(
            "The predicted sponsorship value is equal "
            "to the league average."
        )

    st.caption(
        "Predicted sponsorship values are model estimates. "
        "They should not be interpreted as observed sponsorship "
        "contract prices."
    )


with recommendation_tab:

    st.header("Sponsor–Club Recommendation")

    st.write(
        "Explore the club recommendations generated for each "
        "sponsor profile by the project's matching system."
    )

    st.info(
        "Recommendations reflect the project's 2025 sponsor "
        "and club data snapshots. Digital fit measures the "
        "compatibility calculated by the recommendation system; "
        "it does not represent a guaranteed commercial return."
    )

    
    required_recommendation_columns = [
        "sponsor_entity_key",
        "sponsor_name",
        "category",
        "club_name",
        "league",
        "final_recommendation_rank",
        "sponsor_club_digital_fit",
        "sponsor_club_platform_mix_fit",
        "predicted_sponsorship_eur_m",
        "SVI_2025",
        "svi_rank",
    ]

    missing_master = [
        col
        for col in required_recommendation_columns
        if col not in recommendations.columns
    ]

    missing_top3 = [
        col
        for col in required_recommendation_columns
        if col not in recommendations_top3.columns
    ]

    if missing_master or missing_top3:

        st.error(
            "The recommendation datasets are missing "
            "required columns."
        )

        st.write("Missing master columns:", missing_master)
        st.write("Missing Top 3 columns:", missing_top3)

    else:


        rec = recommendations.copy()
        rec_top3 = recommendations_top3.copy()

        numeric_columns = [
            "final_recommendation_rank",
            "sponsor_club_digital_fit",
            "sponsor_club_platform_mix_fit",
            "predicted_sponsorship_eur_m",
            "SVI_2025",
            "svi_rank",
        ]

        for df in [rec, rec_top3]:

            for col in numeric_columns:

                df[col] = pd.to_numeric(
                    df[col],
                    errors="coerce"
                )

        
        sponsor_options = sorted(
            rec["sponsor_entity_key"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_sponsor = st.selectbox(
            "Select sponsor profile",
            options=sponsor_options,
            key="sponsor_recommendation_selection",
        )

        sponsor_data = (
            rec.loc[
                rec["sponsor_entity_key"].astype(str)
                == selected_sponsor
            ]
            .copy()
            .sort_values(
                "final_recommendation_rank",
                ascending=True
            )
        )

        sponsor_top3 = (
            rec_top3.loc[
                rec_top3["sponsor_entity_key"].astype(str)
                == selected_sponsor
            ]
            .copy()
            .sort_values(
                "final_recommendation_rank",
                ascending=True
            )
        )

        if sponsor_data.empty:

            st.warning(
                "No recommendations found for this sponsor."
            )

        else:

            sponsor_info = sponsor_data.iloc[0]

            sponsor_name = str(
                sponsor_info["sponsor_name"]
            )

            sponsor_category = str(
                sponsor_info["category"]
            )

            
            st.subheader(sponsor_name)

            st.caption(
                f"Category: {sponsor_category} | "
                "Sponsor profile: 2025 snapshot"
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Sponsor profiles in dataset",
                len(sponsor_options)
            )

            col2.metric(
                "Clubs evaluated for this profile",
                sponsor_data["club_name"].nunique()
            )

            col3.metric(
                "Saved Top 3 recommendations",
                len(sponsor_top3)
            )

            
            expected_top3 = (
                sponsor_data.head(3)["club_name"]
                .astype(str)
                .tolist()
            )

            saved_top3 = (
                sponsor_top3["club_name"]
                .astype(str)
                .tolist()
            )

            if saved_top3 != expected_top3:

                st.warning(
                    "The saved Top 3 does not exactly match "
                    "the first three positions in the "
                    "recommendation master. The saved Top 3 "
                    "is displayed below without recalculating "
                    "its order."
                )

            
            st.divider()

            st.subheader("Top 3 Club Recommendations")

            st.write(
                "These are the recommendations saved by "
                "the project's existing matching system."
            )

            if sponsor_top3.empty:

                st.warning(
                    "The Top 3 file contains no records "
                    "for this sponsor profile."
                )

            else:

                top3_columns = st.columns(
                    min(3, len(sponsor_top3))
                )

                for position, (_, row) in enumerate(
                    sponsor_top3.head(3).iterrows()
                ):

                    with top3_columns[position]:

                        saved_rank = row[
                            "final_recommendation_rank"
                        ]

                        if pd.notna(saved_rank):

                            rank_label = (
                                f"#{int(saved_rank)}"
                            )

                        else:

                            rank_label = "N/A"

                        st.markdown(
                            f"### {rank_label} — {row['club_name']}"
                        )

                        st.caption(
                            str(row["league"])
                        )

                        digital_fit = row[
                            "sponsor_club_digital_fit"
                        ]

                        platform_fit = row[
                            "sponsor_club_platform_mix_fit"
                        ]

                        sponsorship_value = row[
                            "predicted_sponsorship_eur_m"
                        ]

                        st.metric(
                            "Digital fit",
                            (
                                f"{digital_fit:.2f}"
                                if pd.notna(digital_fit)
                                else "N/A"
                            )
                        )

                        st.metric(
                            "Platform mix fit",
                            (
                                f"{platform_fit:.2f}"
                                if pd.notna(platform_fit)
                                else "N/A"
                            )
                        )

                        st.metric(
                            "Predicted sponsorship",
                            (
                                f"€{sponsorship_value:.2f}m"
                                if pd.notna(sponsorship_value)
                                else "N/A"
                            )
                        )

                        if "recommendation_class" in row.index:

                            st.caption(
                                "Recommendation class: "
                                f"{row['recommendation_class']}"
                            )

            st.subheader("Evaluate a Recommended Club")

            st.write(
                "Choose a club from this sponsor profile's "
                "saved Top 10 recommendations and transfer "
                "it to the brand ROI scenario simulator."
            )

            roi_shortlist = sponsor_data.head(10).copy()

            roi_club_options = (
                roi_shortlist["club_name"]
                .astype(str)
                .tolist()
            )

            roi_rank_by_club = {
                str(row["club_name"]): (
                    f"#{int(row['final_recommendation_rank'])}"
                    if pd.notna(row["final_recommendation_rank"])
                    else "N/A"
                )
                for _, row in roi_shortlist.iterrows()
            }

            selected_recommended_club = st.selectbox(
                "Club to evaluate in the ROI simulator",
                options=roi_club_options,
                format_func=lambda club: (
                    f"{roi_rank_by_club.get(club, 'N/A')} — {club}"
                ),
                key=f"recommendation_roi_choice_{selected_sponsor}",
            )

            if st.button(
                "Use this club in the ROI simulator",
                key="send_recommendation_to_roi",
            ):

                roi_club_matches = (
                    roi.loc[
                        roi["club_name"]
                        .astype(str)
                        .str.strip()
                        .str.casefold()
                        ==
                        selected_recommended_club
                        .strip()
                        .casefold(),
                        "club_name",
                    ]
                    .dropna()
                    .unique()
                    .tolist()
                )

                if len(roi_club_matches) == 1:

                    st.session_state[
                        "brand_roi_simulator_club"
                    ] = roi_club_matches[0]

                    st.session_state[
                        "roi_scenario_sponsor_name"
                    ] = sponsor_name

                    st.session_state[
                        "roi_scenario_club_name"
                    ] = roi_club_matches[0]

                    st.success(
                        f"{sponsor_name} → "
                        f"{roi_club_matches[0]} selected. "
                        "Open the 'Social + TV ROI' tab "
                        "to continue with the simulator."
                    )

                elif len(roi_club_matches) == 0:

                    st.warning(
                        "This club was not found under the "
                        "same name in the 2024/25 ROI dataset. "
                        "No club has been transferred. "
                        "Select the corresponding club "
                        "manually in the ROI simulator."
                    )

                else:

                    st.warning(
                        "Multiple matching club records were "
                        "found in the ROI dataset. "
                        "No club has been transferred."
                    )

            st.caption(
                "The saved recommendation rank is preserved. "
                "Digital fit and platform mix fit are not "
                "used as estimates of the brand's share "
                "of media exposure."
            )
            
            st.divider()

            st.subheader(
                "Top 10 — Digital Fit Comparison"
            )
            top10 = sponsor_data.head(10).copy()
            top10["ranked_club_label"] = top10.apply(

    lambda row: (

        f"#{int(row['final_recommendation_rank'])} "
        f"— {row['club_name']}"

        if pd.notna(
            row["final_recommendation_rank"]
        )

        else f"N/A — {row['club_name']}"

    ),

    axis=1,

)


            top10_chart_data = top10.sort_values(

                "final_recommendation_rank",

                ascending=False,

            )

            top10_chart = px.bar(

                top10_chart_data,

                x="sponsor_club_digital_fit",

                y="ranked_club_label",

                orientation="h",

                color="league",

                text="sponsor_club_digital_fit",

                hover_data=[

                    "final_recommendation_rank",

                    "sponsor_club_platform_mix_fit",

                    "SVI_2025",

                ],

                labels={

                    "sponsor_club_digital_fit":
                        "Digital fit (0–100)",

                    "ranked_club_label":
                        "Club",

                    "league":
                        "League",

                    "final_recommendation_rank":
                        "Saved recommendation rank",

                    "sponsor_club_platform_mix_fit":
                        "Platform mix fit",

                    "SVI_2025":
                        "SVI",

                },

            )

            top10_chart.update_traces(

                texttemplate="%{text:.1f}",

                textposition="outside",

                cliponaxis=False,

            )

            top10_chart.update_layout(

                height=540,

                yaxis_title=None,

                xaxis_range=[0, 110],

                margin=dict(
                    l=15,
                    r=35,
                    t=20,
                    b=20,
                ),

            )



            st.plotly_chart(
                top10_chart,
                width="stretch",
            )


            st.caption(
               "Clubs are displayed in the original saved "
               "recommendation order. The number beside each "
               "club identifies its recommendation rank; "
               "bar length represents digital fit only. "
               "The recommendation rank is not calculated "
               "solely from digital fit."
            )


            st.divider()

            st.subheader(
                            "Full Recommendation Ranking"
                        )

            available_leagues = sorted(
                            sponsor_data["league"]
                            .dropna()
                            .unique()
                            .tolist()
                        )

            selected_leagues_rec = st.multiselect(
                            "Filter by league",
                            options=available_leagues,
                            default=available_leagues,
                            key="recommendation_league_filter",
                        )

            filtered_recommendations = (
                            sponsor_data.loc[
                                sponsor_data["league"].isin(
                                    selected_leagues_rec
                                )
                            ]
                            .copy()
                        )

            display_columns = [
                            "final_recommendation_rank",
                            "club_name",
                            "league",
                            "sponsor_club_digital_fit",
                            "sponsor_club_platform_mix_fit",
                            "predicted_sponsorship_eur_m",
                            "SVI_2025",
                            "svi_rank",
                        ]

            optional_columns = [
                            "recommendation_class",
                            "recommendation_evidence",
                            "roi_support",
                        ]

            display_columns += [
                            col
                            for col in optional_columns
                            if col in filtered_recommendations.columns
                        ]

            ranking_display = (
                            filtered_recommendations[
                                display_columns
                            ]
                            .sort_values(
                                "final_recommendation_rank",
                                ascending=True
                            )
                            .rename(
                                columns={
                                    "final_recommendation_rank":
                                        "Recommendation rank",

                                    "club_name":
                                        "Club",

                                    "league":
                                        "League",

                                    "sponsor_club_digital_fit":
                                        "Digital fit",

                                    "sponsor_club_platform_mix_fit":
                                        "Platform mix fit",

                                    "predicted_sponsorship_eur_m":
                                        "Predicted sponsorship (€m)",

                                    "SVI_2025":
                                        "SVI",

                                    "svi_rank":
                                        "Overall SVI rank",

                                    "recommendation_class":
                                        "Recommendation class",

                                    "recommendation_evidence":
                                        "Recommendation evidence",

                                    "roi_support":
                                        "ROI data support",
                                }
                            )
                        )

            st.dataframe(
                            ranking_display,
                            width="stretch",
                            hide_index=True,
                        )

            st.caption(
                            "Recommendation ranks are the original "
                            "ranks saved in the project dataset. "
                            "Filtering by league does not recalculate them."
                        )


            st.download_button(
                            label="Download selected sponsor recommendations (CSV)",
                            data=ranking_display.to_csv(
                                index=False
                            ).encode("utf-8-sig"),
                            file_name="sponsor_club_recommendations.csv",
                            mime="text/csv",
                            key="download_sponsor_recommendations",
                        )

            st.divider()

            st.subheader("How to Interpret the Results")

            st.write(
                            "**Digital fit** and **platform mix fit** "
                            "describe different aspects of the calculated "
                            "compatibility between the sponsor's social "
                            "presence and the club's social profile."
                        )

            st.write(
                            "**Recommendation rank** is the original "
                            "ordering generated by the project's "
                            "recommendation system. It must not be "
                            "interpreted as a ranking based solely "
                            "on digital fit."
                        )

            st.write(
                            "**Predicted sponsorship** is an estimate "
                            "produced by the predictive model, "
                            "not a verified commercial offer."
                        )

            st.caption(
                            "ROI-related fields in the recommendation "
                            "dataset may be unavailable for some clubs "
                            "and use proxy-based information. "
                            "Their presence does not establish "
                            "an actual financial return for a "
                            "specific sponsor–club agreement."
                        )


with roi_tab:

    st.header("Brand Sponsor — Social + TV ROI Analysis")
    
    st.caption(
        "Perspective: brand sponsor | "
        "Club-level benchmark and hypothetical "
        "brand-specific investment scenarios"
    )

    st.write(
        "Explore estimated media value, predicted sponsorship "
        "and the ROI proxy indicators available for the "
        "2024/25 Big Five competition universe."
    )

    st.warning(
        "The indicators shown here are media-value proxies, "
        "not realized financial returns. The ROI dataset "
        "refers to the 2024/25 competition universe, while "
        "some sponsorship estimates originate from a "
        "different scoring reference period."
    )

    st.divider()

    st.subheader("Brand Sponsor — ROI Scenario Simulator")

    st.write(
        "Simulate the potential media-value return of a sponsorship "
        "agreement from the perspective of an individual brand."
    )

    st.info(
        "This is a hypothetical scenario, not an estimate of an "
        "existing sponsorship contract. The club-level media value "
        "comes from the 2024/25 ROI dataset; the sponsorship fee "
        "and the brand's share of exposure are assumptions entered "
        "by the user."
    )

    
    simulator_clubs = sorted(
        roi["club_name"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    simulated_club_name = st.selectbox(
        "Select the club",
        options=simulator_clubs,
        key="brand_roi_simulator_club",
    )


    context_sponsor = st.session_state.get(
        "roi_scenario_sponsor_name"
    )

    context_club = st.session_state.get(
        "roi_scenario_club_name"
    )

    if (
        context_sponsor
        and context_club == simulated_club_name
    ):

        st.success(
            f"Recommendation selected: "
            f"{context_sponsor} → {simulated_club_name}"
        )

        st.caption(
            "The selected club comes from the sponsor–club "
            "recommendation system. The hypothetical fee "
            "and the brand-attributable exposure share "
            "must still be entered separately. "
            "Recommendation and ROI datasets may refer "
            "to different reference periods."
        )
    simulated_club = (
        roi.loc[
            roi["club_name"].astype(str) == simulated_club_name
        ]
        .iloc[0]
    )

    
    social_value = pd.to_numeric(
        simulated_club["social_media_value_eur_m"],
        errors="coerce",
    )

    tv_value = pd.to_numeric(
        simulated_club["tv_media_value_eur_m"],
        errors="coerce",
    )

    if pd.isna(social_value) or pd.isna(tv_value):

        st.warning(
            "Social or TV media-value data are unavailable "
            "for the selected club."
        )

    else:

        total_club_media_value = (
            float(social_value) + float(tv_value)
        )

       
        input_col1, input_col2 = st.columns(2)

        with input_col1:

            sponsor_fee_eur_m = st.number_input(
                "Hypothetical sponsorship fee (€m)",
                min_value=0.01,
                value=1.00,
                step=0.25,
                format="%.2f",
                key="brand_roi_simulator_fee",
            )

        with input_col2:

            brand_exposure_share_pct = st.slider(
                "Hypothetical share of club media value "
                "attributable to the brand (%)",
                min_value=0,
                max_value=100,
                value=5,
                step=1,
                key="brand_roi_simulator_share",
            )

        st.caption(
            "The initial fee (€1m) and exposure share (5%) "
            "are illustrative starting values, not observed "
            "contract terms. Adjust both inputs to explore "
            "your own scenario."
        )

        st.info(
            "**Reference period:** The club media-value inputs refer to "
            "the project's 2024/25 competition dataset, with social "
            "fanbase inputs drawn from a 2025 snapshot. For a "
            "same-period scenario, enter a hypothetical sponsorship "
            "fee for one comparable season and an exposure share "
            "referring to that same season. If you know only a "
            "multi-year contract fee, do not compare its full value "
            "with a single season of media value. This scenario "
            "does **not** forecast next season's ROI or a "
            "realized financial return."
        )

        
        brand_media_value_eur_m = (
            total_club_media_value
            * brand_exposure_share_pct
            / 100
        )

       
        brand_roi_proxy_pct = (
            (
                brand_media_value_eur_m
                - sponsor_fee_eur_m
            )
            / sponsor_fee_eur_m
        ) * 100

        media_cost_coverage_pct = (
            brand_media_value_eur_m
            / sponsor_fee_eur_m
        ) * 100

       
        st.divider()

        st.subheader(
            f"Scenario Results — {simulated_club_name}"
        )

        st.markdown("#### Estimated media value")

        result_col1, result_col2 = st.columns(2)

        with result_col1:
            st.metric(
                "Club Social + TV media value",
                f"€{total_club_media_value:.2f}m",
            )

        with result_col2:
            st.metric(
                "Media value attributed to brand",
                f"€{brand_media_value_eur_m:.2f}m",
            )

        st.markdown("#### Sponsorship investment and return")

        result_col3, result_col4 = st.columns(2)

        with result_col3:
            st.metric(
                "Hypothetical sponsorship fee",
                f"€{sponsor_fee_eur_m:.2f}m",
            )

        with result_col4:
            st.metric(
                "Brand media-value ROI proxy",
                f"{brand_roi_proxy_pct:.2f}%",
            )

        st.metric(
            "Media-value coverage of hypothetical fee",
            f"{media_cost_coverage_pct:.2f}%",
        )

        
        st.divider()
        st.subheader("Brand ROI — Sensitivity Analysis")
        st.write(
            "How the brand's hypothetical media-value ROI varies "
            "with its assumed share of club media value. "
            "The club and hypothetical same-season fee remain fixed."
        )

        sensitivity_shares = sorted(set([
            0, 1, 5, 10, 25, 50, 100, brand_exposure_share_pct
        ]))
        sensitivity_rows = []
        for share_pct in sensitivity_shares:
            attributed_value = total_club_media_value * share_pct / 100
            scenario_roi_pct = (
                (attributed_value - sponsor_fee_eur_m)
                / sponsor_fee_eur_m * 100
            )
            sensitivity_rows.append({
                "Scenario": (
                    "Current selection"
                    if share_pct == brand_exposure_share_pct
                    else "Alternative"
                ),
                "Exposure share (%)": share_pct,
                "Brand media value (€m)": round(attributed_value, 4),
                "Hypothetical fee (€m)": round(sponsor_fee_eur_m, 4),
                "Brand ROI proxy (%)": round(scenario_roi_pct, 2),
            })

        sensitivity_df = pd.DataFrame(sensitivity_rows)
        st.dataframe(sensitivity_df, width="stretch", hide_index=True)
        st.caption(
            "Illustrative scenarios only. The fee and club-level "
            "media value remain fixed; only the assumed share "
            "attributable to the brand changes. The ROI is a "
            "media-value proxy, not a future or realized return."
        )

        st.divider()

        st.subheader("Media-Value Break-Even")

        if total_club_media_value > 0:

            required_share_pct = (
                sponsor_fee_eur_m
                / total_club_media_value
            ) * 100

            if required_share_pct <= 100:

                st.write(
                    "Under the current assumptions, the brand "
                    "would need to receive approximately "
                    f"**{required_share_pct:.2f}%** of the "
                    "club's estimated Social + TV media value "
                    "for that media value to equal the "
                    "hypothetical sponsorship fee."
                )

            else:

                st.write(
                    "Under the current assumptions, even "
                    "attributing **100% of the club's estimated "
                    "Social + TV media value** to the brand "
                    "would not cover the hypothetical "
                    "sponsorship fee."
                )

    
        with st.expander(
            "How is the brand ROI scenario calculated?"
        ):

            st.latex(
                r"V_{\mathrm{brand}} = "
                r"(V_{\mathrm{Social}} + V_{\mathrm{TV}})"
                r"\times \frac{q}{100}"
            )

            st.latex(
                r"ROI_{\mathrm{brand}}^{\mathrm{proxy}} = "
                r"\frac{V_{\mathrm{brand}}-C_{\mathrm{sponsor}}}"
                r"{C_{\mathrm{sponsor}}}\times100"
            )

            st.write(
                "Here, q is the hypothetical percentage of "
                "club-level media value attributed to the brand, "
                "and C is the hypothetical fee paid by that brand."
            )

            st.write(
                "The model does not estimate brand-specific "
                "exposure shares or actual contract prices. "
                "The scenario therefore depends on the "
                "assumptions selected by the user."
            )

            st.write(
                "Media-equivalent value is not incremental "
                "revenue or profit. This proxy excludes other "
                "potential sponsorship benefits, such as sales "
                "effects, hospitality, licensing and brand "
                "activation."
            )

    st.divider()

    st.subheader("Club-Level Media-Value Benchmark")

    st.write(
        "The following tables and charts compare **aggregate club-level "
        "Social + TV media value** with a model-predicted sponsorship "
        "reference. This is a benchmark for exploring clubs; it is "
        "**not a brand-specific contract ROI**."
    )

    st.caption(
        "The benchmark can use different TV audience methodologies "
        "across leagues. A negative ROI proxy means that the measured "
        "media-equivalent value is below the hypothetical reference "
        "amount; it does not demonstrate a realized financial loss."
    )

    st.subheader("ROI Data Availability")

    ROI_METRICS = {

        "total_roi_proxy_pct":
            "Total ROI proxy (%) — original field",

        "total_roi_proxy_base_pct":
            "Total ROI proxy (%) — base scenario",

        "total_roi_pct":
            "Social + TV media-value ROI proxy (%) — all 96 clubs",

        "social_roi_proxy_pct":
            "Social ROI proxy (%) — social only",

        "social_roi_pct":
            "Social ROI (%) — alternative social field",

    }

    roi_working = roi.copy()

    available_metric_columns = [
        col
        for col in ROI_METRICS
        if col in roi_working.columns
    ]

    for col in available_metric_columns:

        roi_working[col] = pd.to_numeric(
            roi_working[col],
            errors="coerce"
        )

    
    coverage_records = []

    for col in available_metric_columns:

        available_count = int(
            roi_working[col].notna().sum()
        )

        total_clubs = len(roi_working)

        coverage_records.append({

            "ROI field": col,

            "Indicator": ROI_METRICS[col],

            "Clubs with data": available_count,

            "Clubs without data":
                total_clubs - available_count,

            "Coverage (%)": (
                round(
                    100 * available_count / total_clubs,
                    1
                )
                if total_clubs > 0
                else 0.0
            ),

        })

    coverage_audit = pd.DataFrame(
        coverage_records
    )

    if coverage_audit.empty:

        st.error(
            "No recognized ROI percentage fields were "
            "found in the dataset."
        )

    else:

        st.dataframe(
            coverage_audit,
            width="stretch",
            hide_index=True,
        )

        st.caption(
            "Coverage is calculated separately for each "
            "original CSV field. Different ROI definitions "
            "are not automatically combined."
        )

    total_roi_candidates = [

        col
        for col in [
            "total_roi_proxy_pct",
            "total_roi_proxy_base_pct",
            "total_roi_pct",
        ]

        if (
            col in roi_working.columns
            and roi_working[col].notna().any()
        )

    ]

    if not total_roi_candidates:

        st.warning(
            "No available total ROI percentage field "
            "was found in the master dataset."
        )

        selected_roi_col = None

    else:


        default_roi_col = (
           "total_roi_pct"
           if "total_roi_pct" in total_roi_candidates
           else max(
                total_roi_candidates,
                key=lambda col: roi_working[col].notna().sum()
           )
         )

        selected_roi_col = st.selectbox(

            "Select ROI indicator",

            options=total_roi_candidates,

            index=total_roi_candidates.index(
                default_roi_col
            ),

            format_func=lambda col:
                ROI_METRICS[col],

            key="roi_metric_selector",

        )

        st.info(
            f"Currently displaying the original CSV field: "
            f"`{selected_roi_col}`. "
            "Missing values remain missing; no estimates "
            "are generated to fill them."
        )



    st.divider()

    st.subheader("Club Coverage")

    roi_leagues = sorted(
        roi_working["league_final"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_roi_leagues = st.multiselect(

        "Select leagues",

        options=roi_leagues,

        default=roi_leagues,

        key="roi_leagues_revised",

    )

    filtered_roi = roi_working.loc[

        roi_working["league_final"].isin(
            selected_roi_leagues
        )

    ].copy()

   

    n_clubs = len(filtered_roi)

    n_sponsorship = int(

        filtered_roi[
            "predicted_sponsorship_eur_m"
        ].notna().sum()

    )

    if selected_roi_col is not None:

        n_roi = int(

            filtered_roi[
                selected_roi_col
            ].notna().sum()

        )

    else:

        n_roi = 0

    roi_coverage = (

        100 * n_roi / n_clubs

        if n_clubs > 0

        else 0

    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Clubs in selected leagues",
        n_clubs
    )

    col2.metric(
        "Sponsorship estimates available",
        n_sponsorship
    )

    col3.metric(
        "Selected ROI values available",
        n_roi
    )

    col4.metric(
        "Selected ROI coverage",
        f"{roi_coverage:.1f}%"
    )

    if filtered_roi.empty:

        st.info(
            "Select at least one league to display results."
        )

    else:

        

        st.subheader("ROI Coverage by League")

        league_coverage = (

            filtered_roi
            .groupby("league_final")
            .agg(

                clubs=(
                    "club_name",
                    "size"
                ),

                sponsorship_available=(
                    "predicted_sponsorship_eur_m",
                    "count"
                ),

            )
            .reset_index()

        )

        if selected_roi_col is not None:

            roi_counts = (

                filtered_roi
                .groupby("league_final")[
                    selected_roi_col
                ]
                .count()

            )

            league_coverage[
                "roi_available"
            ] = (

                league_coverage[
                    "league_final"
                ]
                .map(roi_counts)
                .astype(int)

            )

            league_coverage[
                "roi_coverage_pct"
            ] = (

                100

                * league_coverage[
                    "roi_available"
                ]

                / league_coverage[
                    "clubs"
                ]

            ).round(1)

        st.dataframe(

            league_coverage.rename(
                columns={

                    "league_final":
                        "League",

                    "clubs":
                        "Clubs",

                    "sponsorship_available":
                        "Sponsorship estimates",

                    "roi_available":
                        "Available ROI values",

                    "roi_coverage_pct":
                        "ROI coverage (%)",

                }
            ),

            width="stretch",

            hide_index=True,

        )


        st.divider()
        
        st.subheader("TV Audience — Data Methodology")

        tv_method_counts = (
            filtered_roi["tv_methodology"]
            .fillna("Methodology not specified")
            .value_counts()
            .rename_axis("TV methodology")
            .reset_index(name="Clubs")
        )

        st.dataframe(
            tv_method_counts,
            width="stretch",
            hide_index=True,
        )

        observed_tv_count = int(
            filtered_roi["tv_audience_fully_observed"]
            .astype(str)
            .str.strip()
            .str.lower()
            .eq("true")
            .sum()
        )

        st.caption(
            f"Fully observed TV audience: "
            f"{observed_tv_count}/{len(filtered_roi)} clubs "
            "in the selected leagues. Other TV audience "
            "values use proxy-based methodologies. "
            "The ROI indicator combines these different "
            "data sources and should not be interpreted "
            "as a realized financial return."
        )

        st.divider()

        st.subheader("Club-Level Results")

        display_columns = [

            "club_name",

            "league_final",

            "predicted_sponsorship_eur_m",

        ]

        if (
            "total_media_value_eur_m"
            in filtered_roi.columns
        ):

            display_columns.append(
                "total_media_value_eur_m"
            )

        if selected_roi_col is not None:

            display_columns.append(
                selected_roi_col
            )

        column_names = {

            "club_name":
                "Club",

            "league_final":
                "League",

            "predicted_sponsorship_eur_m":
                "Predicted sponsorship (€m)",

            "total_media_value_eur_m":
                "Estimated Social + TV value (€m)",

        }

        if selected_roi_col is not None:

            column_names[
                selected_roi_col
            ] = ROI_METRICS[selected_roi_col]

        roi_display = (

            filtered_roi[
                display_columns
            ]
            .rename(
                columns=column_names
            )

        )

        st.dataframe(
            roi_display,
            width="stretch",
            hide_index=True,
        )

        st.download_button(

            label="Download displayed ROI results (CSV)",

            data=roi_display.to_csv(
                index=False
            ).encode("utf-8-sig"),

            file_name="roi_dashboard_results.csv",

            mime="text/csv",

        )

        
        if selected_roi_col is not None:

            missing_roi_clubs = (

                filtered_roi.loc[

                    filtered_roi[
                        selected_roi_col
                    ].isna(),

                    [
                        "club_name",
                        "league_final",
                    ]

                ]

            )

            with st.expander(

                "Clubs without a value in the "
                f"selected ROI field ({len(missing_roi_clubs)})"

            ):

                if missing_roi_clubs.empty:

                    st.success(
                        "No missing values in this field "
                        "for the selected leagues."
                    )

                else:

                    st.dataframe(

                        missing_roi_clubs.rename(
                            columns={

                                "club_name": "Club",

                                "league_final": "League",

                            }
                        ),

                        width="stretch",

                        hide_index=True,

                    )


        if selected_roi_col is not None:

            chart_data = (

                filtered_roi
                .dropna(
                    subset=[selected_roi_col]
                )
                .sort_values(

                    selected_roi_col,

                    ascending=False

                )
                .head(20)
                .copy()

            )

            if not chart_data.empty:

                st.divider()

                st.subheader(
                    "ROI Comparison — Available Clubs"
                )

                roi_chart = px.bar(

                    chart_data.sort_values(
                        selected_roi_col
                    ),

                    x=selected_roi_col,

                    y="club_name",

                    orientation="h",

                    color="league_final",

                    labels={

                        selected_roi_col:
                            ROI_METRICS[selected_roi_col],

                        "club_name":
                            "Club",

                        "league_final":
                            "League",

                    },

                )

                roi_chart.update_layout(

                    height=max(
                        450,
                        len(chart_data) * 30
                    ),

                    yaxis_title=None,

                )

                st.plotly_chart(
                    roi_chart,
                    width="stretch",
                )

                st.caption(
                    "Only clubs with an available value "
                    "in the selected ROI field are plotted. "
                    "Missing values are excluded rather "
                    "than treated as zero."
                )

        
        if (
            "total_media_value_eur_m"
            in filtered_roi.columns
        ):

            scatter_data = (

                filtered_roi
                .dropna(

                    subset=[

                        "predicted_sponsorship_eur_m",

                        "total_media_value_eur_m",

                    ]

                )

            )

            if not scatter_data.empty:

                st.divider()

                st.subheader(
                    "Media Value vs Predicted Sponsorship"
                )

                media_chart = px.scatter(

                    scatter_data,

                    x="predicted_sponsorship_eur_m",

                    y="total_media_value_eur_m",

                    color="league_final",

                    hover_name="club_name",

                    labels={

                        "predicted_sponsorship_eur_m":
                            "Predicted sponsorship (€m)",

                        "total_media_value_eur_m":
                            "Estimated Social + TV value (€m)",

                        "league_final":
                            "League",

                    },

                )

                media_chart.update_layout(
                    height=500
                )

                st.plotly_chart(
                    media_chart,
                    width="stretch",
                )

                st.caption(
                    "The chart includes only records with "
                    "both variables available. Media value "
                    "may incorporate modeled audiences "
                    "and advertising-equivalent assumptions."
                )

  
    st.divider()

    with st.expander(
        "ROI Methodology and Interpretation"
    ):

        st.write(
            "The dataset contains multiple ROI-related "
            "fields, including total ROI, base-scenario "
            "ROI and social-only ROI. These are displayed "
            "as separate indicators and are not merged "
            "without a dedicated methodology audit."
        )

        st.write(
            "An advertising-equivalent media value is not "
            "the same as incremental revenue or profit. "
            "The predicted sponsorship value is also not "
            "necessarily the price of an actual contract."
        )

        st.write(
            "The 2024/25 competition universe and the "
            "reference period of the model's sponsorship "
            "estimates must be distinguished when "
            "interpreting the results."
        )
with map_tab:

    st.header(
        "Geographic Distribution of the Sponsorship Value Index"
    )

    st.write(
        "Explore the geographical distribution of the 96 clubs "
        "included in the SVI scoring universe."
    )

    st.info(
        "Point color identifies the domestic league, while point "
        "size represents the club's SVI quartile."
    )

    if MAP_PATH.exists():

        import streamlit.components.v1 as components

        map_html = MAP_PATH.read_text(
            encoding="utf-8"
        )

        components.html(
            map_html,
            height=720,
            scrolling=False,
        )

    else:

        st.warning(
            "Geographic map file not available."
        )
with quality_tab:

    st.header("Model & Data Quality")

    st.subheader(
        "Temporal predictive validation — 2023/24"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "High-quality test observations",
        "16"
    )

    col2.metric(
        "MAE",
        "€35.47m"
    )

    col3.metric(
        "RMSE",
        "€45.48m"
    )

    col4.metric(
        "R²",
        "0.747"
    )

    st.caption(
        "XGBoost Model B Original. "
        "Validation statistics refer to the "
        "16 high-quality observations in the "
        "2023/24 temporal test, not all 96 "
        "clubs in the scoring universe."
    )

    st.divider()

    st.subheader(
        "Coverage and scoring readiness"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "SVI scoring coverage",
        "96 / 96"
    )

    col2.metric(
        "ROI club coverage",
        "96 / 96"
    )

    col3.metric(
        "Model feature completeness",
        "100%"
    )

    st.caption(
        "Feature completeness refers to the "
        "40 numeric model inputs after data "
        "preparation. It does not establish "
        "100% completeness of raw source data."
    )
   
    
    st.divider()

    st.subheader(
        "Ranking stability — exploratory"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Spearman correlation",
        "0.8839"
    )

    col2.metric(
        "Mean absolute rank change",
        "3.07 positions"
    )

    col3.metric(
        "Top 10 retention",
        "70%"
    )

    st.info(
        "These exploratory results compare "
        "the 30 clubs common to the historical "
        "2023/24 Model B ranking and the "
        "subsequent 2025 SVI output. "
        "They are not yet a certified "
        "consecutive-season stability KPI "
        "for the complete Big Five universe."
    )

st.divider()

st.caption(
    "SBL Consultancy | Sponsorship Value Index Predictor | "
    "Model estimates and proxy-based analyses"
)
