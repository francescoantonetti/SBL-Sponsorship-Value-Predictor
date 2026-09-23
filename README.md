# SBL Consultancy — Sponsorship Value Index Predictor

Streamlit dashboard with branded UI, sponsor-club recommendation, hypothetical brand ROI simulator, exposure-share sensitivity table, and explicit reference-period note.

## Required files for deployment

The 4 CSVs are intentionally NOT bundled; retrieve them from your local project and ensure you are authorized to publish them. Place all four under `data/final/` as listed in `data/final/INSERISCI_QUI_I_4_CSV.txt`. All four are required at runtime. If public release of the data is not permitted, do not upload them to a public GitHub repository; evaluate private deployment and data governance first.

## Run locally

From repository root: `python3 -m pip install -r requirements.txt` then `python3 -m streamlit run dashboard/app.py`.

## Deploy

Push this folder, its four authorized CSVs, and all files to a GitHub repository. In Streamlit Community Cloud, select the repository, the correct branch, and `dashboard/app.py` as the entrypoint. `requirements.txt` lives at repository root. Choose a privacy setting consistent with data sharing permissions. Never commit secrets.

If replacing an existing GitHub app, preserve any newer changes in its `dashboard/app.py` before overwriting; compare versions first.
