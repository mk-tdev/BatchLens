# BatchLens submission checklist and judge questions

The supplied `research/requirements.txt` requires five deliverables and specifies Google AI plus Cloud Run or Firebase. The written explanation supports the submission; it does not replace the actual deck, video, repository or deployed link.

## Required deliverables

| Requirement | Action before submission |
| --- | --- |
| Pitch deck using prescribed template | Obtain the organizer’s actual template, then fill it with the problem, workflow, architecture, evidence and impact. No template was included in requirements.txt. |
| Demo video showing the solution working | Record the live flow in 03_User_Guide_and_Demo_Script.md. Include real Gemini reading and a saved proposal. |
| Deployed prototype that stays up through evaluation | Use the verified URL in 05_Deployment_and_Verification.md. Keep billing, required APIs and model access active. Test from a signed-out browser. |
| Accessible GitHub repository | Publish or share the source repository with the required audience. Verify access independently. Exclude credentials, local databases and dependencies. |
| Brief description | Adapt the short description in 01_Project_Overview.md to the submission form’s length limit. |
| Google AI and Google Cloud | Show actual Gemini extraction in the hosted Cloud Run application; cite the model and service from the deployment record. |

## Suggested deck content

Fit this material into the prescribed slide structure rather than inventing a replacement template.

1. **Problem:** scattered quality evidence makes inspection planning difficult.
2. **User and workflow:** quality managers move from complaint to sources to confirmed relationships to a handover.
3. **Product:** a factory story with three crew members and an evidence-first workbench.
4. **AI:** Gemini visual extraction with structured output, quotes, null for unreadable evidence and human confirmation.
5. **Architecture:** React and Three.js, FastAPI on Cloud Run, Gemini through Vertex AI, Firestore and deterministic tracing.
6. **Demonstration:** CAP-17, four shipments, recovered S4 mapping, 1,500-unit inspection proposal.
7. **Impact and next steps:** evidence navigation and transparent uncertainty; validate with real teams before claiming savings. Future work includes multiple cases, controlled uploads and enterprise integrations.

## Judge questions

**Is it just a game?**

The world is an interface to a working investigation. The actions read actual source images, confirm relationships, calculate quantities and save an inspection report. The characters make the process understandable; they do not replace it.

**Where is the AI?**

Gemini reads the product label, supplier report and recovered packing slip. The backend retains its identifier candidate and source quote. The crew dialogue is scripted, and the scope arithmetic is deterministic.

**Why not let the model decide everything?**

Inspection scope needs a reproducible paper trail. A visual extraction can be wrong. Human confirmation and a fixed trace algorithm make the transition from uncertain reading to accepted relationship explicit.

**Does it hallucinate the missing batch?**

The prompt asks for null when unreadable or ambiguous. The obscured slip has no readable batch answer. The reviewer resolves S4 using the supplied legible replacement and explicitly confirms the relationship. The unreadable-source live check should be included in verification.

**What impact can you prove today?**

The demo proves the workflow on a synthetic case: source reading, reviewed mapping, deterministic scope and an exportable snapshot. It does not prove production accuracy or measured cost savings. In this scenario, 1,500 of 2,000 units are proposed for inspection; recovery changes certainty rather than the conservative total.

**Are these autonomous AI agents?**

No. Mira, Sol and Pip are authored guides. The real AI component is Gemini document extraction. We avoid implying autonomous control over a factory or shipments.

**Can anyone upload factory documents?**

The MVP uses curated synthetic records and one supplied replacement slip. General upload, enterprise authentication, tenant management and ERP integration are future work.

**What happens if Gemini fails?**

The request fails visibly and no confirmed relationships change. Production configuration does not silently fall back to authored extraction.

**How is data protected?**

The demo isolates cases by a browser ownership cookie, checks request origins, validates inputs and applies action and model-call limits. Cloud credentials stay server-side. These controls are appropriate prototype foundations, not a claim of enterprise compliance.

## Claims to avoid

Do not call all 1,500 connected units defective, say S3 is certified safe, describe scenario arithmetic as measured savings, call scripted characters autonomous agents, or imply general document ingestion and real factory integrations are already shipped. Keep deployment claims aligned with the verification record.
