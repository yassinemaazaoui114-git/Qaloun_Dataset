# Qaloon Quran Dataset

A textual dataset of the Holy Quran in the Qaloon riwayah (رواية قالون عن نافع),
transcribed from the Tunisian Mushaf Al-Mu'allim print edition, preserving the
exact printed page/line layout.

- **Decision history / rationale / open questions:** [`docs/spec.md`](./docs/spec.md)
  (mirrors the working copy in the "Iqraa Dataset" claude.ai project).
- **Picking this up cold?** Start with [`docs/handoff.md`](./docs/handoff.md).
- **Schema / transcription rules (what to do when you see X):** see
  [`schema.md`](./schema.md) — the operational reference used for every
  transcription batch.
- **Progress:** [`data/manifest.json`](./data/manifest.json).
- **Data:** `data/quran_layout.jsonl` (line-level, mushaf-faithful),
  `data/quran_words.jsonl` (word-level, normalized).
- **Validator:** `scripts/validate.py` — structural checks (ayah sequencing,
  ayah counts against each surah's own printed total). Run before human
  review, not instead of it.

## Status

Pilot batch 1 in progress. Printed page 2 is transcribed (draft in `data/drafts/`), awaiting human verification. Nothing is verified yet.

## License / attribution

TBD — see spec.md open questions.
