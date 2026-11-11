# Source contract — v1

`data_source.py` is the source boundary. Current application explicitly loads `load_source('synthetic')`. Real mode is not enabled by an environment variable or browser control. `load_source('real')` fails without an explicit reviewed path; a registered real source must also pass schema/provenance validation. The `validated_real` marker is a necessary declaration, not a substitute for independent scientific review.

## Common dataset envelope

| Key | Meaning |
|---|---|
| `schema_version` | Integer 1 |
| `source.kind` | Exactly `synthetic` or `real`; never mixed |
| `source.label`, `source.disclosure` | Public provenance and interpretation |
| `source.seed`, `source.generated_by` | Required provenance in current synthetic fixture |
| `source.validated_real` | False for synthetic; true only after evidence review for real promotion |
| `competition_brief` | Separately attributed context; never part of calculated totals |
| `groups` | Six unique `{id, name, years}` category definitions |
| `topics` | Shared map of `{id, name, short, keywords, question, verify}` |
| `platforms` | Platform vocabulary |
| `months` | `{id: YYYY-MM, name}` catalog |
| `records` | Small source rows below; all analytics computed from these |

Each record has `id`, `content`, ISO `date_created` (YYYY-MM-DD), `specific_resource_type`, `taggenerasi` (catalog name), `topic_id`, `topic_name`. IDs must be unique. Synthetic IDs begin `SIM-`. Topic ID/name references, group labels, dates and platform values must match the catalog. Synthetic content contains no real account identities. No inference confidence or model score exists in this contract.

`static/js/analytics.js` consumes this source-neutral catalog/record contract, returning group counts, topic rankings, matrix shares, comparison shares/deltas and matching evidence. It does not embed any generation-specific counts or findings. Display copy in the current UI deliberately identifies everything as synthetic.

## Scope and denominator

1. Cohort = records matching platform and month.
2. Group distribution = counts per group in cohort; group share divides by cohort size.
3. Topic ranking = cohort further restricted to the selected group (or all groups). Every topic's share divides by that group's total, including records assigned to other topics.
4. Comparison = each group's topic share calculated independently; delta = A minus B in percentage points. Zero denominator gives `null`, never NaN, infinity or an invented zero share.
5. Matrix = same shares for all six groups. Intensity uses the largest share currently visible; the legend changes with filters. Numeric labels remain present.
6. Topic selection is an evidence selection and visual highlight. It does not reduce matrix/comparison denominators. Search and pagination affect only evidence, never chart totals.
7. Export = all six groups × eight topics for platform/month cohort, with synthetic provenance, seed and denominator on each row.

## Offline reproducibility

`python3 scripts/generate_demo_data.py` creates 1,080 unique rows, seed `190726`, 310,359 UTF-8 bytes including newline. Group counts: 100, 152, 218, 286, 130, 194. Text variants are sampled from a shared topic vocabulary independent of demographic labels. Scenario group weights are explicitly arbitrary. Platform wording variants and dates are synthetic. Uniqueness does not make comments real or statistically representative.

## Future real integration

Obtain authorized outputs in a private location. Independently validate IDs, duplicates, schema, coverage, prediction vocabulary, missing assignments, counts, ranks, references, labels/evaluation and redaction. Record evidence/version/scope. Do not put 434k raw comments into the client contract: prepare a small public-safe slice or extend the adapter with precomputed aggregates plus filtered evidence. Missing/unassigned groups or topics require explicit coverage accounting and schema changes, not silent dropping.

Then register a separate real path with `load_source`, wire source-aware UI copy and the mode selector, and retest the common analytics contract. The current UI is intentionally locked to simulation; changing only `validated_real` must not be treated as production readiness. Replace all provenance wording only for components actually backed by reviewed real outputs. Never merge source kinds in one metric, publish private raw text, or use synthetic labels to evaluate a real model.
