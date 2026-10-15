# BatchLens: three-minute demo video script

Target runtime: **3:00**. Record the hosted application, not localhost. This is a recording script, not a finished video.

Live app: https://batchlens-hk3hxwi5na-as.a.run.app/

Pitch: https://docs.google.com/presentation/d/1_EZO4q_fb1DqmobJcNyoKLMNwv2pT2bQ2s4mr_dYXNs/edit

## Recording setup

Use the internal browser at a desktop size, with notifications hidden and the cursor easy to follow. Keep app motion on for the opening, then pause if it distracts from source reading. Capture at 1080p when available. Record clean screen footage and voice separately for precise timing.

Check `/api/health` for `ai_mode: gemini`, then verify one fresh scan actually succeeds. Health configuration alone does not prove inference. Start a fresh case for the recording. The main story uses three Gemini calls: E2, E3 and E7. A rehearsal uses additional calls, so respect the 100/day limit.

The hosted verification observed a 26.9-second first extraction and 1.6–1.8-second later extractions. Record complete requests. If trimming waiting time, put **“AI processing wait shortened”** on screen. Never replace an error or model result with a fixture answer. Keep the source, returned candidate, Gemini label and confirmation action visible. If Gemini returns a wrong candidate, correct it transparently with a source-backed note or rerecord a fresh run. Do not describe a manual correction as a correct model extraction.

## Timed shot list and narration

### 0:00–0:18 — A quality problem worth solving

**Screen:** Open the animated factory. Orbit briefly past Pip, the moving conveyor and the crew stations. Keep the product name visible. Overlay: “Original synthetic case. Real Gemini extraction.”

**Voice:** “One leaking bottle cap. Four shipments. A missing batch reference. Which units should a quality team inspect? BatchLens turns scattered factory records into a reviewed inspection proposal. Let’s follow one investigation through Northstar’s night shift.”

### 0:18–0:48 — Mira reads the bottle label

**Screen:** Click **Review the evidence**. At Mira’s workbench, click **Scan this evidence**. Show the original E2 label, the in-flight scanner and the returned `B101` with its source quotation and Gemini provider label. Move the cursor between the document and candidate.

**Voice:** “Mira’s workbench starts with the original bottle label. This scan sends the image to Gemini on Vertex AI. The model returns batch B101 and a supporting quote. The reading stays beside its source so a reviewer can check it. A model response alone does not change our inspection scope.”

### 0:48–1:12 — The suspect component and factory ledgers

**Screen:** Click **Next: supplier report**, then **Scan this evidence**. Show `CAP-17`. Click **Next: factory ledgers**. Open E4, return, open E5 and point to S4’s blank batch. Return and click **Confirm baseline & follow the line**.

**Voice:** “The supplier report identifies component lot CAP-17 as out of tolerance. We compare that reading with the original, then inspect the production and shipment ledgers. Shipment S4 is missing its batch reference. Now I confirm the baseline. Accepted evidence, rather than an unchecked AI guess, drives the trace.”

### 1:12–1:35 — Sol makes uncertainty visible

**Screen:** Follow Sol’s schematic. Point to CAP-17, B101/B102/B104, then S4. Hold the totals long enough to read. Overlay: “1,000 connected + 500 unresolved = 1,500 proposed for inspection.”

**Voice:** “Sol traces CAP-17 through finished batches into shipments. One thousand units are connected. Another five hundred remain unresolved, so the conservative inspection proposal includes them. Five hundred have no recorded connection, which does not certify safety. Missing evidence stays visible instead of disappearing from the decision.”

### 1:35–2:05 — Recover S4’s missing link

**Screen:** Click **Recover the missing record**, then **Inspect recovered evidence** and **Extract from source**. Show E7 and Gemini’s `B104`. Pause before clicking **Confirm relationship** so viewers can see that extraction alone has not changed scope. Confirm, then click **Walk to dispatch office**.

**Voice:** “Here is the supplied recovered packing slip. Gemini reads B104 from the image. I compare the candidate and quotation with the original, then explicitly confirm the relationship. S4 now connects to the trace. We still propose inspecting fifteen hundred units. What changed is our certainty: the unresolved quantity falls to zero.”

### 2:05–2:35 — Pip saves the inspection handover

**Screen:** Show 1,500 connected and zero unresolved. Click **Write the inspection proposal**. Enter the note below and click **Save reviewed snapshot**. Click **Download report** and show the report, or show the CSV download briefly. Return to the app.

**Reviewer note:** “Inspect the 1,500 connected units. Reviewed the original label, supplier report, factory ledgers and recovered S4 slip. Connection supports inspection, not proof of a defect.”

**Voice:** “Pip prepares the inspection handover. I record my rationale and save a snapshot of the reviewed scope. The export carries the original evidence, the readings and the review decision. This is a usable handover for another reviewer, rather than an answer they must simply trust. HTML and CSV downloads preserve the result.”

### 2:35–2:50 — A working cloud application

**Screen:** Reload, return through **Crew rooms** to **03 Dispatch office**, and show the saved proposal. Briefly show the shift journal if time permits. Overlay: “Cloud Run · Vertex AI Gemini · Firestore”.

**Voice:** “Refresh, and the saved investigation remains. Cloud Run hosts the application, Gemini reads the evidence, and Firestore stores the case. The characters guide the story. Human review and deterministic tracing govern the decision.”

### 2:50–3:00 — Close with a credible next step

**Screen:** Finish on the factory, with the live demo and GitHub links. Hold the end card until 3:00.

**Voice:** “Our next step is a quality-team pilot measuring review time and mapping errors. BatchLens makes an inspection decision understandable, reviewable and ready to hand over.”

## Edit and submission checklist

- The timeline totals exactly 180 seconds. Rehearse narration within each segment, leaving short pauses for readable results. Do not accelerate confirmation clicks beyond legibility.
- Show all three real Gemini extractions and the explicit human confirmations. Do not use authored local mode footage as evidence of live AI.
- Keep the original uncut recording as evidence. Label any shortened processing waits in the final edit.
- Use captions and consistent audio. Avoid music during source reading if it competes with narration.
- Do not call all 1,500 units defective, claim savings, or imply the crew are autonomous agents. The case is synthetic and arbitrary uploads are not supported.
- Export a 3:00 video, upload to the organizer-supported host, verify judge access while signed out, then add its URL to the pitch deck’s links slide and submission form.
- The script does not create or upload a video. The recording URL remains pending until a real recording exists.
