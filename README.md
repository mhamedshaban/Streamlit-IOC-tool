# IOC Automation Tool (Streamlit)

**Prepared by:** Mohammed Shaaban  
**Date:** 10/1/2025

## Overview
This Streamlit app extracts IOCs (IPs, Domains, Hashes) from Excel files and exports them to text files. It is intended to run locally on each team member's machine.

---

## Files
- `ioc_app.py` — main Streamlit application
- `requirements.txt` — Python dependencies
- `start.bat` — Windows helper to start the app (optional)
- `data/sample_ioc.xlsx` — sample data (optional)
- `.env` — (NOT in repo) place your API keys here if used

---

## Quick Local Install (Windows)

1. Clone the repo:
```bash
git clone https://github.com/YOUR_USERNAME/REPO_NAME.git
cd REPO_NAME

2. Create virtual environment:

powershell

py -m venv .venv
.\.venv\Scripts\activate

3. Install dependencies:

powershell

pip install -r requirements.txt

4. (Optional) Add API key:
Create a file .env in the project root:

ini

GOOGLE_API_KEY=your_api_key_here
(Do NOT commit .env to Git.)

5. Run the app:

powershell

streamlit run ioc_app.py

6. Open in browser:

arduino

http://localhost:8501
