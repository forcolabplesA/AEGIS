# run_demo.py

import datetime
from typing import List, Any, Dict

# --- Import AEGIS Core Components ---
from aegis.core.agent import (
    SafetyFirstRLAgent,
    State,
    Action,
    PolicyModel,
    FallbackPolicy,
    AuditLogger,
    ConsensusMechanism,
)
from aegis.core.usf import ConfigurableUSF
from aegis.core.monitors import (
    RuleBasedMonitor,
    ModelBasedMonitor,
    AnomalyDetectionMonitor,
)

# --- Mock Implementations for the Demonstration ---

class MockPolicyModel(PolicyModel):
    """A mock policy model that returns a pre-defined action for the demo."""
    def __init__(self, action_to_return: Action):
        self.action_to_return = action_to_return
        print(f"Initialized MockPolicyModel to propose: {self.action_to_return}")

    def compute_action_distribution(self, state: State) -> Any:
        # In a real system, this would return a complex distribution object.
        return "mock_distribution"

    def quantilized_sample(self, distribution: Any) -> Action:
        # The demo hijacks this to return the action we want to test.
        return self.action_to_return

    def update(self, trajectory: List[Dict[str, Any]]):
        print("\n--- PolicyModel.update() called ---")
        print(f"Updating model with {len(trajectory)} data points from the buffer.")
        print("This would involve a constrained optimization process (Sec 8).")
        print("--- End of Update ---\n")

class MockFallbackPolicy(FallbackPolicy):
    """A mock fallback policy that always returns a pre-defined safe action."""
    def get_action(self, state: State) -> Action:
        return Action("do_nothing_safely")

class ConsoleAuditLogger(AuditLogger):
    """A mock audit logger that prints log entries to the console for clarity."""
    def log(self, entry: Dict[str, Any]):
        entry["timestamp"] = datetime.datetime.now().isoformat()
        print("\n--- AUDIT LOG ---")
        for key, value in sorted(entry.items()):
            print(f"  {key:<20}: {value}")
        print("--- END LOG ---\n")


# --- Main Demonstration Logic ---

def run_simulation_step(agent: SafetyFirstRLAgent, state: State, proposed_action: Action):
    """Helper function to run and print a single step of the simulation."""
    print("="*80)
    print(f"SCENARIO: Agent is in State '{state}' and proposes Action '{proposed_action}'")
    print("="*80)

    # Set the action that the mock policy model will propose for this step.
    agent.policy_model.action_to_return = proposed_action

    # The agent performs its safety-gated step.
    final_action = agent.step(state)

    print(f"\n>>> Final action executed by agent: {final_action}\n")
    print("_"*80 + "\n")


if __name__ == "__main__":
    print("--- Initializing AEGIS Demonstration System ---")

    # 1. Initialize the USF from the configuration file created earlier.
    usf = ConfigurableUSF(config_path="usf_config.yml")

    # 2. Initialize an ensemble of diverse monitors.
    monitors = [
        RuleBasedMonitor(rules=[{"feature": "action.data", "operator": "contains", "value": "delete"}]),
        ModelBasedMonitor(model_path="/path/to/mock/safety_model.pkl"),
        AnomalyDetectionMonitor(anomaly_threshold=0.9),
    ]

    # 3. Initialize the consensus mechanism (now requires unanimous consent)
    consensus = ConsensusMechanism()

    # 4. Initialize the other mock components.
    fallback_policy = MockFallbackPolicy()
    audit_logger = ConsoleAuditLogger()

    # 5. Initialize the main agent with all its dependencies.
    agent = SafetyFirstRLAgent(
        policy_model=MockPolicyModel(Action("initial_action")), # The proposed action is overridden each step.
        usf=usf,
        monitors=monitors,
        consensus_mechanism=consensus,
        fallback_policy=fallback_policy,
        audit_logger=audit_logger,
    )

    print("\n--- AEGIS Initialization Complete. Starting Simulation Scenarios. ---\n")

    # --- Scenario 1: A clearly safe action ---
    # Expected: USF passes, all monitors pass, agent executes the proposed action.
    run_simulation_step(
        agent=agent,
        state=State(100),
        proposed_action=Action("perform_safe_calculation")
    )

    # --- Scenario 2: An action that violates a hard rule ---
    # Expected: RuleBasedMonitor votes DENY, consensus fails, agent executes fallback action.
    run_simulation_step(
        agent=agent,
        state=State(100),
        proposed_action=Action("user_wants_to_delete_files")
    )

    # --- Scenario 3: A state that the predictive model dislikes ---
    # Expected: ModelBasedMonitor votes DENY, consensus fails, agent executes fallback action.
    run_simulation_step(
        agent=agent,
        state=State(-50), # The mock model monitor is configured to deny negative states.
        proposed_action=Action("allocate_resources")
    )

    # --- Scenario 4: A structurally anomalous action ---
    # Expected: AnomalyDetectionMonitor votes DENY, consensus fails, agent executes fallback action.
    run_simulation_step(
        agent=agent,
        state=State(100),
        proposed_action=Action("this is an unusually long and strange action that might be a disguised attempt to do something harmful and has a weird structure")
    )

    # For Scenario 5 (USF failure), we would need to configure a USF component to fail.
    # The current mock USF always returns the same value. A full test suite would have
    # a USF config specifically for this case. We will describe it instead for this demo.
    print("="*80)
    print("SCENARIO 5: Action fails USF pre-check.")
    print("If the USF score itself is below the threshold, the agent immediately uses the")
    print("fallback policy without even consulting the monitors. This is the first line of defense.")
    print("="*80 + "\n")


    # Finally, demonstrate the learning step on the buffer of trajectories collected.
    agent.learn_from_buffer()
