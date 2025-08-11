# AEGIS System Certification Checklist

This checklist is a template for auditing an ASI system against the AEGIS framework, as described in **Section 75**. The goal is to achieve a specific AEGIS Safety Level (ASL).

---

## Certification Details

*   **System ID:** [Unique System Identifier]
*   **Version:** [System Version]
*   **Target ASL:** [ASL-0 to ASL-5]
*   **Audit Date:** [YYYY-MM-DD]
*   **Auditor(s):** [Names of Auditors]

---

## Part I: Foundational Principles & Formalisms

| Section | Item | Status | Evidence / Link to Document | Notes |
|---|---|---|---|---|
| Sec 2 | Threat Model defined and approved? | [ ] Pass [ ] Fail [ ] N/A | [Link to `threat_model.md`] | |
| Sec 3 | Formal notation document complete? | [ ] Pass [ ] Fail [ ] N/A | [Link to `notation.md`] | |
| Sec 30 | Safety metrics defined and calibrated? | [ ] Pass [ ] Fail [ ] N/A | [Link to `metrics.md`] | |
| Sec 91 | Risk assessment matrix complete? | [ ] Pass [ ] Fail [ ] N/A | [Link to `risk_assessment.md`] | |

## Part II: Core Agent Architecture & Training

| Section | Item | Status | Evidence / Link to Document | Notes |
|---|---|---|---|---|
| Sec 5 | USF specified and implemented? | [ ] Pass [ ] Fail [ ] N/A | [Link to `usf_spec.yml`] | |
| Sec 6 | SVAU design formally verified? | [ ] Pass [ ] Fail [ ] N/A | [Link to proof/analysis] | |
| Sec 7 | Corrigibility proofs reviewed? | [ ] Pass [ ] Fail [ ] N/A | [Link to proof] | |
| Sec 12 | Interpretability metrics meet threshold? | [ ] Pass [ ] Fail [ ] N/A | [Link to test results] | |
| ... | ... | ... | ... | |

## Part III: Runtime Verification, Containment & Control

| Section | Item | Status | Evidence / Link to Document | Notes |
|---|---|---|---|---|
| Sec 14 | Monitor decentralization and BFT guarantees analyzed? | [ ] Pass [ ] Fail [ ] N/A | [Link to analysis doc] | |
| Sec 15 | Secure bootchain verified via hardware attestation? | [ ] Pass [ ] Fail [ ] N/A | [Link to logs/attestation report] | |
| Sec 16 | Shutdown protocol tested and verified? | [ ] Pass [ ] Fail [ ] N/A | [Link to test results] | |
| Sec 31 | Sandbox escape-resistance tests passed? | [ ] Pass [ ] Fail [ ] N/A | [Link to red-team report] | |
| ... | ... | ... | ... | |

## Part IV: Scalable Oversight & Human-in-the-Loop

| Section | Item | Status | Evidence / Link to Document | Notes |
|---|---|---|---|---|
| Sec 20 | Recursive oversight amplification process documented? | [ ] Pass [ ] Fail [ ] N/A | [Link to process doc] | |
| Sec 32 | Human-agent interaction protocols tested with operators? | [ ] Pass [ ] Fail [ ] N/A | [Link to user study results] | |
| ... | ... | ... | ... | |

## Part V: Governance, Ethics & Deployment

| Section | Item | Status | Evidence / Link to Document | Notes |
|---|---|---|---|---|
| Sec 72 | Deployment gates criteria met for current stage? | [ ] Pass [ ] Fail [ ] N/A | [Link to gate review report] | |
| Sec 77 | Incident response playbook drilled and validated? | [ ] Pass [ ] Fail [ ] N/A | [Link to drill report] | |
| Sec 110 | Ethics Review Board charter approved and board seated? | [ ] Pass [ ] Fail [ ] N/A | [Link to charter] | |
| ... | ... | ... | ... | |

---

## Final Certification Decision

*   [ ] **Certification Granted** for **ASL-[X]**
*   [ ] **Provisional Certification Granted** (with remarks)
*   [ ] **Certification Denied**

### Remarks / Required Remediations:

[Auditor's summary of findings and required actions before next review.]

### Sign-off:

*   **Lead Auditor:** _________________________
*   **Date:** _________________________
