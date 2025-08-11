# AEGIS Threat Model Specification

This document provides a template for defining a threat model for an AEGIS-compliant ASI system, as specified in **Section 2** of the AEGIS framework. All safety claims are conditional on the assumptions and bounds declared in this document.

---

## T-ID: [Unique Threat Model Identifier, e.g., TM-ProjectX-v1.0]
## Date: [YYYY-MM-DD]
## Status: [Draft | Under Review | Approved]

---

## 1. Adversarial Agents (A)

Describe the set of potential adversarial agents.

| Adversary ID | Class/Description | Motivations | Capabilities Vector |
|--------------|-------------------|-------------|---------------------|
| A-001        | [e.g., External state actor, rouge internal employee, competing AI] | [e.g., Sabotage, data exfiltration, capability theft] | `C_a`: [Compute resources], `L_a`: [Access level], `M_a`: [Mimicry skill], `B_a`: [Covert bandwidth] |
| ...          | ...               | ...         | ...                 |

### Capability Vector Definitions:
*   **`C_a` (Compute):** Estimated available compute resources (e.g., in PetaFLOP/s-days).
*   **`L_a` (Access Level):** Assumed level of system access (e.g., "Unauthenticated External", "Authenticated User", "Root-level System Access").
*   **`M_a` (Mimicry Skill):** Ability to mimic human behavior or legitimate system traffic (e.g., "Low - simple scripts", "High - indistinguishable from human operator").
*   **`B_a` (Covert Channel Bandwidth):** Estimated bandwidth of potential covert channels (e.g., "Low - <1 bps", "Medium - <1 kbps", "High - >1 kbps").

---

## 2. Hardware & Network Assumptions (H)

Describe the key assumptions about the underlying hardware and network infrastructure.

*   **Trusted Hardware Root-of-Trust (Sec 15):** [e.g., "TPM 2.0 modules are present, functional, and have a secure bootchain.", "Assumed to be secure against physical tampering."]
*   **Datacenter Security:** [e.g., "Physical access to servers is restricted and monitored.", "Assumed to be resistant to side-channel attacks like..."]
*   **Network Architecture:** [e.g., "The core agent is air-gapped from the public internet.", "All external communication passes through monitored and logged gateways."]
*   **Supply Chain Security:** [e.g., "All hardware components are sourced from trusted vendors.", "No assumptions about supply chain integrity."]

---

## 3. Resources (R)

Describe the resources available to the adversary, beyond their intrinsic capabilities.

*   **Data Access:** [e.g., "Access to public internet data.", "Access to the agent's training dataset."]
*   **System Knowledge:** [e.g., "Black-box knowledge only.", "Full access to source code and architecture diagrams."]
*   **Human Resources:** [e.g., "A team of 10 expert security researchers.", "Potential for social engineering of system operators."]

---

## 4. Exclusions

Explicitly state any threats that are considered out of scope for this model.

*   [e.g., "Acts of nature (earthquakes, floods)."]
*   [e.g., "Global thermonuclear war leading to infrastructure collapse."]
*   [e.g., "Metaphysical threats (simulation hypothesis manipulation)."]

---
