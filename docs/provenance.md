# Asset provenance

All manufacturer names, complaint text, identifiers, quantities, and evidence are original synthetic case material. Source records are under `backend/scenarios/bottles_v1/assets/`; their rendering script is `scripts/create_evidence.py`. They describe an authored case, not a real supplier or incident.

The BatchLens SVG mark, favicon (`frontend/public/favicon.svg`), interface components, trace graph, and CSS styling were authored for this project. Lucide supplies general UI icons under its ISC license. React and Vite are MIT-licensed dependencies. Google Fonts supplies DM Sans and Manrope; the current CSS loads them from Google with system-font fallbacks.

## Product photograph

Saved asset: `frontend/public/assets/bottles-studio.png`.

Created with the built-in image generation tool. It is illustrative artwork and is never supplied to the extraction model as evidence. The UI explicitly labels it illustrative.

Exact generation prompt:

> Use case: product-mockup. Asset type: product photograph for BatchLens, a fictional manufacturing quality investigation app. Create an elegant editorial studio photograph of two reusable matte stainless steel water bottles, one warm ivory upright bottle with a dark forest-green ribbed screw cap, one pale sage bottle lying horizontally with its detached cap beside it. A few tiny water droplets near the detached cap suggest a leak investigation, no dramatic damage. Warm light gray seamless background, soft natural directional light, realistic tactile powder-coated metal, restrained industrial product styling. Landscape composition, bottles grouped in the center with breathing room, premium catalog photography. No branding, no text, no labels, no watermark. This is an illustrative synthetic product image, not evidence of a real defect.

The original tool output was copied into the project. Evidence documents were generated separately from authored records, so no generated visual text determines the expected trace outcome.

## Northstar Night Shift — 15 October 2026
Original procedural Three.js factory, robot Pip, crew, forklift, drone, conveyor, animated scanner, station labels, and SVG Pip portrait authored for BatchLens. No Village of Shadows assets or source code copied; the referenced chat informed the use of an explorable world and state-driven characters. Characters are scripted guides, explicitly labeled; the scene is illustrative, not a live factory digital twin. Three.js 0.180.0 (MIT) is the rendering dependency, loaded in a separate chunk.

The factory-room expansion adds original animated SVG portraits for Mira and Sol, a source-scanning workbench, pinned evidence cards, a blueprint trace, shipment crate manifests, an inspection ticket and a shift journal. All are code-native artwork. Scanner motion reflects an in-flight extraction request; it does not imply live Gemini in authored demo mode. Source images and source quotations remain unchanged.

## Pitch deck night-shift redesign — 17 October 2026

The pitch uses a generated cinematic factory illustration (`docs/submission/night-shift-art.png`) as cover and closing atmosphere. It is illustrative and does not depict a real plant or replace product evidence. The original app SVG portraits of Mira, Sol and Pip were rendered to PNG without redesign. `factory-motion.gif` uses browser-recorded frames of the real app's animated factory. Product evidence screenshots remain distinct from the illustration.

The native Google Slides deck retains organizer branding and required subject sections, with a midnight-green, mint and amber treatment matching BatchLens. Its factory GIF provides motion in supported presentation playback; PDF exports are static.
