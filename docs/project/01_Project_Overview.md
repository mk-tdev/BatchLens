# BatchLens project overview

BatchLens helps quality teams turn scattered manufacturing evidence into a reviewable inspection scope. Its demonstration is an interactive factory story called **The Night Shift**: a leaking bottle cap starts an investigation, and the reviewer follows the evidence from a product label to component lots, finished batches and outbound shipments.

## The problem

A customer complaint rarely arrives with a complete trace. Product labels, supplier inspection reports, production ledgers and shipping records may disagree or leave gaps. A quality manager needs to know which units share the suspected component, which remain uncertain, and which records support each conclusion.

BatchLens makes those relationships inspectable. Missing information remains visible and stays in the conservative inspection proposal until it is resolved.

## What we built

An original 3D miniature factory introduces three scripted guides: Mira in the evidence lab, Sol at assembly and Pip at dispatch. Moving characters, conveyors and the scanner create a memorable entry into a practical workflow. Each chapter leads to actual evidence review rather than a separate decorative game.

Mira’s workbench sends the selected source image to Gemini for an identifier and supporting quote. The reviewer compares the candidate with the original. Confirmed identifiers connect to structured production and shipment records. A deterministic trace engine then computes the inspection scope. Pip helps the reviewer prepare an immutable proposal snapshot and download its report or CSV.

## The demonstration case

Northstar Bottles is fictional. All complaint, product, supplier and shipment records are synthetic.

| Shipment | Units | Finished batch | Component lot |
| --- | ---: | --- | --- |
| S1 | 600 | B101 | CAP-17 |
| S2 | 400 | B102 | CAP-17 |
| S3 | 500 | B103 | CAP-18 |
| S4 | 500 | Initially unreadable; recovered slip shows B104 | CAP-17 after review |

The supplier report identifies an out-of-tolerance result for CAP-17. After baseline confirmation, 1,000 units are connected, 500 are unresolved and 500 have no recorded connection. The conservative proposal includes 1,500 units. Confirming the recovered S4 slip changes the split to 1,500 connected and zero unresolved; the proposal remains 1,500. The benefit of the recovery is evidence certainty, not an invented reduction in units.

Compared with inspecting all 2,000 units, the authored scenario excludes 500 units from the proposed scope. This is a scenario calculation, not measured savings or proof that those bottles are safe.

## Why the project stands out

- A factory story makes traceability understandable to a judge who has never worked with manufacturing records.
- Gemini reads visual evidence; the application preserves the original beside the result.
- Human confirmation separates an AI candidate from a trusted relationship.
- A deterministic graph and arithmetic make the proposed scope reproducible.
- Uncertainty is an explicit category, not a gap the model fills with guesses.
- A saved report carries the reviewer’s rationale, sources and extraction excerpts into a handover.

## Intended users and impact

The initial audience is quality managers and operations teams investigating supplier or product exceptions. The intended impact is faster evidence navigation, clearer uncertainty and more defensible inspection planning. Actual time savings, accuracy across factories and operational outcomes require testing with representative customer data.

## Honest boundaries

This MVP supports one curated scenario and a supplied recovered slip. It is not connected to an ERP, live production equipment or logistics system. The crew dialogue and animations are authored; Gemini performs document extraction. The app does not automatically release shipments, diagnose every defect, issue a recall or make a final safety decision. Current implementation and live verification status are recorded in the deployment document.

## Brief submission description

BatchLens turns manufacturing evidence into a source-backed inspection plan through an interactive factory story. Reviewers work with Mira, Sol and Pip to inspect labels and supplier reports, trace component lots through finished batches, resolve a missing shipment record and save an inspection handover. Gemini extracts identifiers and supporting quotes from source images; people confirm the results before a deterministic trace engine changes scope. Unresolved shipments remain included. The Northstar Bottles demo uses synthetic evidence to show how a quality team can move from one leaking cap to a clear, auditable proposal.
