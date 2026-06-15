# centralplanning.bat

Launcher on the Desktop (`C:\Users\spatt\Desktop\centralplanning.bat`) that activates the `RemarkableExploit` conda environment and prompts which feature(s) to run.

## Usage

Double-click `centralplanning.bat`. At the prompt:

| Input | Action |
|-------|--------|
| Enter | Remarkable + Audio (both) |
| `1`   | Remarkable only (`automate_remarkable.py`) |
| `2`   | Audio only (`sync_and_transcribe.py`) |

## Scripts

- **`automate_remarkable.py`** — GUI automation for the Remarkable app; searches for "exploit" text and copies it to output files.
- **`sync_and_transcribe.py`** — Fetches unprocessed audio recordings from the Neon database, transcribes them via Mistral Voxtral, and writes markdown transcripts to `processed/`.
