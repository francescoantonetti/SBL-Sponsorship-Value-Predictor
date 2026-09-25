from pathlib import Path
import base64
from html import escape
import re
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
ASSETS_DIR = Path(__file__).resolve().parent / 'assets'
LOGO_PATH = ASSETS_DIR / 'logo_sbl.png'
MAP_PATH = ASSETS_DIR / 'SVI_geographic_map_2025.html'
SBL_WEBSITE = 'https://sblconsultancy.it/'
SBL_NAVY = '#1E344B'
SBL_NAVY_DARK = '#172B40'
SBL_SLATE = '#345A78'
SBL_ORANGE = '#F7931E'
SBL_SKY = '#32A7DA'
SBL_ICE = '#ECF5FA'
SBL_PAPER = '#F7FAFD'
SBL_BORDER = '#DDE6EE'
DASHBOARD_COLORS = [SBL_NAVY, SBL_ORANGE, SBL_SKY, SBL_SLATE, '#759CB9', '#E2B166']
px.defaults.color_discrete_sequence = DASHBOARD_COLORS
px.defaults.template = 'plotly_white'
if LOGO_PATH.is_file():
    from PIL import Image
    with Image.open(LOGO_PATH) as logo_image:
        PAGE_ICON = logo_image.copy()
else:
    PAGE_ICON = '⚽'
st.set_page_config(page_title='SBL Consultancy | SVI Predictor', page_icon=PAGE_ICON, layout='wide')
st.markdown(tr('\n    <style>\n    :root {\n        --sbl-navy: #1E344B;\n        --sbl-deep: #172B40;\n        --sbl-orange: #F7931E;\n        --sbl-sky: #32A7DA;\n        --sbl-paper: #F4F7FB;\n        --sbl-ink: #21364C;\n        --sbl-muted: #465A70;\n        --sbl-line: #DCE5EF;\n    }\n\n    /* Identita\' visiva: canvas chiaro anche nel browser del responsabile. */\n    html, body, [data-testid="stAppViewContainer"],\n    [data-testid="stMain"], .main, .stApp {\n        background: var(--sbl-paper) !important;\n        color: var(--sbl-ink) !important;\n    }\n    header[data-testid="stHeader"] {\n        background: var(--sbl-paper) !important;\n        box-shadow: none !important;\n    }\n    [data-testid="stMainBlockContainer"], .main .block-container {\n        padding-top: 4.2rem !important;\n        padding-bottom: 2.6rem !important;\n        max-width: 1650px;\n    }\n    @media (max-width: 768px) {\n        [data-testid="stMainBlockContainer"], .main .block-container {\n            padding-top: 4rem !important;\n            padding-left: 1rem !important;\n            padding-right: 1rem !important;\n        }\n    }\n    [data-testid="stMain"] h1,\n    [data-testid="stMain"] h2,\n    [data-testid="stMain"] h3,\n    [data-testid="stMain"] h4 {\n        color: var(--sbl-navy) !important;\n        letter-spacing: -0.025em;\n    }\n    [data-testid="stMain"] p,\n    [data-testid="stMain"] label {\n        color: var(--sbl-ink);\n    }\n\n    /* Hero compatto: logo interamente visibile e cliccabile. */\n    .sbl-hero {\n        display: flex; align-items: center; gap: 1.15rem;\n        background: #fff;\n        border: 1px solid var(--sbl-line);\n        border-radius: 16px;\n        padding: 1.15rem 1.45rem;\n        box-shadow: 0 7px 24px rgba(30, 52, 75, .07);\n        margin: .25rem 0 1.1rem;\n        min-height: 115px;\n    }\n    .sbl-logo-link { flex-shrink: 0; display: inline-flex; align-items: center; justify-content: center; }\n    .sbl-logo-link img {\n        width: 78px; height: 78px; max-width: 100%;\n        object-fit: contain; display: block; border-radius: 12px;\n    }\n    .sbl-logo-link:focus-visible { outline: 3px solid var(--sbl-orange); border-radius: 12px; }\n    .sbl-hero-copy { min-width: 0; }\n    .sbl-eyebrow {\n        color: #426480 !important; font-size: .71rem;\n        letter-spacing: .16em; font-weight: 800;\n        text-transform: uppercase; margin-bottom: .3rem;\n    }\n    .sbl-hero h1 {\n        color: var(--sbl-navy) !important;\n        font-size: clamp(1.45rem, 2.2vw, 2.28rem);\n        font-weight: 780; line-height: 1.2;\n        margin: 0 0 .42rem !important;\n        overflow-wrap: anywhere;\n    }\n    .sbl-hero p {\n        color: var(--sbl-muted) !important;\n        font-size: .92rem; line-height: 1.5; margin: 0 !important;\n    }\n    @media (max-width: 560px) {\n        .sbl-hero { gap: .75rem; padding: .85rem; min-height: auto; }\n        .sbl-logo-link img { width: 55px; height: 55px; }\n        .sbl-hero h1 { font-size: 1.32rem; }\n        .sbl-hero p { font-size: .80rem; }\n    }\n\n    /* Sidebar coordinata: logo cliccabile ma non tagliato. */\n    section[data-testid="stSidebar"] {\n        background: linear-gradient(170deg, var(--sbl-navy), var(--sbl-deep)) !important;\n        border-right: 3px solid var(--sbl-orange);\n    }\n    section[data-testid="stSidebar"] > div { background: transparent !important; }\n    section[data-testid="stSidebar"] p,\n    section[data-testid="stSidebar"] span,\n    section[data-testid="stSidebar"] label,\n    section[data-testid="stSidebar"] h1,\n    section[data-testid="stSidebar"] h2,\n    section[data-testid="stSidebar"] h3 { color: #F7FAFE !important; }\n    section[data-testid="stSidebar"] hr { border-color: rgba(255, 255, 255, .24); }\n    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,\n    section[data-testid="stSidebar"] small { color: #D7E3EF !important; }\n    .sbl-sidebar-brand { padding: .2rem 0 .4rem; }\n    .sbl-sidebar-brand .sbl-logo-link img { width: 154px; height: 150px; }\n    .sbl-sidebar-brand .sbl-logo-link:hover img { filter: drop-shadow(0 4px 7px rgba(255,255,255,.14)); }\n\n    /* KPI: il label dei metric era bianco su fondo bianco nel browser del responsabile.\n       Fissiamo esplicitamente anche il colore degli elementi annidati. */\n    div[data-testid="stMetric"] {\n        box-sizing: border-box;\n        background: #fff !important;\n        border: 1px solid var(--sbl-line) !important;\n        border-top: 3px solid var(--sbl-orange) !important;\n        border-radius: 14px !important;\n        min-height: 137px;\n        padding: 17px 18px !important;\n        box-shadow: 0 5px 16px rgba(30,52,75,.065);\n        overflow: visible !important;\n    }\n    div[data-testid="stMetricLabel"],\n    div[data-testid="stMetricLabel"] *,\n    div[data-testid="stMetric"] [data-testid="stMetricLabel"] p {\n        color: #42546A !important;\n        -webkit-text-fill-color: #42546A !important;\n        opacity: 1 !important;\n        visibility: visible !important;\n        font-size: .88rem !important;\n        font-weight: 700 !important;\n        line-height: 1.35 !important;\n        white-space: normal !important;\n        overflow: visible !important;\n    }\n    div[data-testid="stMetricLabel"] {\n        min-height: 2.25rem;\n        margin-bottom: .48rem;\n    }\n    div[data-testid="stMetricValue"],\n    div[data-testid="stMetricValue"] * {\n        color: var(--sbl-navy) !important;\n        -webkit-text-fill-color: var(--sbl-navy) !important;\n        opacity: 1 !important;\n        font-weight: 750 !important;\n    }\n    div[data-testid="stMetricValue"] { font-size: clamp(1.35rem, 1.7vw, 2rem); }\n    div[data-testid="stMetricDelta"], div[data-testid="stMetricDelta"] * {\n        opacity: 1 !important;\n    }\n\n    /* Tabs leggibili e navigazione attiva nel colore aziendale. */\n    div[data-testid="stTabs"] [role="tablist"] {\n        gap: .25rem;\n        border-bottom: 1px solid var(--sbl-line);\n    }\n    div[data-testid="stTabs"] [role="tab"] {\n        color: #38526C !important;\n        font-weight: 650 !important;\n        border-radius: 8px 8px 0 0;\n        padding: .65rem .9rem;\n    }\n    div[data-testid="stTabs"] [role="tab"]:hover {\n        background: #E7F1F8 !important;\n        color: var(--sbl-navy) !important;\n    }\n    div[data-testid="stTabs"] [role="tab"][aria-selected="true"] {\n        color: var(--sbl-navy) !important;\n        background: #EAF2F8 !important;\n        border-bottom-color: var(--sbl-orange) !important;\n        box-shadow: inset 0 -2px var(--sbl-orange);\n    }\n    div[data-testid="stTabs"] [role="tab"]:focus-visible { outline: 2px solid var(--sbl-orange); }\n\n    /* Input e menu: niente dropdown nero su pagina chiara. */\n    [data-testid="stMain"] div[data-baseweb="select"] > div,\n    [data-testid="stMain"] div[data-baseweb="input"] > div,\n    [data-testid="stMain"] div[data-baseweb="base-input"],\n    [data-testid="stMain"] div[data-baseweb="select"] input,\n    [data-testid="stMain"] input[type="number"] {\n        background: #fff !important;\n        color: var(--sbl-ink) !important;\n        border-color: var(--sbl-line) !important;\n    }\n    [data-baseweb="popover"], [data-baseweb="popover"] > div,\n    ul[role="listbox"], div[role="listbox"], [data-baseweb="menu"] {\n        background: #fff !important;\n        color: var(--sbl-ink) !important;\n        border-color: var(--sbl-line) !important;\n    }\n    li[role="option"], li[role="option"] *,\n    [role="option"], [role="option"] * {\n        color: var(--sbl-ink) !important;\n    }\n    [role="option"]:hover, [role="option"][aria-selected="true"] {\n        background: #E8F3FC !important;\n    }\n    [data-testid="stMain"] button[kind="primary"] {\n        background: var(--sbl-navy) !important;\n        color: #fff !important;\n        border-color: var(--sbl-navy) !important;\n    }\n    [data-testid="stMain"] button:hover { border-color: var(--sbl-orange) !important; }\n    [data-testid="stDataFrame"], [data-testid="stAlert"],\n    [data-testid="stPlotlyChart"] { border-radius: 12px; }\n    [data-testid="stDataFrame"], [data-testid="stPlotlyChart"] {\n        border: 1px solid var(--sbl-line);\n        background: #fff;\n    }\n    </style>\n    '), unsafe_allow_html=True)
ROOT = Path(__file__).resolve().parent.parent
FINAL_DIR = ROOT / 'data' / 'final'

@st.cache_data
def load_csv(filename):
    path = FINAL_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f'Dataset not found: {path}')
    return pd.read_csv(path, low_memory=False)
try:
    svi = load_csv('sponsorship_value_index_BIGFIVE_96_2025.csv')
    roi = load_csv('BIG_FIVE_SOCIAL_TV_ROI_MASTER_96CLUBS_2024_25.csv')
    recommendations = load_csv('sponsor_club_recommendation_master_FINAL_2025.csv')
    recommendations_top3 = load_csv('sponsor_club_recommendation_TOP3_FINAL_2025.csv')
except Exception as exc:
    st.error(tr('Unable to load the required datasets.'))
    st.exception(exc)
    st.stop()
required_svi = ['club_name', 'league', 'predicted_sponsorship_eur_m', 'SVI_2025', 'svi_rank']
required_roi = ['club_name', 'predicted_sponsorship_eur_m', 'total_media_value_eur_m', 'total_roi_proxy_pct', 'league_final']
missing_svi = [col for col in required_svi if col not in svi.columns]
missing_roi = [col for col in required_roi if col not in roi.columns]
if missing_svi or missing_roi:
    st.error(tr('Some required dataset columns are missing.'))
    st.write(tr('Missing SVI columns:'), missing_svi)
    st.write(tr('Missing ROI columns:'), missing_roi)
    st.stop()
svi = svi.copy()
roi = roi.copy()
for col in ['predicted_sponsorship_eur_m', 'SVI_2025', 'svi_rank']:
    svi[col] = pd.to_numeric(svi[col], errors='coerce')
for col in ['predicted_sponsorship_eur_m', 'total_media_value_eur_m', 'total_roi_proxy_pct']:
    roi[col] = pd.to_numeric(roi[col], errors='coerce')
svi = svi.sort_values('svi_rank', ascending=True)
if LOGO_PATH.is_file():
    LOGO_DATA_URL = 'data:image/png;base64,' + base64.b64encode(LOGO_PATH.read_bytes()).decode('ascii')
    SITE_LINK = escape(SBL_WEBSITE, quote=True)
    SBL_LOGO_LINK = f'<a class="sbl-logo-link" href="{SITE_LINK}" target="_blank" rel="noopener noreferrer" aria-label="Open SBL Consultancy website" title="Visit SBL Consultancy website"><img src="{LOGO_DATA_URL}" alt="SBL Consultancy logo" /></a>'
else:
    SBL_LOGO_LINK = '<span style="font-weight:800;color:#1E344B">SBL Consultancy</span>'
ITALIAN_TRANSLATIONS = {
    'Unable to load the required datasets.': 'Impossibile caricare i dataset richiesti.',
    'Some required dataset columns are missing.': 'Mancano alcune colonne obbligatorie nei dataset.',
    'Missing SVI columns:': 'Colonne SVI mancanti:',
    'Missing ROI columns:': 'Colonne ROI mancanti:',
    'SBL CONSULTANCY · FOOTBALL ANALYTICS': 'SBL CONSULTANCY · ANALISI CALCIO',
    'SBL CONSULTANCY / FOOTBALL ANALYTICS': 'SBL CONSULTANCY / ANALISI CALCIO',
    'Interactive sponsorship analytics for European football clubs.': 'Analisi interattiva delle sponsorizzazioni per i club calcistici europei.',
    'Project scope': 'Perimetro del progetto',
    '**SVI ranking:** 2025 scoring universe (96 clubs).': '**Ranking SVI:** universo di scoring 2025 (96 club).',
    '**ROI analysis:** 2024/25 competition universe (96 clubs).': '**Analisi ROI:** universo competitivo 2024/25 (96 club).',
    'The dashboard presents model estimates and media-value proxies, not verified sponsorship transaction prices or realized investment returns.': 'La dashboard presenta stime del modello e proxy di media value, non prezzi verificati di contratti di sponsorizzazione né rendimenti finanziari realizzati.',
    'Club valuation, sponsorship ranking and estimated Social + TV media return.': 'Valutazione dei club, ranking delle sponsorizzazioni e rendimento stimato del media value Social + TV.',
    'Overview': 'Panoramica',
    'SVI & Club Ranking': 'SVI e Ranking Club',
    'Club Explorer': 'Analisi Club',
    'Geographic SVI Map': 'Mappa geografica SVI',
    'Sponsor–Club Recommendation': 'Raccomandazione Sponsor–Club',
    'Social + TV ROI': 'ROI Social + TV',
    'Model & Data Quality': 'Modello e Qualità dei dati',
    'Project Overview': 'Panoramica del progetto',
    "A four-step decision-support workflow: explore the model's club sponsorship estimates, examine the geographic SVI distribution, assess sponsor–club digital compatibility, and simulate a potential media-value return from the brand sponsor's perspective.": 'Un percorso decisionale in quattro fasi: esplorare le stime di sponsorizzazione dei club prodotte dal modello, analizzare la distribuzione geografica dello SVI, valutare la compatibilità digitale sponsor–club e simulare un potenziale rendimento in termini di media value dal punto di vista del brand sponsor.',
    'The SVI ranking uses the 2025 scoring universe, while the Social + TV analysis uses the 2024/25 competition universe. Both include 96 club records but are not the same set of clubs or necessarily the same reference period.': "Il ranking SVI utilizza l'universo di scoring 2025, mentre l'analisi Social + TV utilizza l'universo competitivo 2024/25. Entrambi comprendono 96 club, ma non coincidono necessariamente per composizione né per periodo di riferimento.",
    'Clubs in SVI ranking': 'Club nel ranking SVI',
    'Sponsor profiles': 'Profili sponsor',
    'ROI benchmark coverage': 'Copertura benchmark ROI',
    'Model input features': 'Variabili di input del modello',
    'How to use the dashboard': 'Come utilizzare la dashboard',
    '#### 1 · Club valuation': '#### 1 · Valutazione del club',
    'Use **SVI & Club Ranking** or **Club Explorer** to compare model-predicted sponsorship values (€m) and relative SVI positions (0–100) within the 2025 scoring universe.': "Usa **SVI e Ranking Club** o **Analisi Club** per confrontare i valori di sponsorizzazione previsti dal modello (€m) e le posizioni relative dello SVI (0–100) nell'universo di scoring 2025.",
    '#### 2 · Geographic SVI analysis': '#### 2 · Analisi geografica SVI',
    "Use **Geographic SVI Map** to explore the spatial distribution of the 96 clubs. Point color identifies the domestic league, while point size represents the club's SVI quartile.": 'Usa **Mappa geografica SVI** per esplorare la distribuzione spaziale dei 96 club. Il colore del punto identifica il campionato nazionale, mentre la dimensione rappresenta il quartile SVI del club.',
    '#### 3 · Sponsor–club fit': '#### 3 · Compatibilità sponsor–club',
    'Choose a sponsor profile in **Sponsor–Club Recommendation**. Review the saved recommendation order and the digital and platform-mix compatibility measures; then select a club.': "Scegli un profilo sponsor in **Raccomandazione Sponsor–Club**. Esamina l'ordine delle raccomandazioni salvato e le misure di compatibilità digitale e di platform mix, quindi seleziona un club.",
    '#### 4 · Brand ROI scenario': '#### 4 · Scenario ROI del brand',
    'Transfer the selected club to **Social + TV ROI**. Enter an illustrative sponsorship fee and a hypothetical share of club media value attributable to the brand to simulate its media-value ROI proxy.': 'Trasferisci il club selezionato in **ROI Social + TV**. Inserisci un fee di sponsorizzazione illustrativo e una quota ipotetica del media value del club attribuibile al brand per simulare il relativo proxy di ROI sul media value.',
    'The club-level ROI benchmark uses aggregate club media value and a predicted sponsorship reference, whereas the individual brand scenario uses user-entered assumptions. Neither is a verified realized financial return.': "Il benchmark ROI a livello di club utilizza il media value aggregato del club e un valore di sponsorizzazione previsto, mentre lo scenario del singolo brand utilizza ipotesi inserite dall'utente. Nessuno dei due rappresenta un rendimento finanziario realizzato e verificato.",
    'SVI ranking — Top 10': 'Ranking SVI — Top 10',
    'Top 10 within the 96-club SVI scoring universe. Values are model estimates.': "Top 10 nell'universo di scoring SVI composto da 96 club. I valori sono stime del modello.",
    'Sponsorship Value Index': 'Sponsorship Value Index',
    'SVI is a relative 0–100 index within the 2025 scoring universe; the predicted sponsorship value is shown separately in €m. An SVI of 100 does not represent a guaranteed contract value.': "Lo SVI è un indice relativo da 0 a 100 nell'universo di scoring 2025; il valore di sponsorizzazione previsto è mostrato separatamente in €m. Uno SVI pari a 100 non rappresenta un valore contrattuale garantito.",
    'Explore estimated sponsorship values and club positions in the SVI ranking.': 'Esplora i valori di sponsorizzazione stimati e la posizione dei club nel ranking SVI.',
    'Select leagues': 'Seleziona i campionati',
    'Clubs in selected leagues': 'Club nei campionati selezionati',
    'Select at least one league.': 'Seleziona almeno un campionato.',
    'Predicted sponsorship by club': 'Sponsorizzazione prevista per club',
    'The displayed overall ranks refer to the original 96-club ranking; league filters do not recalculate them.': 'Le posizioni complessive mostrate fanno riferimento al ranking originale dei 96 club; i filtri per campionato non le ricalcolano.',
    'Select a club to explore its predicted sponsorship value, Sponsorship Value Index and position relative to league peers.': 'Seleziona un club per esplorarne il valore di sponsorizzazione previsto, lo Sponsorship Value Index e la posizione rispetto agli altri club del campionato.',
    'Club Explorer uses the SVI scoring universe only. ROI information is intentionally kept separate because the ROI dataset refers to a different club universe.': "L'Analisi Club utilizza esclusivamente l'universo di scoring SVI. Le informazioni ROI sono mantenute separate perché il relativo dataset fa riferimento a un diverso universo di club.",
    'Select club': 'Seleziona club',
    'Overall SVI rank': 'Posizione SVI complessiva',
    'Predicted sponsorship': 'Sponsorizzazione prevista',
    'League Benchmark': 'Benchmark del campionato',
    'League average': 'Media del campionato',
    'League median': 'Mediana del campionato',
    'League percentile': 'Percentile nel campionato',
    'League percentile indicates the percentage of league clubs with a lower predicted sponsorship value.': 'Il percentile indica la percentuale di club del campionato con un valore di sponsorizzazione previsto inferiore.',
    'Closest Sponsorship Competitors': 'Competitor di sponsorizzazione più vicini',
    'Club Summary': 'Sintesi del club',
    'The predicted sponsorship value is equal to the league average.': 'Il valore di sponsorizzazione previsto è uguale alla media del campionato.',
    'Predicted sponsorship values are model estimates. They should not be interpreted as observed sponsorship contract prices.': 'I valori di sponsorizzazione previsti sono stime del modello e non devono essere interpretati come prezzi osservati di contratti di sponsorizzazione.',
    'Geographic Distribution of the Sponsorship Value Index': 'Distribuzione geografica dello Sponsorship Value Index',
    'Explore the geographic distribution of the 96 clubs included in the 2025 SVI scoring universe.': "Esplora la distribuzione geografica dei 96 club inclusi nell'universo di scoring SVI 2025.",
    "Point color identifies the domestic league, while point size represents the club's SVI quartile. Larger points correspond to higher SVI quartiles.": 'Il colore del punto identifica il campionato nazionale, mentre la dimensione rappresenta il quartile SVI del club. I punti più grandi corrispondono ai quartili SVI più elevati.',
    'Clubs mapped': 'Club mappati',
    'SVI quartiles': 'Quartili SVI',
    'Stadium coordinates are used to locate clubs. Clubs sharing the same stadium can overlap geographically. Map visualization powered by Kepler.gl; geographic data include OpenStreetMap-derived coordinates.': 'Per localizzare i club vengono utilizzate le coordinate degli stadi. I club che condividono lo stesso stadio possono sovrapporsi geograficamente. Visualizzazione realizzata con Kepler.gl; i dati geografici includono coordinate derivate da OpenStreetMap.',
    'Geographic map file not available. Add `SVI_geographic_map_2025.html` to `dashboard/assets/`.': 'File della mappa geografica non disponibile. Aggiungi `SVI_geographic_map_2025.html` in `dashboard/assets/`.',
    "Explore the club recommendations generated for each sponsor profile by the project's matching system.": 'Esplora le raccomandazioni dei club generate per ciascun profilo sponsor dal sistema di matching del progetto.',
    "Recommendations reflect the project's 2025 sponsor and club data snapshots. Digital fit measures the compatibility calculated by the recommendation system; it does not represent a guaranteed commercial return.": 'Le raccomandazioni riflettono gli snapshot 2025 dei dati sponsor e club del progetto. Il digital fit misura la compatibilità calcolata dal sistema di raccomandazione e non rappresenta un rendimento commerciale garantito.',
    'The recommendation datasets are missing required columns.': 'Nei dataset delle raccomandazioni mancano alcune colonne obbligatorie.',
    'Missing master columns:': 'Colonne mancanti nel master:',
    'Missing Top 3 columns:': 'Colonne mancanti nella Top 3:',
    'Select sponsor profile': 'Seleziona profilo sponsor',
    'No recommendations found for this sponsor.': 'Nessuna raccomandazione trovata per questo sponsor.',
    'Sponsor profiles in dataset': 'Profili sponsor nel dataset',
    'Clubs evaluated for this profile': 'Club valutati per questo profilo',
    'Saved Top 3 recommendations': 'Top 3 raccomandazioni salvate',
    'The saved Top 3 does not exactly match the first three positions in the recommendation master. The saved Top 3 is displayed below without recalculating its order.': "La Top 3 salvata non coincide esattamente con le prime tre posizioni del master delle raccomandazioni. La Top 3 salvata viene mostrata senza ricalcolarne l'ordine.",
    'Top 3 Club Recommendations': 'Top 3 raccomandazioni club',
    "These are the recommendations saved by the project's existing matching system.": 'Queste sono le raccomandazioni salvate dal sistema di matching esistente del progetto.',
    'The Top 3 file contains no records for this sponsor profile.': 'Il file Top 3 non contiene record per questo profilo sponsor.',
    'Digital fit': 'Digital fit',
    'Platform mix fit': 'Platform mix fit',
    'Evaluate a Recommended Club': 'Valuta un club raccomandato',
    "Choose a club from this sponsor profile's saved Top 10 recommendations and transfer it to the brand ROI scenario simulator.": 'Scegli un club tra le Top 10 raccomandazioni salvate per questo profilo sponsor e trasferiscilo al simulatore dello scenario ROI del brand.',
    'Club to evaluate in the ROI simulator': 'Club da valutare nel simulatore ROI',
    'Use this club in the ROI simulator': 'Usa questo club nel simulatore ROI',
    'This club was not found under the same name in the 2024/25 ROI dataset. No club has been transferred. Select the corresponding club manually in the ROI simulator.': 'Questo club non è stato trovato con lo stesso nome nel dataset ROI 2024/25. Nessun club è stato trasferito. Seleziona manualmente il club corrispondente nel simulatore ROI.',
    'Multiple matching club records were found in the ROI dataset. No club has been transferred.': 'Nel dataset ROI sono stati trovati più record corrispondenti al club. Nessun club è stato trasferito.',
    "The saved recommendation rank is preserved. Digital fit and platform mix fit are not used as estimates of the brand's share of media exposure.": 'La posizione della raccomandazione salvata viene mantenuta. Digital fit e platform mix fit non sono utilizzati come stime della quota di esposizione media attribuibile al brand.',
    'Top 10 — Digital Fit Comparison': 'Top 10 — Confronto Digital Fit',
    'Clubs are displayed in the original saved recommendation order. The number beside each club identifies its recommendation rank; bar length represents digital fit only. The recommendation rank is not calculated solely from digital fit.': "I club sono mostrati nell'ordine originale delle raccomandazioni salvate. Il numero accanto a ciascun club identifica la posizione nella raccomandazione; la lunghezza della barra rappresenta esclusivamente il digital fit. Il ranking di raccomandazione non è calcolato soltanto sul digital fit.",
    'Full Recommendation Ranking': 'Ranking completo delle raccomandazioni',
    'Filter by league': 'Filtra per campionato',
    'Recommendation ranks are the original ranks saved in the project dataset. Filtering by league does not recalculate them.': 'Le posizioni delle raccomandazioni sono quelle originali salvate nel dataset del progetto. Il filtro per campionato non le ricalcola.',
    'Download selected sponsor recommendations (CSV)': 'Scarica le raccomandazioni dello sponsor selezionato (CSV)',
    'How to Interpret the Results': 'Come interpretare i risultati',
    "**Digital fit** and **platform mix fit** describe different aspects of the calculated compatibility between the sponsor's social presence and the club's social profile.": '**Digital fit** e **platform mix fit** descrivono aspetti diversi della compatibilità calcolata tra la presenza social dello sponsor e il profilo social del club.',
    "**Recommendation rank** is the original ordering generated by the project's recommendation system. It must not be interpreted as a ranking based solely on digital fit.": "Il **ranking di raccomandazione** è l'ordine originale generato dal sistema di raccomandazione del progetto. Non deve essere interpretato come un ranking basato esclusivamente sul digital fit.",
    '**Predicted sponsorship** is an estimate produced by the predictive model, not a verified commercial offer.': "La **sponsorizzazione prevista** è una stima prodotta dal modello predittivo, non un'offerta commerciale verificata.",
    'ROI-related fields in the recommendation dataset may be unavailable for some clubs and use proxy-based information. Their presence does not establish an actual financial return for a specific sponsor–club agreement.': 'I campi relativi al ROI nel dataset delle raccomandazioni possono non essere disponibili per alcuni club e possono utilizzare informazioni proxy. La loro presenza non dimostra un rendimento finanziario effettivo per uno specifico accordo sponsor–club.',
    'Brand Sponsor — Social + TV ROI Analysis': 'Brand Sponsor — Analisi ROI Social + TV',
    'Perspective: brand sponsor | Club-level benchmark and hypothetical brand-specific investment scenarios': 'Prospettiva: brand sponsor | Benchmark a livello di club e scenari di investimento ipotetici specifici per il brand',
    'Explore estimated media value, predicted sponsorship and the ROI proxy indicators available for the 2024/25 Big Five competition universe.': "Esplora il media value stimato, la sponsorizzazione prevista e gli indicatori proxy di ROI disponibili per l'universo competitivo Big Five 2024/25.",
    'The indicators shown here are media-value proxies, not realized financial returns. The ROI dataset refers to the 2024/25 competition universe, while some sponsorship estimates originate from a different scoring reference period.': "Gli indicatori mostrati sono proxy di media value, non rendimenti finanziari realizzati. Il dataset ROI si riferisce all'universo competitivo 2024/25, mentre alcune stime di sponsorizzazione derivano da un diverso periodo di riferimento dello scoring.",
    'Brand Sponsor — ROI Scenario Simulator': 'Brand Sponsor — Simulatore scenario ROI',
    'Simulate the potential media-value return of a sponsorship agreement from the perspective of an individual brand.': 'Simula il potenziale rendimento in termini di media value di un accordo di sponsorizzazione dal punto di vista di un singolo brand.',
    "This is a hypothetical scenario, not an estimate of an existing sponsorship contract. The club-level media value comes from the 2024/25 ROI dataset; the sponsorship fee and the brand's share of exposure are assumptions entered by the user.": "Si tratta di uno scenario ipotetico, non della stima di un contratto di sponsorizzazione esistente. Il media value a livello di club deriva dal dataset ROI 2024/25; il fee di sponsorizzazione e la quota di esposizione del brand sono ipotesi inserite dall'utente.",
    'Select the club': 'Seleziona il club',
    'The selected club comes from the sponsor–club recommendation system. The hypothetical fee and the brand-attributable exposure share must still be entered separately. Recommendation and ROI datasets may refer to different reference periods.': 'Il club selezionato proviene dal sistema di raccomandazione sponsor–club. Il fee ipotetico e la quota di esposizione attribuibile al brand devono comunque essere inseriti separatamente. I dataset di raccomandazione e ROI possono riferirsi a periodi differenti.',
    'Social or TV media-value data are unavailable for the selected club.': 'I dati di media value Social o TV non sono disponibili per il club selezionato.',
    'Hypothetical sponsorship fee (€m)': 'Fee di sponsorizzazione ipotetico (€m)',
    'Hypothetical share of club media value attributable to the brand (%)': 'Quota ipotetica del media value del club attribuibile al brand (%)',
    'The initial fee (€1m) and exposure share (5%) are illustrative starting values, not observed contract terms. Adjust both inputs to explore your own scenario.': 'Il fee iniziale (€1m) e la quota di esposizione (5%) sono valori di partenza illustrativi, non condizioni contrattuali osservate. Modifica entrambi gli input per esplorare il tuo scenario.',
    "**Reference period:** The club media-value inputs refer to the project's 2024/25 competition dataset, with social fanbase inputs drawn from a 2025 snapshot. For a same-period scenario, enter a hypothetical sponsorship fee for one comparable season and an exposure share referring to that same season. If you know only a multi-year contract fee, do not compare its full value with a single season of media value. This scenario does **not** forecast next season's ROI or a realized financial return.": '**Periodo di riferimento:** gli input di media value del club si riferiscono al dataset competitivo 2024/25 del progetto, con dati della fanbase social derivati da uno snapshot 2025. Per uno scenario sullo stesso periodo, inserisci un fee di sponsorizzazione ipotetico relativo a una stagione comparabile e una quota di esposizione riferita alla stessa stagione. Se conosci soltanto il valore complessivo di un contratto pluriennale, non confrontarlo con il media value di una singola stagione. Questo scenario **non** prevede il ROI della stagione successiva né un rendimento finanziario realizzato.',
    '#### Estimated media value': '#### Media value stimato',
    'Club Social + TV media value': 'Media value Social + TV del club',
    'Media value attributed to brand': 'Media value attribuito al brand',
    '#### Sponsorship investment and return': '#### Investimento di sponsorizzazione e rendimento',
    'Hypothetical sponsorship fee': 'Fee di sponsorizzazione ipotetico',
    'Brand media-value ROI proxy': 'Proxy ROI del media value del brand',
    'Media-value coverage of hypothetical fee': 'Copertura del fee ipotetico tramite media value',
    'Brand ROI — Sensitivity Analysis': 'ROI del brand — Analisi di sensitività',
    "How the brand's hypothetical media-value ROI varies with its assumed share of club media value. The club and hypothetical same-season fee remain fixed.": 'Mostra come varia il ROI ipotetico del media value del brand al variare della quota assunta del media value del club. Il club e il fee ipotetico della stessa stagione rimangono fissi.',
    'Illustrative scenarios only. The fee and club-level media value remain fixed; only the assumed share attributable to the brand changes. The ROI is a media-value proxy, not a future or realized return.': 'Scenari esclusivamente illustrativi. Il fee e il media value a livello di club rimangono fissi; cambia soltanto la quota ipotizzata attribuibile al brand. Il ROI è un proxy di media value, non un rendimento futuro o realizzato.',
    'Media-Value Break-Even': 'Break-even del media value',
    "Under the current assumptions, even attributing **100% of the club's estimated Social + TV media value** to the brand would not cover the hypothetical sponsorship fee.": 'Con le ipotesi correnti, anche attribuendo al brand il **100% del media value Social + TV stimato del club**, il valore non coprirebbe il fee di sponsorizzazione ipotetico.',
    'How is the brand ROI scenario calculated?': 'Come viene calcolato lo scenario ROI del brand?',
    'Here, q is the hypothetical percentage of club-level media value attributed to the brand, and C is the hypothetical fee paid by that brand.': 'Qui, q è la percentuale ipotetica del media value a livello di club attribuita al brand e C è il fee ipotetico pagato dal brand.',
    'The model does not estimate brand-specific exposure shares or actual contract prices. The scenario therefore depends on the assumptions selected by the user.': "Il modello non stima quote di esposizione specifiche per il brand né prezzi contrattuali effettivi. Lo scenario dipende quindi dalle ipotesi selezionate dall'utente.",
    'Media-equivalent value is not incremental revenue or profit. This proxy excludes other potential sponsorship benefits, such as sales effects, hospitality, licensing and brand activation.': 'Il valore media-equivalente non rappresenta ricavi o profitti incrementali. Questo proxy esclude altri potenziali benefici della sponsorizzazione, come effetti sulle vendite, hospitality, licensing e brand activation.',
    'Club-Level Media-Value Benchmark': 'Benchmark del media value a livello di club',
    'The following tables and charts compare **aggregate club-level Social + TV media value** with a model-predicted sponsorship reference. This is a benchmark for exploring clubs; it is **not a brand-specific contract ROI**.': 'Le tabelle e i grafici seguenti confrontano il **media value Social + TV aggregato a livello di club** con un riferimento di sponsorizzazione previsto dal modello. È un benchmark per analizzare i club; **non è il ROI di uno specifico contratto del brand**.',
    'The benchmark can use different TV audience methodologies across leagues. A negative ROI proxy means that the measured media-equivalent value is below the hypothetical reference amount; it does not demonstrate a realized financial loss.': "Il benchmark può utilizzare metodologie diverse per l'audience TV tra i campionati. Un proxy ROI negativo significa che il valore media-equivalente misurato è inferiore all'importo di riferimento ipotetico; non dimostra una perdita finanziaria realizzata.",
    'ROI Data Availability': 'Disponibilità dei dati ROI',
    'No recognized ROI percentage fields were found in the dataset.': 'Nel dataset non sono stati trovati campi percentuali ROI riconosciuti.',
    'Coverage is calculated separately for each original CSV field. Different ROI definitions are not automatically combined.': 'La copertura è calcolata separatamente per ciascun campo originale del CSV. Le diverse definizioni di ROI non vengono combinate automaticamente.',
    'No available total ROI percentage field was found in the master dataset.': 'Nel dataset master non è stato trovato alcun campo percentuale disponibile per il ROI totale.',
    'Select ROI indicator': 'Seleziona indicatore ROI',
    'Club Coverage': 'Copertura club',
    'Sponsorship estimates available': 'Stime di sponsorizzazione disponibili',
    'Selected ROI values available': 'Valori ROI selezionati disponibili',
    'Selected ROI coverage': 'Copertura ROI selezionata',
    'Select at least one league to display results.': 'Seleziona almeno un campionato per visualizzare i risultati.',
    'ROI Coverage by League': 'Copertura ROI per campionato',
    'TV Audience — Data Methodology': 'Audience TV — Metodologia dei dati',
    'Club-Level Results': 'Risultati a livello di club',
    'Download displayed ROI results (CSV)': 'Scarica i risultati ROI visualizzati (CSV)',
    'No missing values in this field for the selected leagues.': 'Nessun valore mancante in questo campo per i campionati selezionati.',
    'ROI Comparison — Available Clubs': 'Confronto ROI — Club disponibili',
    'Only clubs with an available value in the selected ROI field are plotted. Missing values are excluded rather than treated as zero.': 'Nel grafico sono inclusi solo i club con un valore disponibile nel campo ROI selezionato. I valori mancanti vengono esclusi anziché essere considerati pari a zero.',
    'Media Value vs Predicted Sponsorship': 'Media Value vs Sponsorizzazione prevista',
    'The chart includes only records with both variables available. Media value may incorporate modeled audiences and advertising-equivalent assumptions.': 'Il grafico include soltanto i record per i quali entrambe le variabili sono disponibili. Il media value può incorporare audience modellate e ipotesi di advertising-equivalent value.',
    'ROI Methodology and Interpretation': 'Metodologia e interpretazione del ROI',
    'The dataset contains multiple ROI-related fields, including total ROI, base-scenario ROI and social-only ROI. These are displayed as separate indicators and are not merged without a dedicated methodology audit.': 'Il dataset contiene diversi campi relativi al ROI, tra cui ROI totale, ROI dello scenario base e ROI relativo al solo social. Sono mostrati come indicatori separati e non vengono combinati senza uno specifico audit metodologico.',
    'An advertising-equivalent media value is not the same as incremental revenue or profit. The predicted sponsorship value is also not necessarily the price of an actual contract.': 'Un advertising-equivalent media value non equivale a ricavi o profitti incrementali. Anche il valore di sponsorizzazione previsto non corrisponde necessariamente al prezzo di un contratto effettivo.',
    "The 2024/25 competition universe and the reference period of the model's sponsorship estimates must be distinguished when interpreting the results.": "Nell'interpretazione dei risultati occorre distinguere l'universo competitivo 2024/25 dal periodo di riferimento delle stime di sponsorizzazione del modello.",
    'Temporal predictive validation — 2023/24': 'Validazione predittiva temporale — 2023/24',
    'High-quality test observations': 'Osservazioni di test ad alta qualità',
    'XGBoost Model B Original. Validation statistics refer to the 16 high-quality observations in the 2023/24 temporal test, not all 96 clubs in the scoring universe.': "XGBoost Model B Original. Le statistiche di validazione si riferiscono alle 16 osservazioni ad alta qualità del test temporale 2023/24, non a tutti i 96 club dell'universo di scoring.",
    'Coverage and scoring readiness': 'Copertura e readiness dello scoring',
    'SVI scoring coverage': 'Copertura scoring SVI',
    'ROI club coverage': 'Copertura club ROI',
    'Model feature completeness': 'Completezza delle feature del modello',
    'Feature completeness refers to the 40 numeric model inputs after data preparation. It does not establish 100% completeness of raw source data.': 'La completezza delle feature si riferisce ai 40 input numerici del modello dopo la preparazione dei dati. Non implica una completezza del 100% dei dati grezzi di origine.',
    'Ranking stability — exploratory': 'Stabilità del ranking — analisi esplorativa',
    'Spearman correlation': 'Correlazione di Spearman',
    'Mean absolute rank change': 'Variazione media assoluta di posizione',
    'Top 10 retention': 'Mantenimento Top 10',
    'These exploratory results compare the 30 clubs common to the historical 2023/24 Model B ranking and the subsequent 2025 SVI output. They are not yet a certified consecutive-season stability KPI for the complete Big Five universe.': "Questi risultati esplorativi confrontano i 30 club comuni al ranking storico Model B 2023/24 e al successivo output SVI 2025. Non costituiscono ancora un KPI certificato di stabilità tra stagioni consecutive per l'intero universo Big Five.",
    'SBL Consultancy | Sponsorship Value Index Predictor | Model estimates and proxy-based analyses': 'SBL Consultancy | Sponsorship Value Index Predictor | Stime del modello e analisi basate su proxy',
    'Overall rank': 'Posizione complessiva',
    'Club': 'Club',
    'League': 'Campionato',
    'Predicted sponsorship (€m)': 'Sponsorizzazione prevista (€m)',
    'League rank': 'Posizione nel campionato',
    'Absolute difference (€m)': 'Differenza assoluta (€m)',
    'Selection': 'Selezione',
    'Selected club': 'Club selezionato',
    'League peers': 'Altri club del campionato',
    'Category': 'Categoria',
    'Recommendation rank': 'Posizione raccomandazione',
    'Saved recommendation rank': 'Posizione raccomandazione salvata',
    'Recommendation class': 'Classe di raccomandazione',
    'Recommendation evidence': 'Evidenza della raccomandazione',
    'ROI data support': 'Supporto dati ROI',
    'Digital fit (0–100)': 'Digital fit (0–100)',
    'ROI field': 'Campo ROI',
    'Indicator': 'Indicatore',
    'Clubs with data': 'Club con dati',
    'Clubs without data': 'Club senza dati',
    'Coverage (%)': 'Copertura (%)',
    'Clubs': 'Club',
    'Sponsorship estimates': 'Stime di sponsorizzazione',
    'Available ROI values': 'Valori ROI disponibili',
    'ROI coverage (%)': 'Copertura ROI (%)',
    'Methodology not specified': 'Metodologia non specificata',
    'TV methodology': 'Metodologia TV',
    'Estimated Social + TV value (€m)': 'Media value Social + TV stimato (€m)',
    'Scenario': 'Scenario',
    'Current selection': 'Selezione corrente',
    'Alternative': 'Alternativa',
    'Exposure share (%)': 'Quota di esposizione (%)',
    'Brand media value (€m)': 'Media value del brand (€m)',
    'Hypothetical fee (€m)': 'Fee ipotetico (€m)',
    'Brand ROI proxy (%)': 'Proxy ROI del brand (%)',
    'Total ROI proxy (%) — original field': 'Proxy ROI totale (%) — campo originale',
    'Total ROI proxy (%) — base scenario': 'Proxy ROI totale (%) — scenario base',
    'Social + TV media-value ROI proxy (%) — all 96 clubs': 'Proxy ROI del media value Social + TV (%) — tutti i 96 club',
    'Social ROI proxy (%) — social only': 'Proxy ROI Social (%) — solo social',
    'Social ROI (%) — alternative social field': 'ROI Social (%) — campo social alternativo',
    '3.07 positions': '3.07 posizioni',
}

def is_italian():
    return st.session_state.get('dashboard_language', 'English') == 'Italiano'

def tr(value):
    """Translate user-facing dashboard copy while preserving data values."""
    if not isinstance(value, str) or not is_italian():
        return value
    if value in ITALIAN_TRANSLATIONS:
        return ITALIAN_TRANSLATIONS[value]
    if value.endswith(' rank') and (not value.startswith('Overall ')):
        return f'Posizione {value[:-5]}'
    if value.endswith(' · club vs league average'):
        return value.replace(' · club vs league average', ' · club vs media campionato')
    if value.endswith(' · club vs league median'):
        return value.replace(' · club vs league median', ' · club vs mediana campionato')
    m = re.fullmatch('\\*\\*(.+?)\\*\\* is ranked \\*\\*#(\\d+) overall\\*\\* in the 96-club SVI scoring universe and \\*\\*#(\\d+) in (.+?)\\*\\*\\.', value)
    if m:
        club, overall, league_rank, league = m.groups()
        return f"**{club}** occupa la posizione **#{overall} complessiva** nell'universo di scoring SVI dei 96 club e la posizione **#{league_rank} in {league}**."
    m = re.fullmatch('The model estimates a sponsorship value of \\*\\*€([0-9.]+) million\\*\\*, corresponding to an SVI score of \\*\\*([0-9.]+)\\*\\*\\.', value)
    if m:
        sponsorship, svi_score = m.groups()
        return f'Il modello stima un valore di sponsorizzazione di **€{sponsorship} milioni**, corrispondente a uno SVI di **{svi_score}**.'
    m = re.fullmatch('The predicted sponsorship value is \\*\\*€([0-9.]+) million (above|below)\\*\\* the (.+?) average\\.', value)
    if m:
        amount, direction, league = m.groups()
        direction_it = 'superiore di' if direction == 'above' else 'inferiore di'
        return f'Il valore di sponsorizzazione previsto è **{direction_it} €{amount} milioni** rispetto alla media di {league}.'
    m = re.fullmatch('Category: (.+?) \\| Sponsor profile: 2025 snapshot', value)
    if m:
        return f'Categoria: {m.group(1)} | Profilo sponsor: snapshot 2025'
    m = re.fullmatch('Recommendation class: (.+)', value)
    if m:
        return f'Classe di raccomandazione: {m.group(1)}'
    m = re.fullmatch("(.+?) → (.+?) selected\\. Open the 'Social \\+ TV ROI' tab to continue with the simulator\\.", value)
    if m:
        sponsor, club = m.groups()
        return f"{sponsor} → {club} selezionato. Apri la scheda 'ROI Social + TV' per continuare con il simulatore."
    m = re.fullmatch('Recommendation selected: (.+?) → (.+)', value)
    if m:
        return f'Raccomandazione selezionata: {m.group(1)} → {m.group(2)}'
    m = re.fullmatch('Scenario Results — (.+)', value)
    if m:
        return f'Risultati scenario — {m.group(1)}'
    m = re.fullmatch('Currently displaying the original CSV field: `(.+?)`\\. Missing values remain missing; no estimates are generated to fill them\\.', value)
    if m:
        return f'Campo CSV originale attualmente visualizzato: `{m.group(1)}`. I valori mancanti restano tali; non vengono generate stime per completarli.'
    m = re.fullmatch('Fully observed TV audience: (\\d+)/(\\d+) clubs in the selected leagues\\. Other TV audience values use proxy-based methodologies\\. The ROI indicator combines these different data sources and should not be interpreted as a realized financial return\\.', value)
    if m:
        return f"Audience TV interamente osservata: {m.group(1)}/{m.group(2)} club nei campionati selezionati. Gli altri valori di audience TV utilizzano metodologie basate su proxy. L'indicatore ROI combina queste diverse fonti dati e non deve essere interpretato come rendimento finanziario realizzato."
    m = re.fullmatch('Clubs without a value in the selected ROI field \\((\\d+)\\)', value)
    if m:
        return f'Club senza un valore nel campo ROI selezionato ({m.group(1)})'
    m = re.fullmatch("Under the current assumptions, the brand would need to receive approximately \\*\\*([0-9.]+)%\\*\\* of the club's estimated Social \\+ TV media value for that media value to equal the hypothetical sponsorship fee\\.", value)
    if m:
        return f'Con le ipotesi correnti, il brand dovrebbe ricevere circa **{m.group(1)}%** del media value Social + TV stimato del club affinché tale media value eguagli il fee di sponsorizzazione ipotetico.'
    return value

def tr_dict(mapping):
    """Translate display labels in Plotly/pandas mappings without changing data keys."""
    if not isinstance(mapping, dict):
        return mapping
    return {key: tr(value) if isinstance(value, str) else value for key, value in mapping.items()}
with st.sidebar:
    st.markdown(tr(f'<div class="sbl-sidebar-brand">{SBL_LOGO_LINK}</div>'), unsafe_allow_html=True)
    st.radio('Language / Lingua', options=['English', 'Italiano'], horizontal=True, key='dashboard_language')
    st.markdown(tr('### SVI Predictor'))
    st.caption(tr('SBL CONSULTANCY · FOOTBALL ANALYTICS'))
    st.write(tr('Interactive sponsorship analytics for European football clubs.'))
    st.divider()
    st.subheader(tr('Project scope'))
    st.write(tr('**SVI ranking:** 2025 scoring universe (96 clubs).'))
    st.write(tr('**ROI analysis:** 2024/25 competition universe (96 clubs).'))
    st.divider()
    st.caption(tr('The dashboard presents model estimates and media-value proxies, not verified sponsorship transaction prices or realized investment returns.'))
hero_eyebrow = tr('SBL CONSULTANCY / FOOTBALL ANALYTICS')
hero_subtitle = tr('Club valuation, sponsorship ranking and estimated Social + TV media return.')
st.markdown(tr(f'\n    <div class="sbl-hero">\n        {SBL_LOGO_LINK}\n        <div class="sbl-hero-copy">\n            <div class="sbl-eyebrow">{hero_eyebrow}</div>\n            <h1>Sponsorship Value Index Predictor</h1>\n            <p>{hero_subtitle}</p>\n        </div>\n    </div>\n    '), unsafe_allow_html=True)
overview_tab, svi_tab, club_tab, map_tab, recommendation_tab, roi_tab, quality_tab = st.tabs([tr('Overview'), tr('SVI & Club Ranking'), tr('Club Explorer'), tr('Geographic SVI Map'), tr('Sponsor–Club Recommendation'), tr('Social + TV ROI'), tr('Model & Data Quality')])
with overview_tab:
    st.header(tr('Project Overview'))
    st.write(tr("A four-step decision-support workflow: explore the model's club sponsorship estimates, examine the geographic SVI distribution, assess sponsor–club digital compatibility, and simulate a potential media-value return from the brand sponsor's perspective."))
    st.info(tr('The SVI ranking uses the 2025 scoring universe, while the Social + TV analysis uses the 2024/25 competition universe. Both include 96 club records but are not the same set of clubs or necessarily the same reference period.'))
    roi_coverage_overview = int(pd.to_numeric(roi['total_roi_pct'], errors='coerce').notna().sum()) if 'total_roi_pct' in roi.columns else 0
    summary_1, summary_2, summary_3, summary_4 = st.columns(4)
    summary_1.metric(tr('Clubs in SVI ranking'), tr(len(svi)))
    summary_2.metric(tr('Sponsor profiles'), tr(recommendations['sponsor_entity_key'].dropna().nunique()))
    summary_3.metric(tr('ROI benchmark coverage'), tr(f'{roi_coverage_overview} / {len(roi)}'))
    summary_4.metric(tr('Model input features'), tr(40))
    st.divider()
    st.subheader(tr('How to use the dashboard'))
    workflow_1, workflow_2, workflow_3, workflow_4 = st.columns(4)
    with workflow_1:
        st.markdown(tr('#### 1 · Club valuation'))
        st.write(tr('Use **SVI & Club Ranking** or **Club Explorer** to compare model-predicted sponsorship values (€m) and relative SVI positions (0–100) within the 2025 scoring universe.'))
    with workflow_2:
        st.markdown(tr('#### 2 · Geographic SVI analysis'))
        st.write(tr("Use **Geographic SVI Map** to explore the spatial distribution of the 96 clubs. Point color identifies the domestic league, while point size represents the club's SVI quartile."))
    with workflow_3:
        st.markdown(tr('#### 3 · Sponsor–club fit'))
        st.write(tr('Choose a sponsor profile in **Sponsor–Club Recommendation**. Review the saved recommendation order and the digital and platform-mix compatibility measures; then select a club.'))
    with workflow_4:
        st.markdown(tr('#### 4 · Brand ROI scenario'))
        st.write(tr('Transfer the selected club to **Social + TV ROI**. Enter an illustrative sponsorship fee and a hypothetical share of club media value attributable to the brand to simulate its media-value ROI proxy.'))
    st.caption(tr('The club-level ROI benchmark uses aggregate club media value and a predicted sponsorship reference, whereas the individual brand scenario uses user-entered assumptions. Neither is a verified realized financial return.'))
    st.divider()
    st.subheader(tr('SVI ranking — Top 10'))
    overview_top10 = svi.head(10)
    chart = px.bar(overview_top10.sort_values('predicted_sponsorship_eur_m'), x='predicted_sponsorship_eur_m', y='club_name', orientation='h', color='league', labels=tr_dict({'predicted_sponsorship_eur_m': 'Predicted sponsorship (€m)', 'club_name': 'Club'}), hover_data=['SVI_2025', 'svi_rank'])
    chart.update_layout(height=480, yaxis_title=None)
    st.plotly_chart(chart, use_container_width=True)
    st.caption(tr('Top 10 within the 96-club SVI scoring universe. Values are model estimates.'))
with svi_tab:
    st.header(tr('Sponsorship Value Index'))
    st.caption(tr('SVI is a relative 0–100 index within the 2025 scoring universe; the predicted sponsorship value is shown separately in €m. An SVI of 100 does not represent a guaranteed contract value.'))
    st.write(tr('Explore estimated sponsorship values and club positions in the SVI ranking.'))
    selected_leagues = st.multiselect(tr('Select leagues'), options=sorted(svi['league'].dropna().unique()), default=sorted(svi['league'].dropna().unique()), key='svi_leagues')
    filtered_svi = svi[svi['league'].isin(selected_leagues)].copy()
    st.metric(tr('Clubs in selected leagues'), tr(len(filtered_svi)))
    if filtered_svi.empty:
        st.warning(tr('Select at least one league.'))
    else:
        ranking_display = filtered_svi[['svi_rank', 'club_name', 'league', 'predicted_sponsorship_eur_m', 'SVI_2025']].rename(columns=tr_dict({'svi_rank': 'Overall rank', 'club_name': 'Club', 'league': 'League', 'predicted_sponsorship_eur_m': 'Predicted sponsorship (€m)', 'SVI_2025': 'SVI'}))
        st.dataframe(ranking_display, use_container_width=True, hide_index=True)
        st.subheader(tr('Predicted sponsorship by club'))
        chart = px.bar(filtered_svi.head(20).sort_values('predicted_sponsorship_eur_m'), x='predicted_sponsorship_eur_m', y='club_name', color='league', orientation='h', labels=tr_dict({'predicted_sponsorship_eur_m': 'Predicted sponsorship (€m)', 'club_name': 'Club'}))
        chart.update_layout(height=650, yaxis_title=None)
        st.plotly_chart(chart, use_container_width=True)
        st.caption(tr('The displayed overall ranks refer to the original 96-club ranking; league filters do not recalculate them.'))
with club_tab:
    st.header(tr('Club Explorer'))
    st.write(tr('Select a club to explore its predicted sponsorship value, Sponsorship Value Index and position relative to league peers.'))
    st.info(tr('Club Explorer uses the SVI scoring universe only. ROI information is intentionally kept separate because the ROI dataset refers to a different club universe.'))
    club_options = sorted(svi['club_name'].dropna().unique().tolist())
    selected_club = st.selectbox(tr('Select club'), options=club_options, index=0, key='club_explorer_selection')
    club_row = svi.loc[svi['club_name'] == selected_club].iloc[0]
    club_league = club_row['league']
    league_data = svi.loc[svi['league'] == club_league].copy().sort_values('predicted_sponsorship_eur_m', ascending=False).reset_index(drop=True)
    league_data['league_rank_calculated'] = league_data['predicted_sponsorship_eur_m'].rank(method='min', ascending=False).astype(int)
    selected_league_row = league_data.loc[league_data['club_name'] == selected_club].iloc[0]
    league_rank = int(selected_league_row['league_rank_calculated'])
    league_size = len(league_data)
    st.subheader(tr(selected_club))
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(tr('Overall SVI rank'), tr(f"#{int(club_row['svi_rank'])}"))
    col2.metric(tr('Predicted sponsorship'), tr(f"€{club_row['predicted_sponsorship_eur_m']:.2f}m"))
    col3.metric(tr('SVI'), tr(f"{club_row['SVI_2025']:.2f}"))
    col4.metric(tr(f'{club_league} rank'), tr(f'#{league_rank} / {league_size}'))
    st.divider()
    st.subheader(tr('League Benchmark'))
    league_mean = league_data['predicted_sponsorship_eur_m'].mean()
    league_median = league_data['predicted_sponsorship_eur_m'].median()
    club_value = float(club_row['predicted_sponsorship_eur_m'])
    difference_vs_mean = club_value - league_mean
    difference_vs_median = club_value - league_median
    col1, col2, col3 = st.columns(3)
    col1.metric(tr('League average'), tr(f'€{league_mean:.2f}m'), delta=tr(f'{difference_vs_mean:+.2f}m · club vs league average'), delta_color='off')
    col2.metric(tr('League median'), tr(f'€{league_median:.2f}m'), delta=tr(f'{difference_vs_median:+.2f}m · club vs league median'), delta_color='off')
    clubs_below = int((league_data['predicted_sponsorship_eur_m'] < club_value).sum())
    league_percentile = clubs_below / league_size * 100
    col3.metric(tr('League percentile'), tr(f'{league_percentile:.1f}%'))
    st.caption(tr('League percentile indicates the percentage of league clubs with a lower predicted sponsorship value.'))
    st.divider()
    st.subheader(tr(f'{selected_club} vs {club_league}'))
    chart_data = league_data.copy()
    chart_data['Selection'] = chart_data['club_name'].apply(lambda x: tr('Selected club') if x == selected_club else tr('League peers'))
    league_chart = px.bar(chart_data.sort_values('predicted_sponsorship_eur_m', ascending=True), x='predicted_sponsorship_eur_m', y='club_name', orientation='h', color='Selection', labels=tr_dict({'predicted_sponsorship_eur_m': 'Predicted sponsorship (€m)', 'club_name': 'Club', 'Selection': ''}), hover_data={'SVI_2025': ':.2f', 'svi_rank': True, 'league_rank_calculated': True})
    league_chart.update_layout(height=max(500, league_size * 30), yaxis_title=None, legend_title_text='')
    st.plotly_chart(league_chart, use_container_width=True)
    st.divider()
    st.subheader(tr('Closest Sponsorship Competitors'))
    competitor_data = league_data.copy()
    competitor_data['difference_from_selected_eur_m'] = (competitor_data['predicted_sponsorship_eur_m'] - club_value).abs()
    competitors = competitor_data.loc[competitor_data['club_name'] != selected_club].sort_values('difference_from_selected_eur_m').head(5)
    competitors_display = competitors[['league_rank_calculated', 'club_name', 'predicted_sponsorship_eur_m', 'SVI_2025', 'svi_rank', 'difference_from_selected_eur_m']].rename(columns=tr_dict({'league_rank_calculated': 'League rank', 'club_name': 'Club', 'predicted_sponsorship_eur_m': 'Predicted sponsorship (€m)', 'SVI_2025': 'SVI', 'svi_rank': 'Overall rank', 'difference_from_selected_eur_m': 'Absolute difference (€m)'}))
    st.dataframe(competitors_display, use_container_width=True, hide_index=True)
    st.divider()
    st.subheader(tr('Club Summary'))
    st.write(tr(f"**{selected_club}** is ranked **#{int(club_row['svi_rank'])} overall** in the 96-club SVI scoring universe and **#{league_rank} in {club_league}**."))
    st.write(tr(f"The model estimates a sponsorship value of **€{club_value:.2f} million**, corresponding to an SVI score of **{club_row['SVI_2025']:.2f}**."))
    if difference_vs_mean > 0:
        st.write(tr(f'The predicted sponsorship value is **€{abs(difference_vs_mean):.2f} million above** the {club_league} average.'))
    elif difference_vs_mean < 0:
        st.write(tr(f'The predicted sponsorship value is **€{abs(difference_vs_mean):.2f} million below** the {club_league} average.'))
    else:
        st.write(tr('The predicted sponsorship value is equal to the league average.'))
    st.caption(tr('Predicted sponsorship values are model estimates. They should not be interpreted as observed sponsorship contract prices.'))
with map_tab:
    st.header(tr('Geographic Distribution of the Sponsorship Value Index'))
    st.write(tr('Explore the geographic distribution of the 96 clubs included in the 2025 SVI scoring universe.'))
    st.info(tr("Point color identifies the domestic league, while point size represents the club's SVI quartile. Larger points correspond to higher SVI quartiles."))
    map_note_1, map_note_2 = st.columns(2)
    map_note_1.metric(tr('Clubs mapped'), tr('96'))
    map_note_2.metric(tr('SVI quartiles'), tr('4'))
    if MAP_PATH.exists():
        map_html = MAP_PATH.read_text(encoding='utf-8')
        map_html = map_html.replace('readOnly: false', 'readOnly: true', 1)
        components.html(map_html, height=760, scrolling=False)
        st.caption(tr('Stadium coordinates are used to locate clubs. Clubs sharing the same stadium can overlap geographically. Map visualization powered by Kepler.gl; geographic data include OpenStreetMap-derived coordinates.'))
    else:
        st.warning(tr('Geographic map file not available. Add `SVI_geographic_map_2025.html` to `dashboard/assets/`.'))
with recommendation_tab:
    st.header(tr('Sponsor–Club Recommendation'))
    st.write(tr("Explore the club recommendations generated for each sponsor profile by the project's matching system."))
    st.info(tr("Recommendations reflect the project's 2025 sponsor and club data snapshots. Digital fit measures the compatibility calculated by the recommendation system; it does not represent a guaranteed commercial return."))
    required_recommendation_columns = ['sponsor_entity_key', 'sponsor_name', 'category', 'club_name', 'league', 'final_recommendation_rank', 'sponsor_club_digital_fit', 'sponsor_club_platform_mix_fit', 'predicted_sponsorship_eur_m', 'SVI_2025', 'svi_rank']
    missing_master = [col for col in required_recommendation_columns if col not in recommendations.columns]
    missing_top3 = [col for col in required_recommendation_columns if col not in recommendations_top3.columns]
    if missing_master or missing_top3:
        st.error(tr('The recommendation datasets are missing required columns.'))
        st.write(tr('Missing master columns:'), missing_master)
        st.write(tr('Missing Top 3 columns:'), missing_top3)
    else:
        rec = recommendations.copy()
        rec_top3 = recommendations_top3.copy()
        numeric_columns = ['final_recommendation_rank', 'sponsor_club_digital_fit', 'sponsor_club_platform_mix_fit', 'predicted_sponsorship_eur_m', 'SVI_2025', 'svi_rank']
        for df in [rec, rec_top3]:
            for col in numeric_columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        sponsor_options = sorted(rec['sponsor_entity_key'].dropna().astype(str).unique().tolist())
        selected_sponsor = st.selectbox(tr('Select sponsor profile'), options=sponsor_options, key='sponsor_recommendation_selection')
        sponsor_data = rec.loc[rec['sponsor_entity_key'].astype(str) == selected_sponsor].copy().sort_values('final_recommendation_rank', ascending=True)
        sponsor_top3 = rec_top3.loc[rec_top3['sponsor_entity_key'].astype(str) == selected_sponsor].copy().sort_values('final_recommendation_rank', ascending=True)
        if sponsor_data.empty:
            st.warning(tr('No recommendations found for this sponsor.'))
        else:
            sponsor_info = sponsor_data.iloc[0]
            sponsor_name = str(sponsor_info['sponsor_name'])
            sponsor_category = str(sponsor_info['category'])
            st.subheader(tr(sponsor_name))
            st.caption(tr(f'Category: {sponsor_category} | Sponsor profile: 2025 snapshot'))
            col1, col2, col3 = st.columns(3)
            col1.metric(tr('Sponsor profiles in dataset'), tr(len(sponsor_options)))
            col2.metric(tr('Clubs evaluated for this profile'), tr(sponsor_data['club_name'].nunique()))
            col3.metric(tr('Saved Top 3 recommendations'), tr(len(sponsor_top3)))
            expected_top3 = sponsor_data.head(3)['club_name'].astype(str).tolist()
            saved_top3 = sponsor_top3['club_name'].astype(str).tolist()
            if saved_top3 != expected_top3:
                st.warning(tr('The saved Top 3 does not exactly match the first three positions in the recommendation master. The saved Top 3 is displayed below without recalculating its order.'))
            st.divider()
            st.subheader(tr('Top 3 Club Recommendations'))
            st.write(tr("These are the recommendations saved by the project's existing matching system."))
            if sponsor_top3.empty:
                st.warning(tr('The Top 3 file contains no records for this sponsor profile.'))
            else:
                top3_columns = st.columns(min(3, len(sponsor_top3)))
                for position, (_, row) in enumerate(sponsor_top3.head(3).iterrows()):
                    with top3_columns[position]:
                        saved_rank = row['final_recommendation_rank']
                        if pd.notna(saved_rank):
                            rank_label = f'#{int(saved_rank)}'
                        else:
                            rank_label = 'N/A'
                        st.markdown(tr(f"### {rank_label} — {row['club_name']}"))
                        st.caption(tr(str(row['league'])))
                        digital_fit = row['sponsor_club_digital_fit']
                        platform_fit = row['sponsor_club_platform_mix_fit']
                        sponsorship_value = row['predicted_sponsorship_eur_m']
                        st.metric(tr('Digital fit'), tr(f'{digital_fit:.2f}' if pd.notna(digital_fit) else 'N/A'))
                        st.metric(tr('Platform mix fit'), tr(f'{platform_fit:.2f}' if pd.notna(platform_fit) else 'N/A'))
                        st.metric(tr('Predicted sponsorship'), tr(f'€{sponsorship_value:.2f}m' if pd.notna(sponsorship_value) else 'N/A'))
                        if 'recommendation_class' in row.index:
                            st.caption(tr(f"Recommendation class: {row['recommendation_class']}"))
            st.subheader(tr('Evaluate a Recommended Club'))
            st.write(tr("Choose a club from this sponsor profile's saved Top 10 recommendations and transfer it to the brand ROI scenario simulator."))
            roi_shortlist = sponsor_data.head(10).copy()
            roi_club_options = roi_shortlist['club_name'].astype(str).tolist()
            roi_rank_by_club = {str(row['club_name']): f"#{int(row['final_recommendation_rank'])}" if pd.notna(row['final_recommendation_rank']) else 'N/A' for _, row in roi_shortlist.iterrows()}
            selected_recommended_club = st.selectbox(tr('Club to evaluate in the ROI simulator'), options=roi_club_options, format_func=lambda club: f"{roi_rank_by_club.get(club, 'N/A')} — {club}", key=f'recommendation_roi_choice_{selected_sponsor}')
            if st.button(tr('Use this club in the ROI simulator'), key='send_recommendation_to_roi'):
                roi_club_matches = roi.loc[roi['club_name'].astype(str).str.strip().str.casefold() == selected_recommended_club.strip().casefold(), 'club_name'].dropna().unique().tolist()
                if len(roi_club_matches) == 1:
                    st.session_state['brand_roi_simulator_club'] = roi_club_matches[0]
                    st.session_state['roi_scenario_sponsor_name'] = sponsor_name
                    st.session_state['roi_scenario_club_name'] = roi_club_matches[0]
                    st.success(tr(f"{sponsor_name} → {roi_club_matches[0]} selected. Open the 'Social + TV ROI' tab to continue with the simulator."))
                elif len(roi_club_matches) == 0:
                    st.warning(tr('This club was not found under the same name in the 2024/25 ROI dataset. No club has been transferred. Select the corresponding club manually in the ROI simulator.'))
                else:
                    st.warning(tr('Multiple matching club records were found in the ROI dataset. No club has been transferred.'))
            st.caption(tr("The saved recommendation rank is preserved. Digital fit and platform mix fit are not used as estimates of the brand's share of media exposure."))
            st.divider()
            st.subheader(tr('Top 10 — Digital Fit Comparison'))
            top10 = sponsor_data.head(10).copy()
            top10['ranked_club_label'] = top10.apply(lambda row: f"#{int(row['final_recommendation_rank'])} — {row['club_name']}" if pd.notna(row['final_recommendation_rank']) else f"N/A — {row['club_name']}", axis=1)
            top10_chart_data = top10.sort_values('final_recommendation_rank', ascending=False)
            top10_chart = px.bar(top10_chart_data, x='sponsor_club_digital_fit', y='ranked_club_label', orientation='h', color='league', text='sponsor_club_digital_fit', hover_data=['final_recommendation_rank', 'sponsor_club_platform_mix_fit', 'SVI_2025'], labels=tr_dict({'sponsor_club_digital_fit': 'Digital fit (0–100)', 'ranked_club_label': 'Club', 'league': 'League', 'final_recommendation_rank': 'Saved recommendation rank', 'sponsor_club_platform_mix_fit': 'Platform mix fit', 'SVI_2025': 'SVI'}))
            top10_chart.update_traces(texttemplate='%{text:.1f}', textposition='outside', cliponaxis=False)
            top10_chart.update_layout(height=540, yaxis_title=None, xaxis_range=[0, 110], margin=dict(l=15, r=35, t=20, b=20))
            st.plotly_chart(top10_chart, width='stretch')
            st.caption(tr('Clubs are displayed in the original saved recommendation order. The number beside each club identifies its recommendation rank; bar length represents digital fit only. The recommendation rank is not calculated solely from digital fit.'))
            st.divider()
            st.subheader(tr('Full Recommendation Ranking'))
            available_leagues = sorted(sponsor_data['league'].dropna().unique().tolist())
            selected_leagues_rec = st.multiselect(tr('Filter by league'), options=available_leagues, default=available_leagues, key='recommendation_league_filter')
            filtered_recommendations = sponsor_data.loc[sponsor_data['league'].isin(selected_leagues_rec)].copy()
            display_columns = ['final_recommendation_rank', 'club_name', 'league', 'sponsor_club_digital_fit', 'sponsor_club_platform_mix_fit', 'predicted_sponsorship_eur_m', 'SVI_2025', 'svi_rank']
            optional_columns = ['recommendation_class', 'recommendation_evidence', 'roi_support']
            display_columns += [col for col in optional_columns if col in filtered_recommendations.columns]
            ranking_display = filtered_recommendations[display_columns].sort_values('final_recommendation_rank', ascending=True).rename(columns=tr_dict({'final_recommendation_rank': 'Recommendation rank', 'club_name': 'Club', 'league': 'League', 'sponsor_club_digital_fit': 'Digital fit', 'sponsor_club_platform_mix_fit': 'Platform mix fit', 'predicted_sponsorship_eur_m': 'Predicted sponsorship (€m)', 'SVI_2025': 'SVI', 'svi_rank': 'Overall SVI rank', 'recommendation_class': 'Recommendation class', 'recommendation_evidence': 'Recommendation evidence', 'roi_support': 'ROI data support'}))
            st.dataframe(ranking_display, width='stretch', hide_index=True)
            st.caption(tr('Recommendation ranks are the original ranks saved in the project dataset. Filtering by league does not recalculate them.'))
            st.download_button(label=tr('Download selected sponsor recommendations (CSV)'), data=ranking_display.to_csv(index=False).encode('utf-8-sig'), file_name='sponsor_club_recommendations.csv', mime='text/csv', key='download_sponsor_recommendations')
            st.divider()
            st.subheader(tr('How to Interpret the Results'))
            st.write(tr("**Digital fit** and **platform mix fit** describe different aspects of the calculated compatibility between the sponsor's social presence and the club's social profile."))
            st.write(tr("**Recommendation rank** is the original ordering generated by the project's recommendation system. It must not be interpreted as a ranking based solely on digital fit."))
            st.write(tr('**Predicted sponsorship** is an estimate produced by the predictive model, not a verified commercial offer.'))
            st.caption(tr('ROI-related fields in the recommendation dataset may be unavailable for some clubs and use proxy-based information. Their presence does not establish an actual financial return for a specific sponsor–club agreement.'))
with roi_tab:
    st.header(tr('Brand Sponsor — Social + TV ROI Analysis'))
    st.caption(tr('Perspective: brand sponsor | Club-level benchmark and hypothetical brand-specific investment scenarios'))
    st.write(tr('Explore estimated media value, predicted sponsorship and the ROI proxy indicators available for the 2024/25 Big Five competition universe.'))
    st.warning(tr('The indicators shown here are media-value proxies, not realized financial returns. The ROI dataset refers to the 2024/25 competition universe, while some sponsorship estimates originate from a different scoring reference period.'))
    st.divider()
    st.subheader(tr('Brand Sponsor — ROI Scenario Simulator'))
    st.write(tr('Simulate the potential media-value return of a sponsorship agreement from the perspective of an individual brand.'))
    st.info(tr("This is a hypothetical scenario, not an estimate of an existing sponsorship contract. The club-level media value comes from the 2024/25 ROI dataset; the sponsorship fee and the brand's share of exposure are assumptions entered by the user."))
    simulator_clubs = sorted(roi['club_name'].dropna().astype(str).unique().tolist())
    simulated_club_name = st.selectbox(tr('Select the club'), options=simulator_clubs, key='brand_roi_simulator_club')
    context_sponsor = st.session_state.get('roi_scenario_sponsor_name')
    context_club = st.session_state.get('roi_scenario_club_name')
    if context_sponsor and context_club == simulated_club_name:
        st.success(tr(f'Recommendation selected: {context_sponsor} → {simulated_club_name}'))
        st.caption(tr('The selected club comes from the sponsor–club recommendation system. The hypothetical fee and the brand-attributable exposure share must still be entered separately. Recommendation and ROI datasets may refer to different reference periods.'))
    simulated_club = roi.loc[roi['club_name'].astype(str) == simulated_club_name].iloc[0]
    social_value = pd.to_numeric(simulated_club['social_media_value_eur_m'], errors='coerce')
    tv_value = pd.to_numeric(simulated_club['tv_media_value_eur_m'], errors='coerce')
    if pd.isna(social_value) or pd.isna(tv_value):
        st.warning(tr('Social or TV media-value data are unavailable for the selected club.'))
    else:
        total_club_media_value = float(social_value) + float(tv_value)
        input_col1, input_col2 = st.columns(2)
        with input_col1:
            sponsor_fee_eur_m = st.number_input(tr('Hypothetical sponsorship fee (€m)'), min_value=0.01, value=1.0, step=0.25, format='%.2f', key='brand_roi_simulator_fee')
        with input_col2:
            brand_exposure_share_pct = st.slider(tr('Hypothetical share of club media value attributable to the brand (%)'), min_value=0, max_value=100, value=5, step=1, key='brand_roi_simulator_share')
        st.caption(tr('The initial fee (€1m) and exposure share (5%) are illustrative starting values, not observed contract terms. Adjust both inputs to explore your own scenario.'))
        st.info(tr("**Reference period:** The club media-value inputs refer to the project's 2024/25 competition dataset, with social fanbase inputs drawn from a 2025 snapshot. For a same-period scenario, enter a hypothetical sponsorship fee for one comparable season and an exposure share referring to that same season. If you know only a multi-year contract fee, do not compare its full value with a single season of media value. This scenario does **not** forecast next season's ROI or a realized financial return."))
        brand_media_value_eur_m = total_club_media_value * brand_exposure_share_pct / 100
        brand_roi_proxy_pct = (brand_media_value_eur_m - sponsor_fee_eur_m) / sponsor_fee_eur_m * 100
        media_cost_coverage_pct = brand_media_value_eur_m / sponsor_fee_eur_m * 100
        st.divider()
        st.subheader(tr(f'Scenario Results — {simulated_club_name}'))
        st.markdown(tr('#### Estimated media value'))
        result_col1, result_col2 = st.columns(2)
        with result_col1:
            st.metric(tr('Club Social + TV media value'), tr(f'€{total_club_media_value:.2f}m'))
        with result_col2:
            st.metric(tr('Media value attributed to brand'), tr(f'€{brand_media_value_eur_m:.2f}m'))
        st.markdown(tr('#### Sponsorship investment and return'))
        result_col3, result_col4 = st.columns(2)
        with result_col3:
            st.metric(tr('Hypothetical sponsorship fee'), tr(f'€{sponsor_fee_eur_m:.2f}m'))
        with result_col4:
            st.metric(tr('Brand media-value ROI proxy'), tr(f'{brand_roi_proxy_pct:.2f}%'))
        st.metric(tr('Media-value coverage of hypothetical fee'), tr(f'{media_cost_coverage_pct:.2f}%'))
        st.divider()
        st.subheader(tr('Brand ROI — Sensitivity Analysis'))
        st.write(tr("How the brand's hypothetical media-value ROI varies with its assumed share of club media value. The club and hypothetical same-season fee remain fixed."))
        sensitivity_shares = sorted(set([0, 1, 5, 10, 25, 50, 100, brand_exposure_share_pct]))
        sensitivity_rows = []
        for share_pct in sensitivity_shares:
            attributed_value = total_club_media_value * share_pct / 100
            scenario_roi_pct = (attributed_value - sponsor_fee_eur_m) / sponsor_fee_eur_m * 100
            sensitivity_rows.append({tr('Scenario'): tr('Current selection') if share_pct == brand_exposure_share_pct else tr('Alternative'), tr('Exposure share (%)'): share_pct, tr('Brand media value (€m)'): round(attributed_value, 4), tr('Hypothetical fee (€m)'): round(sponsor_fee_eur_m, 4), tr('Brand ROI proxy (%)'): round(scenario_roi_pct, 2)})
        sensitivity_df = pd.DataFrame(sensitivity_rows)
        st.dataframe(sensitivity_df, width='stretch', hide_index=True)
        st.caption(tr('Illustrative scenarios only. The fee and club-level media value remain fixed; only the assumed share attributable to the brand changes. The ROI is a media-value proxy, not a future or realized return.'))
        st.divider()
        st.subheader(tr('Media-Value Break-Even'))
        if total_club_media_value > 0:
            required_share_pct = sponsor_fee_eur_m / total_club_media_value * 100
            if required_share_pct <= 100:
                st.write(tr(f"Under the current assumptions, the brand would need to receive approximately **{required_share_pct:.2f}%** of the club's estimated Social + TV media value for that media value to equal the hypothetical sponsorship fee."))
            else:
                st.write(tr("Under the current assumptions, even attributing **100% of the club's estimated Social + TV media value** to the brand would not cover the hypothetical sponsorship fee."))
        with st.expander(tr('How is the brand ROI scenario calculated?')):
            st.latex('V_{\\mathrm{brand}} = (V_{\\mathrm{Social}} + V_{\\mathrm{TV}})\\times \\frac{q}{100}')
            st.latex('ROI_{\\mathrm{brand}}^{\\mathrm{proxy}} = \\frac{V_{\\mathrm{brand}}-C_{\\mathrm{sponsor}}}{C_{\\mathrm{sponsor}}}\\times100')
            st.write(tr('Here, q is the hypothetical percentage of club-level media value attributed to the brand, and C is the hypothetical fee paid by that brand.'))
            st.write(tr('The model does not estimate brand-specific exposure shares or actual contract prices. The scenario therefore depends on the assumptions selected by the user.'))
            st.write(tr('Media-equivalent value is not incremental revenue or profit. This proxy excludes other potential sponsorship benefits, such as sales effects, hospitality, licensing and brand activation.'))
    st.divider()
    st.subheader(tr('Club-Level Media-Value Benchmark'))
    st.write(tr('The following tables and charts compare **aggregate club-level Social + TV media value** with a model-predicted sponsorship reference. This is a benchmark for exploring clubs; it is **not a brand-specific contract ROI**.'))
    st.caption(tr('The benchmark can use different TV audience methodologies across leagues. A negative ROI proxy means that the measured media-equivalent value is below the hypothetical reference amount; it does not demonstrate a realized financial loss.'))
    st.subheader(tr('ROI Data Availability'))
    ROI_METRICS = {'total_roi_proxy_pct': 'Total ROI proxy (%) — original field', 'total_roi_proxy_base_pct': 'Total ROI proxy (%) — base scenario', 'total_roi_pct': 'Social + TV media-value ROI proxy (%) — all 96 clubs', 'social_roi_proxy_pct': 'Social ROI proxy (%) — social only', 'social_roi_pct': 'Social ROI (%) — alternative social field'}
    roi_working = roi.copy()
    available_metric_columns = [col for col in ROI_METRICS if col in roi_working.columns]
    for col in available_metric_columns:
        roi_working[col] = pd.to_numeric(roi_working[col], errors='coerce')
    coverage_records = []
    for col in available_metric_columns:
        available_count = int(roi_working[col].notna().sum())
        total_clubs = len(roi_working)
        coverage_records.append({tr('ROI field'): col, tr('Indicator'): tr(ROI_METRICS[col]), tr('Clubs with data'): available_count, tr('Clubs without data'): total_clubs - available_count, tr('Coverage (%)'): round(100 * available_count / total_clubs, 1) if total_clubs > 0 else 0.0})
    coverage_audit = pd.DataFrame(coverage_records)
    if coverage_audit.empty:
        st.error(tr('No recognized ROI percentage fields were found in the dataset.'))
    else:
        st.dataframe(coverage_audit, width='stretch', hide_index=True)
        st.caption(tr('Coverage is calculated separately for each original CSV field. Different ROI definitions are not automatically combined.'))
    total_roi_candidates = [col for col in ['total_roi_proxy_pct', 'total_roi_proxy_base_pct', 'total_roi_pct'] if col in roi_working.columns and roi_working[col].notna().any()]
    if not total_roi_candidates:
        st.warning(tr('No available total ROI percentage field was found in the master dataset.'))
        selected_roi_col = None
    else:
        default_roi_col = 'total_roi_pct' if 'total_roi_pct' in total_roi_candidates else max(total_roi_candidates, key=lambda col: roi_working[col].notna().sum())
        selected_roi_col = st.selectbox(tr('Select ROI indicator'), options=total_roi_candidates, index=total_roi_candidates.index(default_roi_col), format_func=lambda col: tr(ROI_METRICS[col]), key='roi_metric_selector')
        st.info(tr(f'Currently displaying the original CSV field: `{selected_roi_col}`. Missing values remain missing; no estimates are generated to fill them.'))
    st.divider()
    st.subheader(tr('Club Coverage'))
    roi_leagues = sorted(roi_working['league_final'].dropna().unique().tolist())
    selected_roi_leagues = st.multiselect(tr('Select leagues'), options=roi_leagues, default=roi_leagues, key='roi_leagues_revised')
    filtered_roi = roi_working.loc[roi_working['league_final'].isin(selected_roi_leagues)].copy()
    n_clubs = len(filtered_roi)
    n_sponsorship = int(filtered_roi['predicted_sponsorship_eur_m'].notna().sum())
    if selected_roi_col is not None:
        n_roi = int(filtered_roi[selected_roi_col].notna().sum())
    else:
        n_roi = 0
    roi_coverage = 100 * n_roi / n_clubs if n_clubs > 0 else 0
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(tr('Clubs in selected leagues'), tr(n_clubs))
    col2.metric(tr('Sponsorship estimates available'), tr(n_sponsorship))
    col3.metric(tr('Selected ROI values available'), tr(n_roi))
    col4.metric(tr('Selected ROI coverage'), tr(f'{roi_coverage:.1f}%'))
    if filtered_roi.empty:
        st.info(tr('Select at least one league to display results.'))
    else:
        st.subheader(tr('ROI Coverage by League'))
        league_coverage = filtered_roi.groupby('league_final').agg(clubs=('club_name', 'size'), sponsorship_available=('predicted_sponsorship_eur_m', 'count')).reset_index()
        if selected_roi_col is not None:
            roi_counts = filtered_roi.groupby('league_final')[selected_roi_col].count()
            league_coverage['roi_available'] = league_coverage['league_final'].map(roi_counts).astype(int)
            league_coverage['roi_coverage_pct'] = (100 * league_coverage['roi_available'] / league_coverage['clubs']).round(1)
        st.dataframe(league_coverage.rename(columns=tr_dict({'league_final': 'League', 'clubs': 'Clubs', 'sponsorship_available': 'Sponsorship estimates', 'roi_available': 'Available ROI values', 'roi_coverage_pct': 'ROI coverage (%)'})), width='stretch', hide_index=True)
        st.divider()
        st.subheader(tr('TV Audience — Data Methodology'))
        tv_method_counts = filtered_roi['tv_methodology'].fillna(tr('Methodology not specified')).value_counts().rename_axis(tr('TV methodology')).reset_index(name=tr('Clubs'))
        st.dataframe(tv_method_counts, width='stretch', hide_index=True)
        observed_tv_count = int(filtered_roi['tv_audience_fully_observed'].astype(str).str.strip().str.lower().eq('true').sum())
        st.caption(tr(f'Fully observed TV audience: {observed_tv_count}/{len(filtered_roi)} clubs in the selected leagues. Other TV audience values use proxy-based methodologies. The ROI indicator combines these different data sources and should not be interpreted as a realized financial return.'))
        st.divider()
        st.subheader(tr('Club-Level Results'))
        display_columns = ['club_name', 'league_final', 'predicted_sponsorship_eur_m']
        if 'total_media_value_eur_m' in filtered_roi.columns:
            display_columns.append('total_media_value_eur_m')
        if selected_roi_col is not None:
            display_columns.append(selected_roi_col)
        column_names = {'club_name': 'Club', 'league_final': 'League', 'predicted_sponsorship_eur_m': 'Predicted sponsorship (€m)', 'total_media_value_eur_m': 'Estimated Social + TV value (€m)'}
        if selected_roi_col is not None:
            column_names[selected_roi_col] = ROI_METRICS[selected_roi_col]
        roi_display = filtered_roi[display_columns].rename(columns=tr_dict(column_names))
        st.dataframe(roi_display, width='stretch', hide_index=True)
        st.download_button(label=tr('Download displayed ROI results (CSV)'), data=roi_display.to_csv(index=False).encode('utf-8-sig'), file_name='roi_dashboard_results.csv', mime='text/csv')
        if selected_roi_col is not None:
            missing_roi_clubs = filtered_roi.loc[filtered_roi[selected_roi_col].isna(), ['club_name', 'league_final']]
            with st.expander(tr(f'Clubs without a value in the selected ROI field ({len(missing_roi_clubs)})')):
                if missing_roi_clubs.empty:
                    st.success(tr('No missing values in this field for the selected leagues.'))
                else:
                    st.dataframe(missing_roi_clubs.rename(columns=tr_dict({'club_name': 'Club', 'league_final': 'League'})), width='stretch', hide_index=True)
        if selected_roi_col is not None:
            chart_data = filtered_roi.dropna(subset=[selected_roi_col]).sort_values(selected_roi_col, ascending=False).head(20).copy()
            if not chart_data.empty:
                st.divider()
                st.subheader(tr('ROI Comparison — Available Clubs'))
                roi_chart = px.bar(chart_data.sort_values(selected_roi_col), x=selected_roi_col, y='club_name', orientation='h', color='league_final', labels=tr_dict({selected_roi_col: ROI_METRICS[selected_roi_col], 'club_name': 'Club', 'league_final': 'League'}))
                roi_chart.update_layout(height=max(450, len(chart_data) * 30), yaxis_title=None)
                st.plotly_chart(roi_chart, width='stretch')
                st.caption(tr('Only clubs with an available value in the selected ROI field are plotted. Missing values are excluded rather than treated as zero.'))
        if 'total_media_value_eur_m' in filtered_roi.columns:
            scatter_data = filtered_roi.dropna(subset=['predicted_sponsorship_eur_m', 'total_media_value_eur_m'])
            if not scatter_data.empty:
                st.divider()
                st.subheader(tr('Media Value vs Predicted Sponsorship'))
                media_chart = px.scatter(scatter_data, x='predicted_sponsorship_eur_m', y='total_media_value_eur_m', color='league_final', hover_name='club_name', labels=tr_dict({'predicted_sponsorship_eur_m': 'Predicted sponsorship (€m)', 'total_media_value_eur_m': 'Estimated Social + TV value (€m)', 'league_final': 'League'}))
                media_chart.update_layout(height=500)
                st.plotly_chart(media_chart, width='stretch')
                st.caption(tr('The chart includes only records with both variables available. Media value may incorporate modeled audiences and advertising-equivalent assumptions.'))
    st.divider()
    with st.expander(tr('ROI Methodology and Interpretation')):
        st.write(tr('The dataset contains multiple ROI-related fields, including total ROI, base-scenario ROI and social-only ROI. These are displayed as separate indicators and are not merged without a dedicated methodology audit.'))
        st.write(tr('An advertising-equivalent media value is not the same as incremental revenue or profit. The predicted sponsorship value is also not necessarily the price of an actual contract.'))
        st.write(tr("The 2024/25 competition universe and the reference period of the model's sponsorship estimates must be distinguished when interpreting the results."))
with quality_tab:
    st.header(tr('Model & Data Quality'))
    st.subheader(tr('Temporal predictive validation — 2023/24'))
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(tr('High-quality test observations'), tr('16'))
    col2.metric(tr('MAE'), tr('€35.47m'))
    col3.metric(tr('RMSE'), tr('€45.48m'))
    col4.metric(tr('R²'), tr('0.747'))
    st.caption(tr('XGBoost Model B Original. Validation statistics refer to the 16 high-quality observations in the 2023/24 temporal test, not all 96 clubs in the scoring universe.'))
    st.divider()
    st.subheader(tr('Coverage and scoring readiness'))
    col1, col2, col3 = st.columns(3)
    col1.metric(tr('SVI scoring coverage'), tr('96 / 96'))
    col2.metric(tr('ROI club coverage'), tr('96 / 96'))
    col3.metric(tr('Model feature completeness'), tr('100%'))
    st.caption(tr('Feature completeness refers to the 40 numeric model inputs after data preparation. It does not establish 100% completeness of raw source data.'))
    st.divider()
    st.subheader(tr('Ranking stability — exploratory'))
    col1, col2, col3 = st.columns(3)
    col1.metric(tr('Spearman correlation'), tr('0.8839'))
    col2.metric(tr('Mean absolute rank change'), tr('3.07 positions'))
    col3.metric(tr('Top 10 retention'), tr('70%'))
    st.info(tr('These exploratory results compare the 30 clubs common to the historical 2023/24 Model B ranking and the subsequent 2025 SVI output. They are not yet a certified consecutive-season stability KPI for the complete Big Five universe.'))
st.divider()
st.caption(tr('SBL Consultancy | Sponsorship Value Index Predictor | Model estimates and proxy-based analyses'))