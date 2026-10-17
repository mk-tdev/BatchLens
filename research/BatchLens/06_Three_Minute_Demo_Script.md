# BatchLens: three-minute agentic demo script

**Target:** 3:00, within the organizer's required **3–4 minutes**. This is the current recording script, not a finished video. The final recording/upload URL remains pending.

**App:** https://batchlens-hk3hxwi5na-as.a.run.app/
**Track:** Manufacturing: Intelligent Operations & Industrial Efficiency
**Team:** PixelTrendAnalytics

## Recording setup

Use the internal browser and the hosted Gemini deployment. Start a fresh synthetic case and keep sufficient shared daily model budget for an initial investigation, a follow-up and one or two chat checks. There are two investigator runs per case; record all intended mission results before the second run. Do not spend it on a rehearsal in the recording case.

Record complete live responses. If editing out waits, overlay **“AI processing wait shortened”** and retain the original footage. Never swap fixtures for a failed live response. Clearly label the case, procedures and entered inspection results synthetic. Show actual tool calls, citations and approval clicks. Keep a quality-review note visible in the handover.

## Timed shot list

| Time | Screen action | Narration |
| --- | --- | --- |
| **0:00–0:15** | Open factory, move Pip briefly toward Mira. Overlay “Synthetic case. Real Gemini. Human review.” | “One leaking cap. Four shipments. A missing batch reference. BatchLens puts an AI quality investigator inside a factory story, so operators can follow the evidence and decide what to inspect.” |
| **0:15–0:45** | Open **Pip / AI investigator → Let Pip investigate**. Show journal entries for source reads, archive search, a proposed mission and comparison. | “Pip uses real Gemini on Vertex AI. Gemini chooses validated tools to read records and recover the missing slip. The journal exposes the calls and results. Readings remain candidates; the agent cannot approve facts, release stock or control machines.” |
| **0:45–1:05** | Open **Causes**, inspect a source citation, then **Scope lab**. | “Pip compares component defects, assembly variation and handling damage. Each explanation shows evidence and the next useful check. Scope scenarios use deterministic arithmetic and explicit workload assumptions. These are hypotheses and comparisons for an operator to review.” |
| **1:05–1:30** | **Missions → Read procedure E8 → Approve this demo mission**. Enter the clearly labelled example below and record it. | “Pip proposes a procedure-backed inspection mission. I approve it, then enter this synthetic seal-check result: two leaking assemblies out of five fictional samples. The record includes sample IDs, method and limitations. It does not prove the whole lot defective.” |
| **1:30–1:55** | **Reassess with operator results**. Open **Causes**, point to R1 citation and computed assessment changes. | “Now Gemini investigates again with R1 as new evidence. In our verified run, it changed the component-defect hypothesis to supported while other explanations remained unresolved. Read the current output rather than assuming it will match. The change summary compares the saved assessments.” |
| **1:55–2:15** | **Ask Pip**: ask a case-specific question; show citations. Briefly show refusal of a general query if time permits. | “The operations radio answers questions about this case, using cited evidence. General queries are outside its role. Chat has no decision-changing tools, so clarification cannot bypass the operator's approvals.” |
| **2:15–2:45** | Show baseline review of E2/E3/E4/E5 and recovered E7 confirmation, then **Handover** action approval and save proposal. Show HTML download. | “I review the original sources and confirm the shipment relationship. Fifteen hundred units are connected, with zero unresolved. I review the action drafts, add my rationale and save an exportable handover. The original evidence, mission result and review decisions travel with it.” |
| **2:45–3:00** | Reload, show saved case and finish with public app/repo links. | “Cloud Run hosts the app, Gemini powers the investigation, and Firestore preserves the case. Our next step is a quality-team pilot measuring review time and decision errors. BatchLens makes the inspection story explainable and ready to hand over.” |

If the baseline/source review needs more time, use up to **4:00** rather than rushing or concealing a required approval. Alternatively, capture the complete source review before the follow-up and edit it into the handover segment with a clear chronological transition. Reports and comparisons reflect their investigation-time state; later approvals do not rewrite old findings.

## Example operator result

Use the mission Gemini actually proposes. The following is suitable only for the fictional CAP-17 seal-check mission:

- IDs: `DEMO-CAP17-01 through DEMO-CAP17-05`
- Checked: `5`; leaking: `2`
- Interpretation: supports the mission concern, without asserting root cause.
- Observation: “Synthetic demonstration only: five fictional CAP-17 cap-and-bottle assemblies were represented in a seal-check record; two were marked leaking. No real physical test was performed. This does not distinguish cap dimensions from assembly torque or prove a lot-wide defect.”

If Gemini proposes a different allowed mission, enter an appropriate labelled synthetic result and narrate the actual behavior. Never fabricate a tool call or claim a specific model outcome before it appears.

## Suggested operational question

“What evidence is missing before we can identify the cause of the leaking cap in this BatchLens case?”

Off-topic check: “Write a poem about space.” Show the refusal. Both checks consume real model attempts; avoid unnecessary repeats.

## Final recording checklist

Show the real Gemini label, actual calls, originals and citations; human mission approval; synthetic result; follow-up findings; reviewed scope; saved/exported handover and persisted reload. Caption speech and disclose shortened processing waits. Do not claim lot-wide defects, certified safety or measured savings. Upload the final **3–4 minute** video to an organizer-supported host, test public access while signed out, then add its actual URL to the deck, README and submission form.
