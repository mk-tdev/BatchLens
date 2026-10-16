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

Each run allows at most 6 model turns, 14 tool actions and 95 seconds. Two runs are available per case, with at most 12 investigator model calls plus the existing 8 image-extraction attempts. Every real model call shares the existing 100-attempt daily project budget. These are usage limits, not a monetary spending cap. No new services, roles or credentials are required.

A failed or timed-out run retains partial journal entries and pending readings. It does not approve any decisions. Interrupted leases expire; the operator can inspect partial results or use the remaining follow-up run. Requests are deduplicated by run ID. Case ownership and expiry apply to the journal and sources.

## Architecture reference

Implementation follows the [Google Gen AI SDK's manual function-calling pattern](https://github.com/googleapis/python-genai): explicit declarations, automatic calling disabled, model tool calls executed by a bounded server loop, function responses returned in the conversation. The visual factory, crew animation and physical inspection activity remain illustrative, not sensor telemetry or an executed real-world inspection.
