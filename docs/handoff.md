# Handoff — Qaloon Quran Dataset

> Read this first if you're picking this project up cold (a new conversation, another AI tool, or the user returning after a gap). For full decision history and rationale, see `docs/spec.md` in this same folder.

**As of:** 2026-09-25 (end of session — see `docs/sessions/2026-09-25.md` for that session's own log)

## What's done

- Project scoped: textual Qaloon dataset, layout-faithful to the Tunisian Mushaf Al-Mu'allim print edition, published openly. App/model are future, separate phases.
- Schema finalized: two tables — `quran_layout` (line-level, faithful text + word-ID ranges) and `quran_words` (word-level, normalized). Full field definitions in `schema.md`.
- Source pinned: Internet Archive item `qalooon-tones`, 605 page images / PDF.
- Repo scaffolded and live, self-contained: `schema.md`, `data/manifest.json`, `scripts/validate.py`, `README.md`, `docs/spec.md`, `docs/handoff.md` (this file), `docs/sessions/` (dated per-session summaries, never merged).
- Structural validator built and smoke-tested (catches line-sequence gaps, ayah-sequence gaps, out-of-order word positions, dangling word-ID references). Uses each surah's own printed `ayah_count`, not an external table (Qaloon's Madani First Count differs from generic tables).
- Working process agreed: 10-page batches, verify-before-continuing, two-layer QA (automatic structural check, then human word-level check against the source image), model tiers assigned per step (Sonnet for transcription, Haiku for mechanical corrections, no model for the validator), roughly one fresh conversation per 2-3 batches.
- Symbol-handling workflow agreed for unfamiliar recitation marks (tasheel, sila, etc.): check standard Unicode Quranic-annotation range → QUL → other sources; log resolved ones in `docs/symbols_glossary.md` (**not yet created** — first real entry will come from the pilot batch).
- End-of-session habit settled: session summary → `docs/sessions/YYYY-MM-DD.md`; `docs/handoff.md` kept current; GitHub changes prepared with exact push commands (this sandbox cannot push directly — confirmed, session-level repo authorization issue).

## What's in progress

Nothing yet — no page has entered the actual transcription pipeline. Two pages (83, 502) were used only to design the schema; they are **not verified dataset content**.

## Blocked on

**Getting the actual source page images.** This working environment cannot fetch archive.org directly (tested, blocked by network policy). The user needs to download the PDF or JPEG bundle from the `qalooon-tones` item and provide it (upload, or commit into the repo).

## Immediate next steps, in order

1. Get the source PDF/JPEG bundle from the user.
2. Confirm how archive.org's file numbering (000.jpg–604.jpg) maps to actual printed page numbers — do not assume they match 1:1.
3. Run the pilot batch: the first ~10 pages (Al-Fatiha + opening of Al-Baqarah) — these carry the most layout edge cases (title pages, first basmala, first surah header), so issues surface here cheaply rather than 300 pages in.
4. User verifies the pilot against the real mushaf; fix whatever the pilot surfaces in `schema.md` before scaling up.
5. From there: batches of 10, strict verify-before-continuing, update `data/manifest.json`'s cursor after each verified batch.

## Open questions (see `docs/spec.md` §9 for detail)

1. File-number → printed-page-number mapping.
2. `hizb` line-level attachment (deferred).
3. Publishing platform, license, attribution.
4. Font/text-encoding strategy for the future app (not blocking now).
5. Row-type completeness — watch for new element types once real pages start flowing.

## File structure

```
Qaloun_Dataset/
├── README.md              orientation, points here and to schema.md
├── schema.md              operational rules — what a transcription conversation reads
├── data/
│   ├── manifest.json      progress tracker + continuity cursor
│   ├── quran_layout.jsonl (not yet created — master dataset, line-level)
│   └── quran_words.jsonl  (not yet created — master dataset, word-level)
├── scripts/
│   └── validate.py        structural validator, run before human review
└── docs/
    ├── spec.md            full decision history/rationale (mirrors the claude.ai Project copy)
    └── handoff.md         this file
```

## What a new batch-transcription conversation actually needs

Just `schema.md` + `data/manifest.json` from this repo, plus that batch's source page images from the user. Not `spec.md`, not `handoff.md`, not prior page data — see `docs/spec.md` §8 for why.
