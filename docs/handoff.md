# Handoff — Qaloon Quran Dataset

> Read this first if you're picking this project up cold (a new conversation, another AI tool, or the user returning after a gap). For full decision history and rationale, see `docs/spec.md`.

**As of:** 2026-10-01 (end of session — see `docs/sessions/2026-10-01.md`)

## What's done

- Project scoped: textual, layout-faithful Qaloon dataset from the Tunisian Mushaf Al-Mu'allim; app/model are future, separate phases.
- Schema final (two tables, `quran_layout` + `quran_words`), documented in `schema.md` including transcription conventions (Latin-digit ayah markers `﴿N﴾`, tajwid colors ignored, tajwid marks kept, standalone waqf tokens dropped from the words table).
- Repo scaffolded, validator built (`scripts/validate.py`), symbols glossary started (`docs/symbols_glossary.md`: waqf signs م ۘ, ج ۚ, صلى ۖ, قلى ۗ, ∴ ۛ).
- Batch 1 (pilot, printed pages 2–11) source received as a 10-page PDF. PDF page N = printed page N+1.
- **Printed page 2 is transcribed (draft), NOT verified.** Files in `data/drafts/`: `page_0002_layout.jsonl`, `page_0002_words.jsonl`, `page_0002_review.md`. 14 lines, 61 words, validator passes.

## What's in progress

- User's word-by-word verification of page 2 against the image. Until they report errors or say "verified", page 2 stays `transcribed_unverified` in `data/manifest.json`.

## Rules to remember

- No new page/batch starts until the previous one is verified.
- Gray or colored letters are tajwid coloring: transcribe as black. Tajwid marks stay.
- Never validate against Hafs/Kufi ayah tables; Qaloon uses the Madani First Count. The validator uses each surah's printed `ayah_count`.
- Unknown symbol: flag it in the review sheet, resolve at review, log in `docs/symbols_glossary.md`.

## Open questions (details in `docs/spec.md` §9)

1. Printed page 1 (not in the PDF): how to handle, deferred. Mapping for the other scanned images unconfirmed.
2. License: CC0 1.0 recommended, not chosen. Check publisher rights on the print layout.
3. Should standalone waqf marks stay out of `quran_words`? (current assumption: yes)
4. `hizb` line-level attachment (deferred).
5. Font / text-encoding strategy for the future app (Hafs-oriented fonts may not render Qaloon forms).
6. Row-type completeness: watch for new element types on pages 3–11.

## Next steps

1. User verifies page 2 and reports errors; fix them, mark page 2 `verified` in the manifest, move drafts into the master `data/quran_layout.jsonl` / `data/quran_words.jsonl`, run the validator on the master files.
2. Transcribe page 3 using the PDF (PDF page 2). Continue through printed page 11, verifying each before the next. Update the manifest cursor.
3. Choose the license; add `LICENSE`.
4. Handle printed page 1 later.

## File structure

```
Qaloun_Dataset/
├── README.md
├── schema.md
├── data/
│   ├── manifest.json
│   ├── drafts/            page_0002_layout.jsonl, page_0002_words.jsonl, page_0002_review.md
│   ├── quran_layout.jsonl (not yet created — master, filled only from verified pages)
│   └── quran_words.jsonl  (not yet created)
├── scripts/validate.py
└── docs/
    ├── spec.md
    ├── handoff.md
    ├── symbols_glossary.md
    └── sessions/          2026-09-25.md, 2026-10-01.md
```

## What a new batch-transcription conversation needs

`schema.md`, `data/manifest.json`, `docs/symbols_glossary.md`, plus the batch's page images from the user. Not `spec.md`, not `handoff.md`.
