# Implemented architecture

Browser → FastAPI → transactional store and pure scope engine. A bounded Gemini adapter proposes candidate facts; the reviewer confirms before graph mutation. SQLite runs locally; Firestore is provided for Cloud Run.

Source artifacts are immutable packaged originals. Structured CSV facts are parsed with duplicate/quantity/reference validation. Every inclusion carries its evidence IDs. The scope engine classifies shipment lines, then sums each line exactly once. Proposals freeze scope and source/candidate snapshots.

Extraction reserves an expiring job outside the model call. The model runs outside database transactions. Failed or invalid output leaves the graph unchanged; successful candidates still require review. Mutation commands use expected revision and request deduplication. Firestore/SQLite daily counters bound real model attempts across sessions.

Implemented scope differs from the full plan: supplied evidence only; a bounded JSON investigation document instead of subcollections; no arbitrary upload or Cloud Storage; Cloud Run, Firestore and live Gemini verified on 15 October 2026. These choices retain the complete original-case workflow while keeping the first build small.
