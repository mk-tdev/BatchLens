# Playable factory floor

The factory is now a third-person investigation space. Select **Enter factory · Play as Pip** to expand the floor to the viewport. Walk with WASD, arrow keys, or the on-screen directional pad. Drag to orbit the following camera and scroll to adjust distance. Press E or the interaction button when near a station. Escape or Leave factory floor returns to the overview.

Mira's evidence station opens source review, Sol's assembly station opens the batch trace, and dispatch opens the next applicable recovery or handover step. These actions use the same case, confirmation and persistence APIs as the crew rooms. Walking does not run Gemini or consume model calls. The operator must explicitly start a scan.

The floor includes receiving storage, production conveyors, utility tanks, dispatch pallets, pedestrian aisles, moving bottles, crew, a forklift and Pip. Equipment and floor boundaries constrain movement. A minimap shows the operator and three stations. Objectives advance only from confirmed baseline, recovered shipment relationship and a saved inspection proposal; there are no points for accepting unverified AI output. Pause stops both world motion and walking. Crew-room buttons remain an alternative to spatial navigation.

This is an illustrative, synthetic factory story, not a measured facility digital twin, operational telemetry system or safety simulator. The animated machinery is authored. Gemini readings, human confirmations, trace computations and saved inspection snapshots remain separate from that illustration.

## Pitch template alignment

The organizer's cover artwork and closing artwork are retained. Cover team: PixelTrendAnalytics. Team leader: Muthukumar Arunachalam. The interior slides follow the template sequence: idea, opportunities (difference, solution, USP), features, process flow, optional wireframes, architecture, technologies, optional cost, snapshots, performance, future and links. The optional cost slide explicitly says a pilot estimate has not yet been measured. Performance figures describe the previously observed synthetic-case run, not production benchmarks. The 3-minute demo link remains pending while recording is paused.

## Verification, 17 October 2026

- TypeScript and production build passed; 10 backend tests passed.
- Internal-browser checks: enter/exit, camera following, keyboard movement beyond the original front aisle, workbench collision, and proximity interaction opening Mira's existing workbench.
- Local authored-mode regression from that interaction: scan E2/E3, open E4/E5, confirm baseline, recover and confirm E7, save the 1,500-unit proposal, reload, and verify 3/3 objectives with zero unresolved units. This check used authored extraction; it is not additional evidence of live Gemini performance.
- All 14 pitch slides exported and visually checked. Corrected the optional cost heading to prevent overlap. Organizer first/last artwork restored, editable cover details filled, and playable-floor screenshot included.

- Deployed commit `fd005cc` as Cloud Run revision `batchlens-00003-6f2`, serving 100% of traffic. Verified the existing submission URL, retained live Gemini case (1,500 connected / 0 unresolved), playable floor and dispatch E interaction opening the handover. No new inference was required for this frontend-only deployment check. Existing runtime, access and usage settings were retained.
