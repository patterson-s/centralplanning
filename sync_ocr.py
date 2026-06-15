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


def get_next_n(date_str: str) -> int:
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    nums = [int(p.stem.rsplit("_", 1)[-1]) for p in Path(OUTPUT_DIR).glob(f"ocr_{date_str}_*.md")]
    return max(nums, default=0) + 1


def run_ocr(client: Mistral, image_bytes: bytes, filename: str) -> str:
    uploaded = client.files.upload(
        file={"file_name": filename, "content": image_bytes},
        purpose="ocr",
    )
    signed = client.files.get_signed_url(file_id=uploaded.id, expiry=1)
    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={"type": "document_url", "document_url": signed.url},
    )
    return "\n\n".join(p.markdown for p in ocr_response.pages).strip()


def write_ocr(rows: list[dict], context_text: str) -> str:
    today = datetime.now().strftime("%Y%m%d")
    n = get_next_n(today)
    filename = f"ocr_{today}_{n}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    lines = []
    if len(rows) == 1 and not context_text:
        ts = rows[0]["created_at"].astimezone().strftime("%Y-%m-%d %H:%M:%S")
        lines.append(f"# OCR - {ts}")
        lines.append("")
        lines.append(rows[0]["ocr_text"])
    else:
        date_str = rows[0]["created_at"].astimezone().strftime("%Y-%m-%d")
        lines.append(f"# OCR - {date_str}")
        lines.append("")
        if context_text:
            lines.append(f"Context: {context_text}")
            lines.append("")
        for i, row in enumerate(rows, start=1):
            ts = row["created_at"].astimezone().strftime("%Y-%m-%d %H:%M:%S")
            lines.append(f"## Photo {i} - {ts}")
            lines.append("")
            lines.append(row["ocr_text"])
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
        "SELECT id, created_at, context_text, image_data, image_filename "
        "FROM ocr_photos WHERE processed = FALSE ORDER BY created_at"
    )
    rows = cur.fetchall()

    if not rows:
        print("No new photos.")
        cur.close()
        conn.close()
        return

    print(f"Found {len(rows)} unprocessed photo(s).")

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
            print(f"  OCR: {row['image_filename']}…")
            row["ocr_text"] = run_ocr(client, bytes(row["image_data"]), row["image_filename"])
        filepath = write_ocr(group_rows, ctx)
        print(f"  → {filepath}")
        all_processed_ids.extend(r["id"] for r in group_rows)

    if all_processed_ids:
        cur.execute(
            "UPDATE ocr_photos SET processed = TRUE WHERE id = ANY(%s)",
            (all_processed_ids,),
        )
        conn.commit()

    cur.close()
    conn.close()
    print("Done.")


if __name__ == "__main__":
    main()
