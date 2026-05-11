import streamlit as st
import json
import os
from dotenv import load_dotenv
import anthropic

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
You are a compliance triage assistant.

Analyze the compliance note below.

Return ONLY one domain from this list:

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


# Issue summary
def generate_summary(note):

    if len(note) > 150:
        return note[:150] + "..."

    return note.strip()


# Next action
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


# Streamlit UI
st.title("Compliance Tracker Assistant")

st.write(
    "Enter a compliance-related note below. "
    "This tool supports first-pass triage only. "
    "Human review is required."
)

user_input = st.text_area("Compliance Note")


if st.button("Run Triage"):

    if not user_input.strip():

        st.warning(
            "Please enter a compliance note before running triage."
        )

    else:

        with st.spinner("Analyzing with Claude..."):

            domain = classify_with_claude(user_input)

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