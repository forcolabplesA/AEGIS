# run_pcm_demo.py

from typing import Set, Dict, List

from aegis_v2.core.pcm import Capability, Action, PolicyEnforcementPoint

def run_test_scenario(pep: PolicyEnforcementPoint, policy_name: str, policy: Set[Capability], actions: List[Action]):
    """Helper function to run a set of tests for a given policy."""
    print(f"--- Running Scenario: {policy_name} ---")
    policy_str = ", ".join(c.name for c in policy) or "None"
    print(f"Policy: {{{policy_str}}}")

    for action in actions:
        is_allowed = pep.is_allowed(action, policy)
        result = "ALLOWED" if is_allowed else "DENIED"
        print(f"  - Action: {action.type:<15} -> {result}")
    print("-" * 40)


if __name__ == "__main__":
    print("--- Initializing PCM Demonstration ---")

    # 1. Define the Capability Lattice
    # Define capabilities from the most general (parent) to the most specific (child).
    CAP_FS_ACCESS = Capability("fs_access")
    CAP_FS_READ = Capability("fs_read", parent=CAP_FS_ACCESS)
    CAP_FS_WRITE = Capability("fs_write", parent=CAP_FS_READ)  # write implies read

    CAP_NET_ACCESS = Capability("net_access")
    CAP_NET_READ = Capability("net_read", parent=CAP_NET_ACCESS)
    CAP_NET_WRITE = Capability("net_write", parent=CAP_NET_READ) # write implies read

    CAP_INFERENCE = Capability("inference") # A standalone capability

    # A map of all defined capabilities, used by the PEP.
    capability_map = {
        cap.name: cap for cap in [
            CAP_FS_ACCESS, CAP_FS_READ, CAP_FS_WRITE,
            CAP_NET_ACCESS, CAP_NET_READ, CAP_NET_WRITE,
            CAP_INFERENCE
        ]
    }
    print("Capability Lattice Defined.")

    # 2. Initialize the Policy Enforcement Point
    pep = PolicyEnforcementPoint(capability_map)
    print("Policy Enforcement Point Initialized.\n")

    # 3. Define Policies to test
    policy_fs_read_only = {CAP_FS_READ}
    policy_net_full = {CAP_NET_WRITE}
    policy_inference_only = {CAP_INFERENCE}
    policy_nothing = set()

    # 4. Define Actions to test
    actions_to_test = [
        Action("inference", payload={}),
        Action("fs_read", payload={'file': '/data/log.txt'}),
        Action("fs_write", payload={'file': '/data/config.txt', 'content': '...'}),
        Action("net_read", payload={'url': 'example.com'}),
        Action("net_write", payload={'url': 'example.com', 'data': '...'}),
        Action("execute_arbitrary_code", payload={}) # An unknown action type
    ]

    # 5. Run Demonstration Scenarios

    # Scenario 1: A very restrictive policy that only allows inference.
    run_test_scenario(pep, "Inference-Only Policy", policy_inference_only, actions_to_test)

    # Scenario 2: A policy that grants fs_read.
    # Should allow fs_read and fs_access (implied), but not fs_write.
    run_test_scenario(pep, "Filesystem Read-Only Policy", policy_fs_read_only, actions_to_test)

    # Scenario 3: A policy that grants net_write.
    # Should allow net_write, net_read (implied), and net_access (implied).
    run_test_scenario(pep, "Full Network Access Policy", policy_net_full, actions_to_test)

    # Scenario 4: An empty policy.
    # Should deny everything except inference if inference is the default. Let's assume no default.
    # Our current PEP has no default, so it should deny everything.
    run_test_scenario(pep, "Empty Policy", policy_nothing, actions_to_test)


    print("--- PCM Demonstration Complete ---")
