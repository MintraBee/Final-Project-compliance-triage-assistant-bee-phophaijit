# Compliance Triage and Owner Routing Assistant

## Context, User, and Problem

This project supports a compliance coordinator, project coordinator, or operations manager working in a regulated organization such as biotechnology, healthcare, or life sciences.

Compliance issues often appear in unstructured meeting notes, audit discussions, HR conversations, legal reviews, or operational updates. A coordinator may need to identify the compliance domain, determine the correct owner, locate a relevant policy or SOP, assign escalation priority, and create a tracker-ready follow-up item.

This process is often manual, inconsistent, and dependent on tribal knowledge.

## Solution and Design

I built a small Streamlit application that converts one unstructured compliance note into a structured triage output.

The tool returns:

- Domain
- Suggested owner
- Escalation level
- Policy reference
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