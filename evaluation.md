# Evaluation and Results

## Evaluation Goal

The goal of this evaluation is to compare the compliance triage assistant against a simpler baseline workflow.

This project was tested using 10 synthetic compliance notes covering:

- Employment compliance
- Biosafety
- Data privacy
- Contract review
- Policy review
- Ambiguous inputs
- Multi-domain cases
- High-risk escalation scenarios

---

## Baseline

The baseline represents how this work is often done today.

### Manual / Keyword-Based Baseline

A coordinator reads the note and manually:

1. identifies the compliance domain
2. determines the owner from memory or spreadsheets
3. searches for relevant policy references
4. decides escalation priority
5. drafts follow-up actions

Common baseline issues:

- inconsistent outputs
- missing ownership
- escalation not always clear
- dependent on tribal knowledge

---

## Evaluation Criteria

Each test case was scored using the following rubric:

### 1. Domain Classification
Was the correct compliance domain identified?

### 2. Owner Routing
Was the issue routed to the correct owner?

### 3. Policy Reference
Was the policy suggestion relevant?

### 4. Escalation Accuracy
Was the escalation level appropriate?

### 5. Output Completeness
Did the system return all required fields?

### 6. Safe Failure Handling
Did the system avoid guessing when input was unclear?

---

## Sample Evaluation Results

| Test Case | Baseline | Assistant | Result |
|-----------|----------|-----------|--------|
| Payroll Registration | Partial | Complete | Improved |
| Biosafety Inspection | Partial | Complete | Improved |
| HIPAA Privacy Issue | Partial | Complete | Improved |
| Policy Review Delay | Partial | Complete | Improved |
| Contract Ownership | Partial | Complete | Improved |
| Ambiguous Input | Often Guessed | Returned Unclear | Safer |
| Multi-Domain Input | Inconsistent | Partial | Needs Improvement |
| Privacy Incident | Partial | Complete | Improved |
| Missing Policy | Often Missed | Flagged Gap | Improved |
| Compliance Calendar | Complete | Complete | Equivalent |

---

## Key Findings

The compliance triage assistant performed better than the baseline in:

- consistency of structured outputs
- owner routing reliability
- escalation visibility
- policy reference completeness
- handling of ambiguous inputs

---

## Failure Cases

The assistant struggled with:

### Multi-Domain Notes

Notes involving multiple compliance areas may require routing to several stakeholders.

### Highly Ambiguous Notes

Some inputs lacked enough context for confident classification.

### Policy Gaps

When no policy exists, human review remains necessary.

---

## Recommendation

This assistant should be used for first-pass compliance triage only.

A human reviewer should validate all outputs before escalation or action.