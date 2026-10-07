# 📄 ATS Resume Checker

A Streamlit app that scores a resume for Applicant Tracking System (ATS) compatibility and gives specific, prioritized improvements. Powered by Google's Gemini Flash model.

## Features
- Upload resume as **PDF, DOCX or TXT**
- Optional **job description** for keyword matching
- Overall **ATS score (0–100)** + breakdown: keywords, content impact, formatting, structure, readability
- Strengths, missing keywords, and prioritized fixes with example rewrites
- Download the report as JSON

## Run locally
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
Get a free API key at https://aistudio.google.com/apikey and paste it in the sidebar, or set it as an environment variable:
```bash
export GEMINI_API_KEY="your-key"     # Windows PowerShell: $env:GEMINI_API_KEY="your-key"
```
Optional: set `GEMINI_MODEL` to change the model (default `gemini-2.5-flash`; falls back to `gemini-flash-latest`).

---

## Push to GitHub (using the website, no Git needed)
1. Sign in at https://github.com and click **+ → New repository**.
2. Name it (e.g. `ats-resume-checker`), choose **Public** (required for free Streamlit hosting of public apps; private also works if you grant access), and click **Create repository**.
3. On the new repo page click **uploading an existing file**.
4. Drag in `app.py`, `requirements.txt`, and `README.md` (keep them in the repo root, not inside a folder).
5. Click **Commit changes**.
6. **Never upload your API key.** To be safe, click **Add file → Create new file**, name it `.gitignore`, paste the lines below, and commit:
   ```
   .streamlit/secrets.toml
   venv/
   __pycache__/
   .env
   ```

## Deploy on Streamlit Community Cloud
1. Go to https://share.streamlit.io and sign in with GitHub (authorize access to your repo when asked).
2. Click **Create app** → **Deploy a public app from GitHub**.
3. Choose your **Repository**, **Branch** (`main`), and **Main file path**: `app.py`.
4. Open **Advanced settings → Secrets** and paste:
   ```toml
   GEMINI_API_KEY = "your-gemini-api-key"
   ```
   (Optional: `GEMINI_MODEL = "gemini-2.5-flash"`)
5. Click **Deploy**. After a minute or two you get a public URL like `https://your-app.streamlit.app`.

To update the app later: edit a file on GitHub and commit; Streamlit redeploys automatically. To change secrets: app **⋮ → Settings → Secrets**.

## Troubleshooting
| Problem | Fix |
|---|---|
| "Very little text was found" | PDF is a scanned image. Export a text-based PDF or use DOCX. |
| `ModuleNotFoundError` on deploy | Make sure `requirements.txt` is in the repo root. |
| Model not found / 404 | Set `GEMINI_MODEL` to a current Flash model name from https://ai.google.dev/gemini-api/docs/models |
| Quota / 429 error | Free-tier rate limit hit; wait a minute or enable billing. |

## Privacy
The resume text is sent to the Gemini API for analysis. The app does not store files or results on any server.

## Disclaimer
The score is an AI-generated estimate, not the output of any real employer's ATS. Use it as guidance.
