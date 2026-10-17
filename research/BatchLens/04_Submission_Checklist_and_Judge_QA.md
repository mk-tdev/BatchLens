# Submission checklist and judge questions

The current [submission pack](../../docs/submission/README.md) maps the organizer's form to the repository artifacts. Requirements were read from the [prototype submission form](https://hack2skill.com/event/aibuildercup2026/dashboard/submissions/6a5da99a444e4f43e5657a85) on 17 October 2026; the earlier supplied summary remains in [requirements.txt](../requirements.txt).

## Required deliverables

| Requirement | Current material / remaining action |
| --- | --- |
| Prescribed-template pitch deck converted to PDF, up to 5 MB | [14-slide PDF](../../docs/submission/BatchLens-Pitch-Deck.pdf), approximately 0.49 MiB. Template first/last slides retained. |
| 3–4 minute video demonstrating working functionality | **Pending final recording/upload.** Use the [current three-minute agentic demo script](06_Three_Minute_Demo_Script.md). A script is not a submitted video. |
| Accessible working prototype throughout evaluation | [Cloud Run app](https://batchlens-hk3hxwi5na-as.a.run.app/). Keep hosting, APIs, model access and inference budget available. |
| Public GitHub repository with source and supporting materials | [mk-tdev/BatchLens](https://github.com/mk-tdev/BatchLens), including research, deck, posters and exported handover. |
| Brief description including Google services, up to 1,024 characters | [Ready-to-paste text](../../docs/submission/solution-description.txt). |
| Manufacturing challenge alignment | Evidence becomes cited hypotheses, inspection recommendations and a human-reviewed handover. Gemini on Vertex AI, Cloud Run and Firestore are implemented. Firebase Hosting/Authentication are not used. |

Before submitting, verify all public links while signed out, add the actual video URL to the deck and README, and recheck the portal for changes. Publishing this repository does not submit the form.

## Judge questions

**What makes it agentic?**

Pip's investigator uses real Gemini function calling to select validated reads, archive search, lot trace, procedure, mission and scope-comparison tools. It gathers observations and produces structured source-cited findings. The server supplies a manifest and existing case context before the loop, clearly labelled as server context in the journal. After an operator result, a second Gemini run revises the hypotheses. This is bounded autonomy over investigation tools, not autonomous factory control.

**Where are human approvals?**

Image readings remain candidates until review. Baseline and S4 mappings need explicit confirmation. Missions must be approved before results can be recorded. Corrective-action handover approval requires baseline review and a report that incorporates newer operator results. No AI tool can approve facts, release stock or control machinery.

**What is the practical outcome?**

An immutable handover with reviewed scope, supporting sources, candidate readings, inspection mission results, AI findings and approved action drafts. It can be exported as HTML; CSV exports the scope. Reload preserves the case while its access is valid.

**Why build a factory game?**

The factory gives an operator a spatial route through evidence, assembly and dispatch. Missions connect station visits to real source review and result entry. The Three.js world and crew are authored; the investigation and operational clarification use Gemini. The same work can be completed through room controls.

**What does the demo prove?**

The hosted flow works on a synthetic case. Gemini proposed a CAP-17 seal-check mission. A labelled operator-entered R1 result described two leaking assemblies out of five fictional samples. Gemini cited R1 and changed the component-defect hypothesis from unresolved to supported, leaving assembly and handling unresolved. This does not prove causation, production accuracy or a defective lot. The visible change history is a server comparison of the saved Gemini assessments.

**Why not let Gemini calculate all quantities?**

Scope arithmetic should be reproducible. Confirmed relationships drive a deterministic engine. The conservative proposal includes connected plus unresolved units: 1,000 + 500 before S4 confirmation, then 1,500 + 0 after confirmation. Recovery improves certainty; it does not invent a reduction in scope.

**Does chat answer anything?**

No. Pip's operations radio uses a Gemini scope-classification step and case evidence with validated source IDs. General and mixed requests are refused. It has no mutation tools, so it cannot change approvals. Semantic filtering is not a formal guarantee against every adversarial prompt; the authority boundary is enforced in code.

**What if Gemini fails or evidence is unreadable?**

The run stops visibly and confirmed facts do not change. Partial tool results remain for review. Unreadable identifiers can return null. Hosted failures are never replaced silently with local fixtures.

**What is not built yet?**

Arbitrary uploads, real industrial procedures, ERP integration, live sensor ingestion, enterprise authentication and validated factory deployment. E8–E10 are fictional procedures/operational records for the demonstration. Physical inspections are performed by neither Pip nor the app.

**What impact will you measure?**

A pilot would compare review time, missed connections, source coverage and decision errors against an existing quality workflow. No measured savings or production performance is claimed today.

## Claims to avoid

Do not call all 1,500 connected units defective, certify S3 as safe, present scenario minutes as measured productivity, describe authored crew dialogue as AI generation, or claim a completed video before one is uploaded. Keep model, hosting and verification claims aligned with the [deployment record](05_Deployment_and_Verification.md) and [adaptive guide](11_Adaptive_Operations.md).
