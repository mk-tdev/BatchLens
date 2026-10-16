# Pip: AI quality investigator

Pip uses Gemini function calling via Vertex AI to choose its next investigative action. The server passes explicit function declarations to Gemini, executes only validated tools, then returns function responses to the model. The full model content is preserved between turns, including thought signatures; tool-call IDs are retained. This is a real tool loop, not a scripted sequence of UI animations. It requires live Gemini and has no authored-mode fallback.

## Tools and authority

- `evidence_index`: available documents and human-confirmed case state.
- `read_document`: original text/CSV or real Gemini image extraction. Image readings become pending candidates. Existing readings are reused with their review status.
- `search_archive`: search the supplied synthetic archive for supplementary documents, including the S4 replacement slip. This does not search an external ERP.
- `trace_lot`: a deterministic hypothetical trace. It uses only human-confirmed shipment mappings and does not change approved scope.
- `submit_findings`: source-cited draft findings, proposed inspection checks and open questions. The server requires cited documents to have been read during the run. Citation validation proves source access, not that every model claim is correct; review remains necessary.

The agent cannot confirm the baseline, approve S4's relationship, save an inspection decision, release stock or contact anyone. Review commands remain separate and require the operator. While a run is active, case mutations and manual extractions are blocked to avoid competing changes. Sources and generated findings are treated as untrusted data.

## Using it

Open **Pip / AI investigator** from the factory or a crew room, then **Let Pip investigate**. The journal updates while Gemini requests tools. Expand tool results to inspect the actual returned data. When findings are ready, inspect original sources from the citation buttons, review the baseline and S4 relationship using the existing controls, then prepare the reviewed handover. The saved report includes a frozen copy of Pip's AI draft, explicitly separated from the approved scope.

## Limits and recovery

Each run allows at most 6 model turns, 24 tool actions and 95 seconds. Two runs are available per case, with at most 12 investigator model calls plus the existing 8 image-extraction attempts. Every real model call shares the existing 100-attempt daily project budget. These are usage limits, not a monetary spending cap. No new services, roles or credentials are required.

A failed or timed-out run retains partial journal entries and pending readings. It does not approve any decisions. Interrupted leases expire; the operator can inspect partial results or use the remaining follow-up run. Requests are deduplicated by run ID. Case ownership and expiry apply to the journal and sources.

## Architecture reference

Implementation follows the [Google Gen AI SDK's manual function-calling pattern](https://github.com/googleapis/python-genai): explicit declarations, automatic calling disabled, model tool calls executed by a bounded server loop, function responses returned in the conversation. The visual factory, crew animation and physical inspection activity remain illustrative, not sensor telemetry or an executed real-world inspection.

## Demo sequence

1. Open the playable factory and Pip's investigation journal. State the leaking-cap mission and start the investigator.
2. Show Gemini's actual tool requests and the document results as they arrive. Expand an image reading and the hypothetical trace.
3. Show the archive search and recovered-slip candidate if Gemini selected them. Do not narrate unexecuted actions as completed.
4. Inspect the proposed checks and source citations. Point out that the approved scope remains unchanged until review.
5. Use the operator checkpoints to approve the baseline and S4 connection, then save the reviewed handover and export its frozen AI draft alongside the deterministic scope.

A run can stop early at its time or tool budget. In that case show the incomplete status and retained evidence rather than presenting it as a completed autonomous investigation.

## Live verification: 17 October 2026

A fresh live synthetic case completed with Gemini 3.5 Flash-Lite. Gemini selected 12 tool actions: evidence index, reads of E1–E6, archive search (`Penang East S4 packing slip batch`), E7 read, traces of CAP-17 and CAP-18, and findings submission. The run produced four cited findings and an open question about whether dimensional exceptions cause functional leakage. E2/E3/E6/E7 readings used real Gemini.

Before operator review, the baseline and S4 mapping remained unapproved. Verification then used the normal review screens to inspect original E2/E3/E4/E5/E7, confirm the baseline and S4 relationship, save a 1,500-unit proposal and download HTML. The export included the frozen AI draft with its advisory label. Reload retained the journal, findings and approved case state. The final deployed revision is `batchlens-00005-vq2`, built from `a2aa4f8`; the live inference run occurred on `batchlens-00004-wsw`, followed by journal-layout and approval-gate refinements validated with 14 backend tests and a production build. No production accuracy or physical inspection claim is made.

The adaptive operations release adds procedure, mission, result-reading and scope-comparison tools. See [the adaptive operations guide](11_Adaptive_Operations.md) for current behavior and budgets.
