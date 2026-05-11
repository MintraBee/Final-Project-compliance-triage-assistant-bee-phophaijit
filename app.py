import streamlit as st
import json

# Load owner registry
with open("owners.json", "r") as f:
    owners = json.load(f)

# Load policy registry
with open("policies.json", "r") as f:
    policies = json.load(f)


# Simple classification logic
def classify_note(note):
    note = note.lower()

    if "payroll" in note or "employee" in note or "california" in note:
        return "employment"

    elif "biosafety" in note or "lab" in note or "inspection" in note:
        return "biosafety"

    elif "hipaa" in note or "privacy" in note or "health information" in note:
        return "data_privacy"

    elif "contract" in note or "vendor" in note:
        return "contracts"

    elif "policy" in note or "handbook" in note:
        return "policy_review"

    else:
        return "unclear"


# Escalation logic
def assign_escalation(domain):
    if domain in ["data_privacy", "employment"]:
        return "High"

    elif domain in ["biosafety", "contracts", "policy_review"]:
        return "Medium"

    else:
        return "Low"


# Issue summary logic
def generate_summary(note):
    return note.strip()


# Recommended next action logic
def next_action(domain):
    actions = {
        "employment": "Confirm payroll or HR compliance issue before the next payroll cycle.",
        "biosafety": "Coordinate inspection follow-up with Lab Operations or the Safety Officer.",
        "data_privacy": "Escalate to Legal and IT Security for privacy review.",
        "contracts": "Clarify ownership and route the contract for Legal and Finance review.",
        "policy_review": "Review policy documentation and assign a responsible owner.",
        "vendor_risk": "Coordinate cross-functional review with Procurement, Legal, and IT Security.",
        "unclear": "Request additional context before taking action."
    }

    return actions.get(domain, "Human review required.")


# App UI
st.title("Compliance Tracker Assistant")

st.write(
    "Enter a compliance-related note below. "
    "This tool supports first-pass triage only. "
    "Human review is required."
)

user_input = st.text_area("Compliance Note")

if st.button("Run Triage"):

    if not user_input.strip():
        st.warning("Please enter a compliance note before running triage.")

    else:
        domain = classify_note(user_input)
        owner = owners[domain]["owner"]
        policy = policies[domain]["policy_reference"]
        escalation = assign_escalation(domain)
        summary = generate_summary(user_input)
        action = next_action(domain)

        st.subheader("Triage Output")

        st.write(f"**Domain:** {domain}")
        st.write(f"**Issue Summary:** {summary}")
        st.write(f"**Suggested Owner:** {owner}")
        st.write(f"**Escalation Level:** {escalation}")
        st.write(f"**Policy Reference:** {policy}")
        st.write(f"**Recommended Next Action:** {action}")
        st.write("**Human Review:** Required before action")