# BatchLens user guide and demo script

The demo follows one complete quality investigation at Northstar Bottles. Use a fresh case and allow live model requests to finish. The source images are synthetic and safe to show in a recording.

## Before recording

Open the deployed URL recorded in `05_Deployment_and_Verification.md`. Confirm that the factory identifies live extraction rather than authored demo mode. Restart the story if another case is open. Use a desktop window wide enough to show both the source document and reading. Keep the network connected. Allow up to a minute for the first scan; the hosted verification observed a 27-second first request and roughly two-second later scans. Narrate the source-review design while waiting. A normal successful flow makes three Gemini calls; repeated scans consume the per-case and daily limits.

## Complete walkthrough

1. **Enter the night shift.** Introduce the leaking cap, four shipments and one missing link. Orbit the factory briefly and select the evidence lab. Motion can be paused from the header.
2. **Open Mira’s workbench.** Click Review the evidence. On the bottle-label step, select Scan this evidence. Compare the original with the extracted B101 candidate and quote. Mention that the result came from Gemini and still needs review.
3. **Read the supplier report.** Continue to the supplier report and scan it. Inspect the CAP-17 candidate and supporting inspection excerpt. If the reading is wrong, inspect and correct it with a source-backed reason; do not claim the model was correct after a manual correction.
4. **Read both factory ledgers.** Continue to factory ledgers. Open E4 to inspect the four production mappings, return, open E5 to see shipments and S4’s blank batch, then return. Confirm baseline and follow the line.
5. **Follow Sol’s schematic.** Inspect CAP-17, the finished batches and shipment nodes. Explain 1,000 connected units, 500 unresolved units, and 500 with no recorded connection. The inspection scope includes uncertainty: 1,500 units.
6. **Recover the missing record.** Click Recover the missing record, then Inspect recovered evidence. This adds the scenario’s supplied replacement slip; it is not an arbitrary file upload.
7. **Review S4’s new evidence.** Click Extract from source. Gemini should read B104 from E7. Compare the displayed source and quote, then confirm the relationship. The graph changes only after this action.
8. **Walk to dispatch.** The scope now has 1,500 connected units and zero unresolved. The total inspection quantity stays 1,500. Say that the missing record improved certainty, not that the AI magically reduced the inspection count.
9. **Save the handover.** Write the inspection proposal, add a rationale, and save the reviewed snapshot. Download the HTML report or CSV. The report records the reviewed scope, sources, excerpts and note.
10. **Show the shift journal.** Open the journal to demonstrate the extraction and confirmation trail. Return to the factory if time permits.

## Suggested three minute narration

**0:00–0:25 — Problem and hook**

“One leaking cap can turn into a difficult quality investigation. The answer is spread across product labels, supplier reports and shipping ledgers. This is BatchLens: a factory story that turns those records into an inspection handover.”

**0:25–1:10 — Real AI and source review**

“Mira’s workbench sends this image to Gemini. It returns an identifier and supporting quote. We keep the original next to the result so a person can verify it. Now the supplier report gives us the suspect component lot. The model proposes; the reviewer confirms.”

**1:10–1:45 — Trace and uncertainty**

“Sol’s schematic traces that lot through finished batches into shipments. One thousand units are connected, and another five hundred have no readable batch reference. Missing evidence stays in the inspection proposal rather than being guessed away.”

**1:45–2:20 — Missing link**

“The recovered packing slip gives Gemini another source to read. After I verify B104, shipment S4 becomes connected. The scope remains conservative: fifteen hundred units. What changed is the evidence certainty.”

**2:20–3:00 — Outcome and technology**

“Pip prepares the handover. I record my rationale, save the snapshot, and export the report with its sources. The app runs on Cloud Run, uses Gemini for visual extraction and Firestore for durable investigation state. The factory is illustrative, but the evidence-to-review workflow is working end to end.”

Use the final technology sentence only after checking the recorded deployment status.

## If something goes wrong

- A scan error leaves scope unchanged. Retry once after checking connectivity; do not conceal the error with a demo answer.
- An unreadable result is a valid outcome. Inspect the original or use the recovered source; do not infer a hidden identifier.
- If a case reaches its eight-attempt limit, restart the story. A global daily limit requires the owner to inspect usage before changing the deployment configuration.
- A 24-hour-old case may expire; start a fresh case. Download a report during the active session if you need to keep it.
- Reload restores the current browser-owned case. A different browser receives its own investigation.
- On a device without WebGL, use the accessible station controls and crew rooms.
