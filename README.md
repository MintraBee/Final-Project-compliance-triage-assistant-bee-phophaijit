# Compliance Triage and Owner Routing Assistant

## Context, User, and Problem

This project supports a compliance coordinator, project coordinator, or operations manager working in a regulated organization such as biotechnology, healthcare, or life sciences.

Compliance issues often appear in unstructured meeting notes, audit discussions, HR conversations, legal reviews, or operational updates. A coordinator may need to identify the compliance domain, determine the correct owner, locate a relevant policy or SOP, assign escalation priority, and create a tracker-ready follow-up item.

This process is often manual, inconsistent, and dependent on tribal knowledge.

## Solution and Design

I built a small Streamlit application that converts one unstructured compliance note into a structured triage output.

The tool returns:

- Domain
- Issue summary
- Suggested owner
- Escalation level
- Policy reference
- Recommended next action
- Human review requirement

The current prototype uses rule-based classification and deterministic lookup files:

- `owners.json` routes each compliance domain to a suggested owner
- `policies.json` maps each domain to a policy reference
- `app.py` provides the Streamlit user interface and triage logic

This design keeps the workflow narrow, auditable, and easy to test.

## Why GenAI Is Useful

The final intended workflow uses GenAI to interpret messy or ambiguous compliance notes and classify them into structured outputs. GenAI is useful because compliance notes are often written in natural language and may not follow a consistent format.

However, the project separates model interpretation from deterministic routing logic. Owner and policy references are controlled through registry files instead of allowing the model to invent them.

## Baseline Comparison

The baseline is a simple manual or keyword-based process where a coordinator reads the note and identifies the domain, owner, policy, and escalation level from memory or by searching documentation.

The prototype improves the baseline by producing a consistent structured output and reducing missed fields.

## Setup Instructions

1. Clone or download this repository.

2. Install dependencies:

```bash
py -m pip install -r requirements.txt
```

3. Run the Streamlit app:

```bash
py -m streamlit run app.py
```

4. Open the local browser link provided by Streamlit.

## Example Input

```text
Remote employee in California may not be properly registered for payroll withholding. Need to confirm before next cycle.
```

## Example Output

```text
Domain: employment
Issue Summary: Remote employee in California may not be properly registered for payroll withholding. Need to confirm before next cycle.
Suggested Owner: People Team / Finance
Escalation Level: High
Policy Reference: Remote Work and Multi-State Employment Policy
Recommended Next Action: Confirm payroll or HR compliance issue before the next payroll cycle.
Human Review: Required before action
```

## Evaluation and Results

The project includes a synthetic evaluation set in `sample_inputs.md`. The evaluation covers clear cases, ambiguous cases, multi-domain cases, missing policy cases, and high-risk escalation cases.

Evaluation criteria include:

- Domain classification accuracy
- Owner routing accuracy
- Policy reference relevance
- Escalation level appropriateness
- Output completeness
- Safe handling of ambiguous inputs

Detailed results are documented in `evaluation.md`.

## Human Oversight and Limitations

This tool does not provide legal advice.

This tool does not make final compliance decisions.

All outputs require human review before action is taken.

Current limitations include:

- The current prototype uses simple rule-based classification
- Ambiguous notes may require manual clarification
- Multi-domain issues may require additional routing logic
- Policy references are synthetic and not tied to a real internal knowledge base
- The tool is designed for first-pass triage only

## Artifact Snapshot

The working artifact is a Streamlit app in `app.py`.

A user can enter a compliance note, click “Run Triage,” and receive a structured triage output.