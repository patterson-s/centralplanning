import os
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()

OUTPUT_DIR = r"C:\Users\spatt\Desktop\RemarkableExploit\processed"
LANGUAGE_NAMES = {"en": "English", "fr": "French", "de": "German"}


def get_next_n(date_str: str) -> int:
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    nums = [int(p.stem.rsplit("_", 1)[-1]) for p in Path(OUTPUT_DIR).glob(f"transcript_{date_str}_*.md")]
    return max(nums, default=0) + 1


def transcribe(client: Mistral, audio_bytes: bytes, filename: str, language: str) -> str:
    response = client.audio.transcriptions.complete(
        model="voxtral-mini-latest",
        file={"content": audio_bytes, "file_name": filename},
        language=language,
    )
    return response.text.strip()


def write_transcript(rows: list[dict], context_text: str) -> str:
    today = datetime.now().strftime("%Y%m%d")
    n = get_next_n(today)
    filename = f"transcript_{today}_{n}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    lines = []
    if len(rows) == 1 and not context_text:
        ts = rows[0]["created_at"].astimezone().strftime("%Y-%m-%d %H:%M:%S")
        lang_name = LANGUAGE_NAMES.get(rows[0]["language"], rows[0]["language"])
        lines.append(f"# Transcript - {ts}")
        lines.append("")
        lines.append(f"Language: {lang_name}")
        lines.append("")
        lines.append(rows[0]["transcription"])
    else:
        date_str = rows[0]["created_at"].astimezone().strftime("%Y-%m-%d")
        lines.append(f"# Transcript - {date_str}")
        lines.append("")
        if context_text:
            lines.append(f"Context: {context_text}")
            lines.append("")
        for i, row in enumerate(rows, start=1):
            ts = row["created_at"].astimezone().strftime("%Y-%m-%d %H:%M:%S")
            lang_name = LANGUAGE_NAMES.get(row["language"], row["language"])
            lines.append(f"## Recording {i} - {ts}")
            lines.append(f"Language: {lang_name}")
            lines.append("")
            lines.append(row["transcription"])
            lines.append("")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")

    return filepath


def main() -> None:
    neon_url = os.environ["NEON_DATABASE_URL"]
    mistral_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=mistral_key)

    conn = psycopg2.connect(neon_url)
    conn.autocommit = False
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute(
        "SELECT id, created_at, context_text, language, audio_data, audio_filename "
        "FROM audio_recordings WHERE processed = FALSE ORDER BY created_at"
    )
    rows = cur.fetchall()

    if not rows:
        print("No new recordings.")
        cur.close()
        conn.close()
        return

    print(f"Found {len(rows)} unprocessed recording(s).")

    groups: dict[str, list[dict]] = defaultdict(list)
    standalone: list[dict] = []

    for row in rows:
        ctx = (row["context_text"] or "").strip()
        if ctx:
            groups[ctx].append(dict(row))
        else:
            standalone.append(dict(row))

    all_groups = list(groups.items()) + [("", [r]) for r in standalone]
    all_processed_ids: list[int] = []

    for ctx, group_rows in all_groups:
        for row in group_rows:
            print(f"  Transcribing {row['audio_filename']} ({row['language']})…")
            row["transcription"] = transcribe(
                client,
                bytes(row["audio_data"]),
                row["audio_filename"],
                row["language"],
            )
        filepath = write_transcript(group_rows, ctx)
        print(f"  → {filepath}")
        all_processed_ids.extend(r["id"] for r in group_rows)

    if all_processed_ids:
        cur.execute(
            "UPDATE audio_recordings SET processed = TRUE WHERE id = ANY(%s)",
            (all_processed_ids,),
        )
        conn.commit()

    cur.close()
    conn.close()
    print("Done.")


if __name__ == "__main__":
    main()
