# Qaloon Quran Dataset — Schema & Transcription Rules

> This is the **operational reference** — what to do when you see X. For decision history, rationale, and open questions, see `spec.md` in the "Iqraa Dataset" claude.ai project. This file should rarely need spec.md's context to be used correctly.

## Files

Two tables, two append-only JSONL files (one JSON object per line):

- **`data/quran_layout.jsonl`** — one row per printed mushaf line (or surah header / basmala). The faithful, human-readable layer.
- **`data/quran_words.jsonl`** — one row per word. The normalized, machine-addressable layer.

Plus `data/manifest.json` — progress tracker (see bottom).

---

## `quran_layout` row

One row per printed line on the page. Every row has a `type`.

| Field | Type | Applies to | Meaning |
|---|---|---|---|
| `page` | int | all | printed page number |
| `line` | int | all | line number within the page (1-based, top to bottom) |
| `type` | string | all | `"ayah_line"` \| `"surah_header"` \| `"basmala"` |
| `surah` | int | all | surah number this line belongs to (for `surah_header`, the surah it introduces) |
| `juz` | int | all | juz number (from the page header) |
| `is_centered` | bool | all | true for `surah_header`/`basmala`, false (justified) for `ayah_line` |
| `text` | string | `ayah_line`, `basmala` | the line **exactly as printed**, including the inline ayah-end marker (e.g. `﴿٢٧﴾`) in its printed position |
| `first_word_id` | int | `ayah_line` | id of the first word (in `quran_words`) on this line |
| `last_word_id` | int | `ayah_line` | id of the last word on this line |
| `surah_name` | string | `surah_header` | e.g. `سُورَةُ الْأَحْقَافِ` |
| `ayah_count` | int | `surah_header` | printed ayah count for this surah (from the banner) |
| `surah_order` | int | `surah_header` | printed order-in-mushaf number (from the banner) |

**Why both `text` and word-ID range on the same row:** `text` gives faithful page rendering (what a mushaf app shows). `first_word_id`/`last_word_id` give clean programmatic access ("give me ayah 28") without parsing symbols out of a string. A line spanning two ayahs (very common) needs both — the reader can't reliably split on the marker alone, and the marker's exact printed position is lost if you don't keep it.

**Not stored as separate fields (deliberately):** `ayahs_on_line`, `contains_ayah_end`. These were in an earlier draft of this schema but are now redundant — fully derivable by looking up each word from `first_word_id` to `last_word_id` in `quran_words` and reading its `ayah` field. Keeping them as separate fields would risk them drifting out of sync with the real data; better to compute them when needed.

**Waqf marks (ۖ ۚ ۗ etc.) and sajda markers:** inline in `text` only, no separate structured field in v1. They render correctly as part of the text either way; structuring *which rule* each mark represents is v2/tajwid territory (see spec.md §7).

---

## `quran_words` row

| Field | Type | Meaning |
|---|---|---|
| `id` | int | stable, global, sequential across the whole Quran |
| `surah` | int | surah number |
| `ayah` | int | ayah number within the surah |
| `position` | int | word's position within its ayah (1-based) |
| `text` | string | the word exactly as printed — a space-delimited token, tashkeel included. **Not** morphologically split (no prefix/suffix separation like QUL's root/lemma/POS — out of scope, we're not doing linguistic analysis) |

`id` is generated automatically from the verified line text (split on spaces, strip the ayah-marker glyph) — **this is not extra manual work**. You verify the line text once; the word table is a mechanical derivative of it.

---

## Worked example — Surah An-Nisa, ayah 29 (page 83, fully self-contained on that page)

Printed line text (page 83, lines 3–6, from `quran_layout`):

```json
{"page":83,"line":3,"type":"ayah_line","surah":4,"juz":5,"is_centered":false,
 "text":"عَنكُمْ ۚ وَخُلِقَ ٱلْإِنسَٰنُ ضَعِيفًا ﴿٢٨﴾ يَٰٓأَيُّهَا ٱلَّذِينَ",
 "first_word_id":101,"last_word_id":109}
{"page":83,"line":4,"type":"ayah_line","surah":4,"juz":5,"is_centered":false,
 "text":"ءَامَنُوا۟ لَا تَأْكُلُوٓا۟ أَمْوَٰلَكُم بَيْنَكُم بِٱلْبَٰطِلِ إِلَّآ أَن",
 "first_word_id":110,"last_word_id":117}
{"page":83,"line":5,"type":"ayah_line","surah":4,"juz":5,"is_centered":false,
 "text":"تَكُونَ تِجَٰرَةً عَن تَرَاضٍ مِّنكُمْ ۚ وَلَا تَقْتُلُوٓا۟ أَنفُسَكُمْ ۚ",
 "first_word_id":118,"last_word_id":125}
{"page":83,"line":6,"type":"ayah_line","surah":4,"juz":5,"is_centered":false,
 "text":"إِنَّ ٱللَّهَ كَانَ بِكُمْ رَحِيمًا ﴿٢٩﴾ وَمَن يَفْعَلْ ذَٰلِكَ عُدْوَٰنًا",
 "first_word_id":126,"last_word_id":133}
```

Corresponding `quran_words` rows for ayah 29 (ids illustrative — real ids are a running count from page 1 onward):

```json
{"id":108,"surah":4,"ayah":29,"position":1,"text":"يَٰٓأَيُّهَا"}
{"id":109,"surah":4,"ayah":29,"position":2,"text":"ٱلَّذِينَ"}
{"id":110,"surah":4,"ayah":29,"position":3,"text":"ءَامَنُوا۟"}
{"id":111,"surah":4,"ayah":29,"position":4,"text":"لَا"}
{"id":112,"surah":4,"ayah":29,"position":5,"text":"تَأْكُلُوٓا۟"}
... (continues: أَمْوَٰلَكُم, بَيْنَكُم, بِٱلْبَٰطِلِ, إِلَّآ, أَن, تَكُونَ, تِجَٰرَةً, عَن, تَرَاضٍ, مِّنكُمْ, وَلَا, تَقْتُلُوٓا۟, أَنفُسَكُمْ) ...
{"id":130,"surah":4,"ayah":29,"position":19,"text":"إِنَّ"}
{"id":131,"surah":4,"ayah":29,"position":20,"text":"ٱللَّهَ"}
{"id":132,"surah":4,"ayah":29,"position":21,"text":"كَانَ"}
{"id":133,"surah":4,"ayah":29,"position":22,"text":"بِكُمْ"}
{"id":134,"surah":4,"ayah":29,"position":23,"text":"رَحِيمًا"}
```

Notice: line 3's `last_word_id` (109) is ayah 29's word #2 — line 3 ends mid-ayah, exactly as printed. `text` preserves that faithfully; `quran_words` makes it queryable.

## Worked example — `surah_header` + `basmala` (page 502)

```json
{"page":502,"line":7,"type":"surah_header","surah":46,"juz":26,"is_centered":true,
 "surah_name":"سُورَةُ الْأَحْقَافِ","ayah_count":35,"surah_order":46}
{"page":502,"line":8,"type":"basmala","surah":46,"juz":26,"is_centered":true,
 "text":"بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"}
```

---

## `manifest.json`

Tracks progress. See `data/manifest.json` — structure documented there. Key idea: it carries a `cursor` (last verified page/surah/ayah + whether that ayah closed or is still open going into the next page) so a new batch never needs to read old page content to know where to continue.

## Status: DRAFT / UNVERIFIED

Everything transcribed against this schema is a first-pass AI reading until a human has checked it word-by-word against the source page image. No row is part of the real dataset until its page is marked `verified` in `manifest.json`.
