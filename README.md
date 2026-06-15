# RemarkableExploit

Automates interaction with the Remarkable desktop application to extract and save exploits as markdown files.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure Remarkable is installed on the system.

## Usage
- Double-click `re_run.bat` on the desktop to execute the script.
- The script performs the following actions:
  1. Opens the Remarkable app via Windows search.
  2. Searches for "exploit" in the app.
  3. Selects and copies exploit content.
  4. Saves the copied content as a markdown file in `processed/`.

## Output
- Files are saved in `C:\Users\spatt\Desktop\RemarkableExploit\processed` as `file_YYYYMMDD_n.md`.
- Each file contains the date and the copied exploit content.

## Files
- `automate_remarkable.py`: Main automation script.
- `re_run.bat`: Batch file to run the script with the correct Conda environment.
- `requirements.txt`: Python dependencies.
