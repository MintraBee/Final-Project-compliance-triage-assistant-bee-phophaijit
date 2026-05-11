# Compliance Tracker Assistant

A GenAI-powered workflow assistant for first-pass compliance triage in regulated organizations.

Live application:

[Compliance Tracker Assistant](https://bee-compliance-tracker.streamlit.app?utm_source=chatgpt.com)

---

## Context, User, and Problem

This project supports a compliance coordinator, project coordinator, operations manager, or cross-functional program manager working in regulated industries such as biotechnology, healthcare, or life sciences.

Compliance issues often appear in:

- meeting notes
- audit findings
- HR escalations
- legal reviews
- vendor discussions
- operational conversations

These updates are often written in messy, unstructured language and may involve multiple stakeholders.

A coordinator typically must manually:

1. read the note
2. identify the compliance domain
3. determine ownership
4. search for relevant policies or SOPs
5. assign escalation priority
6. create tracker-ready follow-up actions

This process is often:

- time consuming
- inconsistent
- dependent on tribal knowledge
- vulnerable to missed ownership or delayed escalation

When compliance issues are not handled consistently, organizations may face:

- audit findings
- operational delays
- policy gaps
- regulatory exposure

---

## Solution and Design

I built a Streamlit application called **Compliance Tracker Assistant**.

The application takes one unstructured compliance note and converts it into a structured compliance triage output.

The tool returns:

- Domain classification
- Issue summary
- Suggested owner
- Escalation level
- Policy reference
- Recommended next action
- Human review requirement

### Workflow Architecture

```text
Raw Compliance Note
↓
Claude (Anthropic API)
↓
Controlled Owner + Policy Registries
↓
Structured Triage Output
```

### Key Design Decision

Claude is only used for:

- interpreting messy natural language
- identifying the compliance domain

Deterministic business controls are used for:

- owner routing
- policy references
- escalation logic

This reduces hallucination risk and keeps the workflow auditable.

### Core Files

- `app.py` → Streamlit application and Claude integration
- `owners.json` → Owner routing registry
- `policies.json` → Policy reference registry
- `sample_inputs.md` → Evaluation scenarios
- `evaluation.md` → Detailed evaluation results

---

## Why GenAI Is Useful

Compliance notes are rarely structured.

They often contain:

- incomplete context
- multiple stakeholders
- inconsistent wording
- operational ambiguity

Traditional keyword matching often fails.

Claude helps interpret these messy notes and classify them more consistently.

However, business routing remains deterministic to maintain governance and compliance controls.

---

## Evaluation and Results

This project was evaluated using **10 synthetic enterprise compliance scenarios** covering:

- Employment compliance
- Biosafety operations
- Data privacy incidents
- Contract review
- Policy governance
- Vendor risk
- Ambiguous inputs
- Multi-domain escalation scenarios

### Baseline

Baseline workflow:

Manual or spreadsheet-based triage using memory, keyword matching, and internal documentation.

### Baseline Performance

Correct domain classification:

**5/10 cases (50%)**

Common failures:

- inconsistent ownership routing
- privacy issues misclassified
- vendor risks routed incorrectly
- escalation inconsistencies

### Compliance Tracker Assistant Performance

After prompt refinement:

Correct domain classification:

**9/10 cases (90%)**

Output completeness:

**10/10 cases (100%)**

Ambiguous input handling:

**2/2 ambiguous scenarios safely escalated**

### Key Improvement

Compared with the baseline:

- Domain classification improved from **50% → 90%**
- Output completeness improved from **~60% → 100%**
- Ambiguous input handling improved from guessing to safe escalation

### Known Limitations

The assistant still struggles with:

#### Multi-Domain Notes

Some enterprise notes require routing to multiple owners.

#### Policy Gaps

If no matching policy exists, human review remains necessary.

#### Enterprise Knowledge Limits

Current policy references are synthetic and not connected to a live enterprise knowledge base.

---

## Human Oversight

This system:

- does not provide legal advice
- does not make final compliance decisions
- does not autonomously escalate issues

All outputs require human review before action.

---

## Artifact Snapshot

The working artifact is a deployed Streamlit application.

### Example: Vendor Risk Escalation

A third-party software vendor scenario was submitted through the application.

The assistant correctly returned:

- Domain: Vendor Risk
- Suggested Owner: Procurement / Legal / IT Security
- Escalation Level: Medium
- Policy Reference: Vendor Risk Review Procedure
- Recommended Next Action: Coordinate cross-functional review

This demonstrates how the assistant converts messy compliance notes into structured, tracker-ready outputs.

### Application Screenshot

![Vendor Risk Example](screenshots/vendor_risk.png)

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Final-Project-compliance-triage-assistant-bee-phophaijit
```

### 2. Install dependencies

```bash
py -m pip install -r requirements.txt
```

### 3. Create a `.env` file

Create a file named `.env`

Add:

```env
ANTHROPIC_API_KEY="your_api_key_here"
```

Do not commit this file.

### 4. Run the app

```bash
py -m streamlit run app.py
```

### 5. Open the local Streamlit URL

Usually:

```text
http://localhost:8501
```

---

## Final Recommendation

This tool is best used as a **first-pass compliance workflow assistant** for:

- compliance teams
- operations teams
- PMO functions
- governance programs
- audit preparation workflows

Claude handles interpretation.

Humans remain accountable for final compliance decisions.