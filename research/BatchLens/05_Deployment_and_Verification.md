# BatchLens deployment and verification

BatchLens is publicly deployed on Google Cloud Run. The browser factory-story flow has completed with real Gemini image extraction and a saved inspection proposal.

**Live demo:** https://batchlens-hk3hxwi5na-as.a.run.app/

## Target configuration

- Project: `yourstorieslive-i18n`.
- Service: `batchlens`, region `asia-southeast1`.
- Named Firestore database: `batchlens`, separate from the existing project’s default database.
- Deployed model: `gemini-3.5-flash-lite`, global Vertex AI endpoint.
- Authentication to Gemini: Cloud Run service account, without a downloaded service-account key or browser API key.
- Runtime: `batchlens-runtime`; model inference permissions and conditional access to the BatchLens database.
- Builder: `batchlens-builder`; write access to BatchLens’s image repository, read access to its build source bucket, and build logging.
- Capacity: minimum zero and maximum two instances, one CPU, 512 MiB memory, concurrency 20.
- Model-call ceiling: 100/day across cases; eight attempts per case. These are usage controls, not a monetary cap.
- Case access expires after 24 hours. Firestore TTL on `batchlens_cases.expires_at` is ACTIVE for eventual cleanup.

A separate project was attempted but Google rejected creation because the account project quota was exhausted. The owner then approved a separate service and database in the existing project, together with the scoped permissions and public prototype access.

## Verification record

- Local production frontend build: passed.
- Local backend suite: 10 passed, including Cloud Run refusal to use authored mode when live configuration is missing.
- Dedicated service accounts, image repository, build bucket and named Firestore database: created.
- Cloud build `17d1db4d-92f6-4e2a-b2c6-ef0a585762c9`: SUCCESS.
- Cloud Run revision `batchlens-00003-6f2`: serving 100% of traffic (17 October factory-floor update).
- Image: `asia-southeast1-docker.pkg.dev/yourstorieslive-i18n/batchlens/app:20261015154027`.
- Hosted URL: https://batchlens-hk3hxwi5na-as.a.run.app/
- Hosted API workflow: PASSED at 2026-10-15 15:43 UTC (23:43 Singapore). E2 → B101; E3 → CAP-17; unreadable E6 → null; recovered E7 → B104. All four responses came from Gemini, with response IDs and usage metadata.
- Extraction alone left scope unchanged; human confirmations produced 1,500 included units, zero unresolved, and 500 outside the recorded connection. HTML and CSV exports and saved-case reload passed.
- Evidence: [live verification JSON](../../docs/live-cloud-verification.json) and [browser handover screenshot](../../docs/live-cloud-handover.jpg).
- `/api/health` returns Firestore storage and Gemini mode. This route avoids Cloud Run’s reserved `/healthz` path.
- Browser verification on the public URL: passed. E2 returned B101, E3 returned CAP-17, E7 returned B104. Human review connected S4 to B104, then saved a 1,500-unit proposal with zero unresolved units. Report and CSV download links appeared. Reload preserved the reviewed case and filed proposal.

## Operating the prototype

Keep billing, Cloud Run, Firestore and Vertex AI active through evaluation. A cold start can occur after idle periods because minimum instances is zero. The verification run’s first model request took 26.9 seconds; subsequent requests took 1.6–1.8 seconds. These are observations from one run, not a latency guarantee. Allow time for the first scan during the demo. Check `/api/health` for deployment configuration, but use a fresh evidence scan to verify actual model access. Configuration alone does not prove inference succeeds.

From the source directory with Python dependencies installed, run `python scripts/live_smoke.py <service-url>` to test real E2, E3, E6 and E7 extraction, human confirmations, the final scope, reload and report exports. This consumes four model calls. Save the non-secret JSON result as verification evidence.

The deployment source is `deploy/cloudrun.sh`. Its setup, deploy and publish stages are separate. Rebuild and deploy from the saved source when changing code; retain the same service URL for the submission.

## Model lifecycle

Google’s [model lifecycle page](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-versions) lists Gemini 3.5 Flash-Lite as available until at least July 21, 2027. The deployed model passed live image extraction in the browser. Recheck model availability before making future updates.

## Cost and availability controls

The hosted prototype uses a trial-funded billing account. It may become unavailable when its trial or credits end; verify availability through the evaluation period. Keep the account on its existing trial configuration unless the owner explicitly approves a billing change. Private billing balances and account evidence are intentionally kept out of this public repository.

An account-wide early-warning budget is configured. Budget alerts are not spending caps. Cloud Run is configured for zero minimum and two maximum instances; real model attempts are limited to 100 per day and eight per case. These usage controls do not guarantee a monetary ceiling.
