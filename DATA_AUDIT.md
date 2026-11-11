# Evidence audit — 11 November 2026

Scope: `/home/pc_pusaka/zandi/projects/20_demo`, its documentation and all 15 slides and speaker notes in `PPT_GEMASTIK19_MBG_v5.pptx`. No external project or dataset was searched. No external artifact path or hyperlink was found in the deck. All embedded PNG figures were extracted for inspection; the pipeline, labeling diagram, and comment illustration were visually inspected. Full slide rendering was unavailable (no LibreOffice); this is not a visual audit of every slide or embedded video.

Presentation SHA256: `a5178f25c4268b60b9d5763f895d95499e781b2b21875812070317bae1b892f9`. The original deck is reference-only, unchanged and excluded from publication, as is its Windows Zone.Identifier.

## Data availability matrix

| Artifact | Status | Evidence / permitted use |
|---|---|---|
| Competition size, period, platforms, six target categories | PARTIAL | Human-provided brief; PPT slides 1, 4, 6. 434,463 is the **described dataset size**, not a verified processed count. |
| `part_0.csv` through `part_4.csv` | MISSING | No source CSV in project. Actual spellings of id/content/date_created/specific_resource_type cannot be verified. |
| Classification submission / predictions / models | MISSING | No CSV, notebook, trained model, or executable classification pipeline present. No group totals or proportions. |
| Gold labels, split, confusion matrix, Macro-F1 | MISSING | No evaluation artifact. A proposed test size in a diagram is not a measured result. |
| Topic assignments, ranks, keywords, counts | MISSING | No output. Cannot calculate within-group shares, lift, trends, or topic ranking. |
| Three source IDs per topic and source excerpts | MISSING | No traceable examples. No actual comments or IDs published. |
| Policy questions | PARTIAL | PPT slide 11 explicitly says examples of hypotheses, to be filled after analysis. Published only as hypothesis plans, common to all groups. |
| Existing Flask preview | REAL_AND_VALIDATED | Local routes and Gunicorn import verified. This validates application behavior, not scientific findings. |

No analytical artifact qualifies as REAL_AND_VALIDATED or REAL_BUT_UNVALIDATED. Missing counts are JSON `null`, displayed as “— / belum tersedia”, never as zero.

## Complete slide review

| Slide (physical order) | Narrative / implication |
|---|---|
| 1 | VOICE RADAR; 434,463 comments; Who / What / When / So What. Connect to PETA SUARA MBG as the companion prototype. |
| 2 | Team: Indra Gantz, Universitas Airlangga; Indah Auliya, Muhammad Raafi’ Adhinandra, Azgan Rizal Sani. |
| 3 | Motivating examples: satisfaction, menu complaints, safety concerns, media. Not measured findings. |
| 4 | Author account metadata lost; only text/time/platform remain according to narrative. No local dataset to corroborate. |
| 5 | Four questions: who, what, when, action. Demo prioritizes who → what → contrast → verification. |
| 6 | Short, informal texts, imbalance/reposts; proposed n-grams, IndoBERT, dedup, Macro-F1, weak supervision and gold labels. Quantitative audit missing. |
| 7 | Pipeline figure: audit → WHO → WHAT → WHEN → SO WHAT; one common topic map. |
| 8 | Labeling figure: lexicon plus zero-shot agreement → silver labels; ±600 gold labels “only for testing”. Notes still use a label-count placeholder. No actual labels found. |
| 9 | Candidate ladder: majority baseline, frozen multilingual-e5-small + LR, word/char TF-IDF LR/SVM/NB, IndoBERT, ensemble. No winner verified. |
| 10 | NMF, LDA, LSA+KMeans, e5+HDBSCAN; silhouette, NPMI, stability; c-TF-IDF and representative IDs. Proposed methodology only. |
| 11 | Four policy hypotheses and verification plans; explicitly not final findings. Basis of clickable hypothesis explorer. |
| 12 | Response horizons; conditional policy directions, not evidence of impacts or achieved outcomes. |
| 13 | Topic Explorer, Group Contrast, Trend Monitor, Policy Brief. Product concept, not proof of implemented analytics. |
| 14 | Future roadmap begins with running the pipeline and filling actual numbers; reinforces preview status. |
| 15 | Closing / team identity. |

## Material inconsistencies and claims to avoid

- “Indra Ganz” and “Indra Gantz” alternate. UI follows slide 2's “Indra Gantz”; confirm preferred spelling before final presentation.
- Printed slide numbers after slide 10 differ from physical order. UI citations use physical slide 11 for the hypothesis table (printed 17).
- Speaker notes sometimes say “we trained / use” while the roadmap and placeholders indicate planned work. Presenter must say **rancangan / direncanakan**, unless independent results are supplied.
- Gold-set size ±600 in a graphic conflicts with an unresolved count placeholder in notes. Neither establishes completed annotation or a score.
- Illustrated comments lack source IDs; do not reuse them as actual evidence or assign their apparent styles to real generations.
- Generational labels estimate text-associated categories; they do not recover true ages. Gold-set agreement does not establish demographic accuracy.
- Social media volume is not population prevalence. Relative prominence is not policy impact; coincident events are not causal proof.

## Implemented public states

REAL: six-category selection, contextual hypothesis drawer, comparison selectors and guards, method/audit panel, local API, guided demo.

PREVIEW: the entire analytical dashboard. Four issue names are PPT hypotheses, with no rank or attribution to any group. Selecting a group changes the viewing context only.

UNAVAILABLE: predicted distributions, topic rankings/keywords/counts, real comment evidence, numerical contrasts, platform/month filters, Macro-F1, trends, aggregate export. Disabled/omitted until supporting evidence is available.

Next evidence gate: obtain the five source CSVs plus classification and topic outputs in an authorized private location; validate schema, unique IDs, duplicates, coverage, label vocabulary, ranks, references and totals offline. Redact examples before publication. Agree on the six submission labels before transforming them. Do not manually enter plausible counts into public JSON. The current preview must not be switched to an analysis state without implementing and testing that data contract.
