# DGDM Rule Tracker

A daily pharma data quality rule tracking app built with Streamlit.

## Features
- 20 priority rules ranked by patient safety & regulatory impact
- Daily checkbox tracking with timestamps
- Notes field per rule to capture inconsistencies found
- Filter by day, priority
- Export today's tasks or full history as CSV
- Data persists locally in `tracker_data.json`

## How to run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## How to deploy on Streamlit Cloud (free)

1. **Push to GitHub**
   - Create a new repo on github.com (e.g. `dgdm-tracker`)
   - Upload all files: `app.py`, `requirements.txt`, `.streamlit/config.toml`, `README.md`

2. **Deploy on Streamlit Community Cloud**
   - Go to https://share.streamlit.io
   - Sign in with your GitHub account
   - Click **New app**
   - Select your repo, branch (`main`), and set Main file path to `app.py`
   - Click **Deploy**
   - Your app will be live at `https://<your-app-name>.streamlit.app`

3. **Persistent data note**
   - On Streamlit Cloud, `tracker_data.json` resets on each redeploy.
   - Use the **Export full history** button regularly to save your CSV locally.
   - For true persistence, replace the JSON file with a Google Sheet or Supabase (free tier) — ask for help if needed.

## File structure

```
dgdm-tracker/
├── app.py                  # Main application
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml         # Theme configuration
└── README.md               # This file
```
