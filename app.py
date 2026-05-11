import streamlit as st
import json
import os
from dotenv import load_dotenv
import anthropic

# Page configuration
st.set_page_config(
    page_title="Compliance Tracker Assistant",
    page_icon="🧭",
    layout="centered"
)

# Load environment variables
load_dotenv()

# Create Anthropic client
client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# Load owner registry
with open("owners.json", "r") as f:
    owners = json.load(f)

# Load policy registry
with open("policies.json", "r") as f:
    policies = json.load(f)


# Claude classification
def classify_with_claude(note):
    prompt = f"""
You are an enterprise compliance classification assistant.

Classify the compliance note into EXACTLY one domain.

IMPORTANT RULES:

employment:
Use ONLY for payroll, HR registration, employee tax withholding, state employment compliance, handbook employment requirements.

biosafety:
Use ONLY for laboratory safety, inspections, safety equipment, lab vendor scheduling.

data_privacy:
Use ONLY for HIPAA, privacy incidents, employee health information, data sharing, access logs, IT security concerns.

contracts:
Use ONLY for vendor contracts, procurement approvals, contract ownership, signature routing.

policy_review:
Use ONLY for policy governance, annual reviews, SOP updates, handbook review cycles, missing policy documentation.

vendor_risk:
Use ONLY for third-party software vendors, employee data storage, security documentation, vendor security assessments.

unclear:
Use ONLY when the note is too ambiguous to classify.

Return ONLY one of these exact values:

employment
biosafety
data_privacy
contracts
policy_review
vendor_risk
unclear

Compliance Note:
{note}
"""

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=20,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    domain = response.content[0].text.strip().lower()

    if domain not in owners:
        domain = "unclear"

    return domain


# Escalation logic
def assign_escalation(domain):
    if domain in ["employment", "data_privacy"]:
        return "High"

    elif domain in ["biosafety", "contracts", "policy_review", "vendor_risk"]:
        return "Medium"

    else:
        return "Low"


# Simple summary
def generate_summary(note):
    if len(note) > 170:
        return note[:170] + "..."

    return note.strip()


# Suggested action
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


# Header
st.markdown(
    """
# Compliance Tracker Assistant

Turn messy compliance notes into structured, tracker-ready follow-up items.

This tool uses Claude for first-pass classification and controlled registries for owner and policy routing.
"""
)

st.info("Human review is required before any compliance action is taken.")


# Sample scenarios
sample_note = st.selectbox(
    "Try a sample scenario",
    [
        "",
        "During the monthly operations review, HR flagged that a remote employee who relocated to California may not have completed state payroll registration. Finance noted that payroll withholding appears to be active, but legal has not confirmed whether state employment registration requirements were completed before the employee’s relocation.",
        "During a partner check-in, a healthcare collaborator asked whether employee wellness survey results were shared with external vendors. Legal has not responded yet, and IT Security noted that access logs may need review. The partner requested clarification before contract renewal discussions continue.",
        "Facilities reported that the biosafety cabinet inspection for Lab 3 is now three weeks overdue. The vendor invoice was approved, but no inspection appointment was scheduled. Lab Operations believes the Safety Officer owns the process, while Procurement believes vendor scheduling should remain with Facilities.",
        "During annual policy review, HR identified that the employee handbook still references outdated remote work guidance from last year. Compliance noted the document should have been reviewed in Q1, but legal sign-off has not been completed.",
        "A new software vendor has been selected to support laboratory inventory tracking and employee access control. Procurement approved pricing, but IT Security raised concerns about employee badge data storage and vendor security documentation. Legal has not completed the contract review.",
        "There is an open compliance issue from last week, but the meeting notes do not identify which team owns it."
    ]
)


# User input
user_input = st.text_area(
    "Compliance Note",
    value=sample_note,
    height=180,
    placeholder="Paste a compliance-related meeting note, audit note, or operational update here..."
)


# Run button
if st.button("Run Triage", type="primary"):

    if not user_input.strip():
        st.warning("Please enter a compliance note before running triage.")

    else:
        with st.spinner("Analyzing note with Claude..."):
            domain = classify_with_claude(user_input)

        owner = owners[domain]["owner"]
        policy = policies[domain]["policy_reference"]
        escalation = assign_escalation(domain)
        summary = generate_summary(user_input)
        action = next_action(domain)

        st.divider()
        st.subheader("Triage Output")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Domain")
            st.success(domain)

            st.markdown("### Escalation Level")
            st.info(escalation)

        with col2:
            st.markdown("### Suggested Owner")
            st.write(owner)

            st.markdown("### Policy Reference")
            st.write(policy)

        st.markdown("### Issue Summary")
        st.write(summary)

        st.markdown("### Recommended Next Action")
        st.success(action)

        st.warning("Human review required before action.")

        with st.expander("Why this design matters"):
            st.write(
                "Claude is used to interpret messy natural-language compliance notes. "
                "Owner routing and policy references come from controlled JSON registries, "
                "which reduces hallucination risk and keeps the workflow auditable."
            )