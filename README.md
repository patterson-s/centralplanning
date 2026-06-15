# RemarkableExploit

Two tools for capturing and processing notes:

1. **Remarkable automation** — extracts exploit content from the Remarkable desktop app and saves it as markdown.
2. **Voice notes** — records audio notes on your phone, stores them in a Neon database, and transcribes them to your PC using Mistral's Voxtral model.

---

## Setup

```bash
pip install -r requirements.txt
```

Copy `.env` and fill in your API keys:
```
NEON_DATABASE_URL=postgresql://...
MISTRAL_API_KEY=your_key_here
```

---

## Voice Notes

### Phone interface (`phone_app.py`)

A Streamlit app deployed to [Streamlit Community Cloud](https://share.streamlit.io) for HTTPS access from any device.

- **Language toggle** — cycles English → Français → Deutsch
- **Context box** — optional label that groups related recordings together; persists between recordings until manually cleared
- **Record button** — tap to record, tap again to stop; audio uploads automatically to Neon DB

To run locally:
```bash
streamlit run phone_app.py
```

For local dev, add your Neon connection string to `.streamlit/secrets.toml`:
```toml
NEON_DATABASE_URL = "postgresql://..."
```

### PC sync & transcription (`sync_and_transcribe.py`)

Run on your PC to pull new recordings from Neon, transcribe them with Voxtral, and write markdown files to `processed/`.

```bash
python sync_and_transcribe.py
```

Recordings that share the same context label are grouped into a single output file. Recordings with no context each get their own file.

**Output format:** `processed/transcript_YYYYMMDD_n.md`

---

## Remarkable Automation

- Double-click `re_run.bat` on the desktop to run the script.
- Opens the Remarkable app, searches for "exploit", copies the content, and saves it to `processed/`.

**Output format:** `processed/file_YYYYMMDD_n.md`

---

## Files

| File | Purpose |
|---|---|
| `phone_app.py` | Streamlit phone interface for recording voice notes |
| `sync_and_transcribe.py` | PC script: pull from Neon DB, transcribe, save to `processed/` |
| `automate_remarkable.py` | Remarkable desktop automation |
| `requirements.txt` | Python dependencies |
| `.env` | API keys (gitignored) |
| `.streamlit/secrets.toml` | Streamlit local dev secrets (gitignored) |
