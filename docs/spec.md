# Qaloon Quran Dataset — Living Specification

> Single source of truth for the project. Every item is flagged **Confirmed** or **Assumption (unconfirmed)**. History of how we got here lives only in the Change Log (§10) — everything above it describes the current state, not the path to it.
>
> This file mirrors `claude/spec.md` in the "Iqraa Dataset" claude.ai project, which is the actively-edited working copy. This repo copy is synced on meaningful updates.

**Last updated:** 2026-09-25
**Status:** Repo scaffolded and live. Blocked on: getting the actual source page images in hand to confirm page numbering and start batch 1.
**Repo:** https://github.com/yassinemaazaoui114-git/Qaloun_Dataset

---

## 1. Project Summary

Build a **textual dataset of the Holy Quran in the Qaloon riwayah** (رواية قالون عن نافع), digitized from the Tunisian **Al-Mushaf Al-Mu'allim** (المصحف المعلم) print edition, preserving the **exact printed page/line layout**. First step toward a future Wahy-style mushaf app with Tarteel-style recitation correction — this phase is dataset-only.

**Deliverable:** the dataset, published openly.

**Why it matters:** Qaloon is the dominant recitation across Tunisia, Algeria, Libya, Mauritania, and much of West Africa, yet almost every existing digital Quran dataset is Hafs 'an 'Asim. No complete, verified, layout-faithful Qaloon text dataset exists publicly.

---

## 2. Scope

### In scope (v1) — all Confirmed
- Full Quran text, Qaloon riwayah, all surahs.
- Exact printed page/line layout — one row per printed line.
- Ayah and surah boundaries as structured data.
- Plain black text only — no tajwid coloring.
- Word-level normalization alongside the line-level faithful text (§4).
- Every page manually verified before the next batch starts. No exceptions.

### Out of scope for v1 — deferred, not cancelled
- Tajwid coloring layer → v2 (§7).
- Audio — excluded entirely.
- Recitation-correction model — not part of the dataset project.
- Morphological word analysis (root/lemma/POS) — not needed for a recitation-highlighting use case.
- The Mushaf app itself — future project, consumes this dataset.

---

## 3. Source Material

- **Confirmed** — Al-Mushaf Al-Mu'allim, Tunisian edition (Qaloon). Canonical source: Internet Archive item `qalooon-tones` (https://archive.org/details/qalooon-tones) — 605 scanned page images (000.jpg–604.jpg), also available as PDF.
- **Confirmed** — Source is images only. AI does first-pass transcription; a human verifies word-by-word against the image; only then is a page "verified."
- **Confirmed** — This sandbox cannot fetch archive.org directly (tested, blocked). The user supplies the source file directly.
- **Confirmed** — This edition: one text block per page, no repetition rows, ~15 lines/page. One row per printed line.
- **Open** — Mapping of archive.org file numbers (000–604) to actual printed page numbers. Do not assume 000.jpg = page 1 — must confirm once the source file is in hand, before batch 1.
- Pages 83 and 502 were used to design the schema. **They are illustration examples only, never run through the real verification process — not dataset content.**

---

## 4. Data Model / Schema

**Canonical, detailed reference: `schema.md` in this repo.** This section is a summary.

Two tables, two append-only JSONL files:

- **`quran_layout`** — one row per printed line (or surah header / basmala). Fields: `page`, `line`, `type` (`ayah_line`/`surah_header`/`basmala`), `surah`, `juz`, `is_centered`, plus type-specific fields (`text` + `first_word_id`/`last_word_id` for `ayah_line`; `surah_name`/`ayah_count`/`surah_order` for `surah_header`). `text` preserves the line exactly as printed, including the inline ayah-end marker — this is the faithful-rendering layer.
- **`quran_words`** — one row per word: `id`, `surah`, `ayah`, `position`, `text` (space-delimited printed token, tashkeel included — no morphological splitting).

Word IDs, positions, and per-word ayah membership are all generated automatically from the same verified line text — no extra manual verification step beyond checking the line itself.

**Waqf and sajda marks:** inline in `text` only, no separate structured field in v1.

**Page metadata:** `juz` is a field on every row. `hizb` line-level attachment is deferred (marginal medallions indicate it, but pinpointing the exact line needs closer inspection than done so far).

**Ayah-count validation:** the structural validator does not use any external ayah-count-per-surah table (Qaloon's Madani First Count differs from the generic Kufi-count tables most tools ship with, and from Warsh's Madani Last Count). Instead each surah's true count is read from its own printed `surah_header.ayah_count`, sourced from the mushaf itself.

---

## 5. Working Process

- **Batch size:** 10 pages. No batch N+1 until batch N is verified.
- **Two-layer QA per batch:** (1) automatic structural check (`scripts/validate.py` — ayah/line sequencing, ayah counts against each surah's own printed total; run against the *cumulative* master files, not an isolated batch) before a human ever looks at it; (2) human word/diacritic check against the source image — the layer only a person can do.
- **Storage:** per-page draft files during active work; merged into the single master `quran_layout.jsonl`/`quran_words.jsonl` once verified. The master files are the published deliverable.
- **Verification ownership:** solo (the user) for v1 plain text. A qualified Qaloon reviewer becomes relevant only for v2 tajwid rule-labeling.
- **Conversation cadence:** roughly one fresh conversation per 2–3 batches (~20–30 pages), not one per single batch — bounds conversation length (the real cost driver, via context re-processing) without paying fixed re-orientation overhead too often. Adjustable empirically.
- **Model tiers:** Sonnet for actual page transcription (vision + accuracy is what matters). Haiku for applying corrections once the user has specified the fix (mechanical, no ambiguity). No model needed for the structural validator or an OCR cross-check (plain code/tools). Opus reserved for genuinely ambiguous cases only.
- **Optional, not yet built:** independent OCR cross-check alongside AI vision reading, flagging disagreements for extra human scrutiny.

---

## 6. Publishing

- **Confirmed** — Published openly.
- **Open** — Platform, license, source-print attribution.

---

## 7. Future Phases

- **v2 — Tajwid coloring layer:** (1) red-span flagging (cheap, while transcribing) and (2) rule labeling (expensive, needs a Qaloon-qualified reviewer — real mislabeling risk in an authoritative dataset).
- **Future — Mushaf app** (Wahy-style layout) + Tarteel-style word-highlighting recitation correction, consuming this dataset. Rendering needs word data (✓), a compatible font (not yet chosen), layout data (✓), surah-name metadata (✓) — confirmed against Tarteel QUL's own stated requirements.
- **Design work can proceed in parallel** with dataset-building, using `schema.md` + the two sample pages as the shared contract. **Exception:** font/text-encoding strategy (plain Unicode vs. QCF-style per-word glyph ligatures) is a shared dependency — affects what `quran_words.text` may need to hold — should be a joint decision, not built on unilaterally by either side.
- **Future (parked, may never happen):** the recitation-correction model itself.

---

## 8. Repo & Docs Layout

Two different audiences, two different homes:

| File | Lives in | Who reads it |
|---|---|---|
| `schema.md`, `data/manifest.json` | GitHub repo | Every batch-transcription conversation. Small, stable, self-sufficient — this is all a new conversation needs to do the work. |
| `data/quran_layout.jsonl`, `data/quran_words.jsonl` | GitHub repo | The dataset itself. |
| `scripts/validate.py` | GitHub repo | Run every batch, before human review. |
| `docs/spec.md`, `docs/handoff.md` | GitHub repo (mirrored) | Anyone cloning the repo for full context — a future contributor, another AI tool, or the user without claude.ai access. **Not** needed by a batch-transcription conversation. |
| `claude/spec.md` | claude.ai Project | The working copy, edited directly during conversations. Mirrored here on meaningful updates. |

A batch-transcription conversation pulling the repo gets everything it needs without ever touching `spec.md`.

---

## 9. Open Questions

1. File-number → printed-page-number mapping — needs the actual source file.
2. `hizb` line-level attachment — deferred, not blocking.
3. Publishing platform, license, source attribution.
4. Font / text-encoding strategy for the future app — not blocking dataset work now, but a joint decision before app/design work goes far (§7).
5. Row-type completeness (`ayah_line`/`surah_header`/`basmala`) — sufficient for the two sample pages seen; watch for new element types once real pages start flowing.

---

## 10. Change Log

| Date | Change | Why |
|---|---|---|
| 2026-09-18 | Doc created; scoping conversation consolidated (text-only, page/line-faithful, v1 plain text, initial single-table schema sketch, waqf/sajda left open). | First source-of-truth pass. |
| 2026-09-25 | Spec moved into the project (was a local file). | Project reattached; docs were empty. |
| 2026-09-25 | Source pinned to archive.org `qalooon-tones`. Confirmed this sandbox can't fetch archive.org directly. | Tested via WebFetch (works) / curl (blocked). |
| 2026-09-25 | Process agreed: batch size 10, fresh conversation every 2-3 batches, model tiers per step, schema.md+manifest.json (not spec.md) as what a new conversation needs. | User is cost-conscious; conversation length (not page count) is the real cost driver. |
| 2026-09-25 | Schema redesigned from a single-table (line text + `ayahs_on_line`/`contains_ayah_end` fields) into two tables, `quran_layout` + `quran_words`, after comparing against Tarteel QUL's data model. Old fields dropped as redundant once word-level data exists. | QUL needs word-level IDs for rendering; user's own app plans (word-highlighting) need the same — avoids a costly re-do later. No extra manual verification cost. |
| 2026-09-25 | Discovered Qaloon uses the Madani First Count (distinct from Kufi and from Warsh's Madani Last Count). Validator uses each surah's own printed `ayah_count` instead of an external table. | Avoids silently validating against the wrong counting tradition. |
| 2026-09-25 | Waqf/sajda marks resolved: inline-only in v1. | Was open question from 2026-09-18; confirmed when user gave the go-ahead to proceed. |
| 2026-09-25 | Repo scaffolded (`schema.md`, `data/manifest.json`, `scripts/validate.py`, `README.md`) and pushed by the user manually (session's GitHub connection didn't grant this sandbox push access — separate, session-level repo authorization needed). Validator smoke-tested against a broken fixture, caught all planted errors. | User gave the go-ahead; this session's git proxy returned 403 on push attempts even after connecting GitHub generally. |
| 2026-09-25 | Realized `spec.md`/`handoff.md` were Project-only, leaving the repo non-self-contained — conflicts with handoff.md's own stated purpose ("another AI tool" should be able to pick up). Mirrored both into `docs/` in the repo. | User asked why the repo didn't have them. |
| 2026-09-25 | Full rewrite of this doc: removed resolved items and superseded-design narrative from the main body, added §5 (Working Process) and §8 (Repo & Docs Layout) as permanent reference sections. | User asked for a clean rewrite reflecting only current state, not the path taken to get there. |
