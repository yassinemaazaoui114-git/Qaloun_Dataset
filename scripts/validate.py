#!/usr/bin/env python3
"""
Structural validator for the Qaloon Quran dataset.

Runs BEFORE human review — catches bookkeeping mistakes for free, so the
human verification pass can focus entirely on word-level/diacritic accuracy
(the thing only a person can actually check).

Deliberately does NOT need any external "ayah count per surah" table.
Qaloon uses the Madani First Count, a different ayah-counting tradition
from the generic (Kufi) tables most Quran datasets ship with -- using the
wrong one would silently validate against wrong numbers. Instead, each
surah's true ayah count is read directly from that surah's own
`surah_header` row (`ayah_count`), which comes straight from the printed
banner in the mushaf itself. Self-contained, no external dependency.

Usage:
    python3 validate.py data/quran_layout.jsonl data/quran_words.jsonl

IMPORTANT: run this against the CUMULATIVE master files (after merging a
newly-verified batch in), not an isolated batch's draft file alone.
Ayah/line continuity checks assume everything before the current batch is
already present -- run on just one batch and you'll get false "gap" errors
for ayahs that earlier, already-verified batches covered.
"""
import sys
import json
from collections import defaultdict


def load_jsonl(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"  MALFORMED JSON at {path}:{i}: {e}")
    return rows


def validate(layout_rows, word_rows):
    errors = []
    words_by_id = {w["id"]: w for w in word_rows}

    # --- 1. Page/line sequencing ---
    by_page = defaultdict(list)
    for row in layout_rows:
        by_page[row["page"]].append(row)

    for page, rows in sorted(by_page.items()):
        rows_sorted = sorted(rows, key=lambda r: r["line"])
        expected_line = 1
        for row in rows_sorted:
            if row["line"] != expected_line:
                errors.append(
                    f"page {page}: expected line {expected_line}, "
                    f"got line {row['line']} (gap or duplicate)"
                )
            expected_line = row["line"] + 1

    # --- 2. Ayah continuity + per-surah count, using each surah's own
    #        printed ayah_count (from its surah_header row) as the target ---
    surah_declared_count = {}
    for row in layout_rows:
        if row["type"] == "surah_header":
            surah_declared_count[row["surah"]] = row["ayah_count"]

    ayah_max_position = defaultdict(int)  # (surah, ayah) -> max position seen
    surah_max_ayah = defaultdict(int)     # surah -> max ayah number seen

    words_sorted = sorted(word_rows, key=lambda w: w["id"])
    for w in words_sorted:
        key = (w["surah"], w["ayah"])
        if w["position"] != ayah_max_position[key] + 1:
            errors.append(
                f"surah {w['surah']} ayah {w['ayah']}: word position "
                f"{w['position']} out of sequence (expected "
                f"{ayah_max_position[key] + 1})"
            )
        ayah_max_position[key] = max(ayah_max_position[key], w["position"])
        surah_max_ayah[w["surah"]] = max(surah_max_ayah[w["surah"]], w["ayah"])

    # ayah numbers within a surah must be gapless 1..N up to whatever we've
    # transcribed so far (can't check the final total until the whole surah
    # is in, but we CAN check no ayah number is skipped along the way)
    for surah, max_ayah in surah_max_ayah.items():
        seen_ayahs = {w["ayah"] for w in word_rows if w["surah"] == surah}
        expected = set(range(1, max_ayah + 1))
        missing = expected - seen_ayahs
        if missing:
            errors.append(
                f"surah {surah}: ayah number(s) {sorted(missing)} never "
                f"appear, but ayah {max_ayah} does (gap)"
            )
        declared = surah_declared_count.get(surah)
        if declared is not None and max_ayah > declared:
            errors.append(
                f"surah {surah}: transcribed ayah {max_ayah}, but its own "
                f"surah_header banner declares only {declared} ayahs total"
            )

    # --- 3. Every word_id referenced by a layout row must exist ---
    for row in layout_rows:
        if row["type"] != "ayah_line":
            continue
        for key in ("first_word_id", "last_word_id"):
            wid = row.get(key)
            if wid is not None and wid not in words_by_id:
                errors.append(
                    f"page {row['page']} line {row['line']}: {key}={wid} "
                    f"not found in quran_words"
                )

    return errors


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    layout_rows = load_jsonl(sys.argv[1])
    word_rows = load_jsonl(sys.argv[2])
    errors = validate(layout_rows, word_rows)
    if errors:
        print(f"{len(errors)} structural issue(s) found:\n")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"OK — {len(layout_rows)} layout rows, {len(word_rows)} words, "
              f"no structural issues.")
        sys.exit(0)


if __name__ == "__main__":
    main()
