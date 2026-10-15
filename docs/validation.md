# Validation record

15 October 2026, Singapore time. Local build only.

## Completed

- Production frontend build with TypeScript checking.
- Nine pytest tests passed, including a ten-fresh-case API flow test.
- Exact initial quantities: 1,000 included, 500 unresolved, 500 with no recorded connection.
- Exact final quantities: 1,500 included, 0 unresolved, 500 with no recorded connection.
- Inspected the original generated product image and incorporated it into the UI.
- Browser walkthrough through baseline extraction/review, trace, recovered slip, confirmation, proposal creation, and successful HTML download.
- Browser refresh retained confirmed evidence, resolved S4, and the saved proposal.
- Mobile 390px evidence search, source viewing, and Escape dismissal worked; document width equaled viewport width.
- Desktop 1440px DOM layout check showed no document overflow.
- Production security/correctness regressions cover unauthorized source/export access, CSRF headers/origin, stale requests, identical-request replay, changed-body rejection, rejected candidates, expired access, daily model admission cap, and model failure without graph mutation.

## Verification limits

The checked browser flow used the authored demo adapter. Real Gemini extraction and model latency/cost were not tested because project credentials and a model were not configured. Firestore and Cloud Run are not deployed or integration-tested. The Docker image has not been built in this environment.

The Playwright test runner was attempted but could not start because its Chromium binary was not installed. The same core workflow and mobile search were exercised through the available in-app browser. The checked-in Playwright tests can run after `npx playwright install chromium`; they are not reported as passing here.

No external usability participants or production data were used. This record establishes prototype behavior, not business savings or defect-detection performance.

## Night Shift redesign validation — 15 October 2026
- Production TypeScript/Vite build passed; Three.js lives in a lazy-loaded chunk (~132 kB gzip). Vite reports its >500 kB uncompressed chunk advisory.
- Backend suite: 9 passed.
- Browser manual full flow: evidence lab → two authored extractions → baseline confirmation → dispatch → recovered slip → extraction → human confirmation → 1,500 connected / 0 unresolved → saved proposal → report in case desk.
- Browser checked pause/resume controls and fresh-case restart. Mobile viewport 390×844: document width 390, no horizontal overflow; scene and station controls rendered.
- WebGL fallback keeps station buttons and the case desk available. Reduced-motion preference initializes the scene paused; modal dialogs pause scene activity. Background tabs skip rendering; renderer resources disposed on exit.
- E2E specs updated for the world entry and station/motion controls. Automated browser runner remains unexecuted (local Chromium not installed); the flow above was exercised through the in-app browser.

## Factory story throughout the app — 15 October 2026
Replaced the remaining corporate desk with four factory chapters and rebuilt baseline review as Mira’s sequential workbench. Manual browser verification covered both identifier scans, E4 and E5 originals with return to the same review step, baseline-to-assembly navigation, recovered E7 extraction and confirmation, dispatch scope (1,500 units), and saving the inspection handover with export links. At 390×844 the evidence room had document width 390; the workbench rendered in a scrollable single column. Shared pause was checked from a room back to the factory floor. Build and nine backend tests passed. Browser test specifications were rewritten for this flow; their standalone runner was not executed (Chromium unavailable), so browser verification remains manual.

## Cloud deployment verification — 15 October 2026

This supersedes the earlier local-only integration limits. Cloud Build succeeded and Cloud Run served the app with Firestore and real Vertex AI Gemini extraction. Ten backend tests and the production frontend build passed. The hosted smoke check verified four real image extractions, confirmation boundaries, final scope of 1,500 included / zero unresolved / 500 outside, HTML and CSV exports and persisted reload. See [verification JSON](live-cloud-verification.json). A manual browser walkthrough also completed the factory-story handover on the public service. The standalone Playwright runner is still not claimed as passing.
