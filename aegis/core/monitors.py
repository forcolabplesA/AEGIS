# aegis/core/monitors.py

from typing import List, Dict, Any

from aegis.core.agent import Monitor, State, Action

# --- Concrete Implementations of Diverse Monitors ---
# The AEGIS framework calls for an ensemble of diverse, independent monitors
# to reduce the chance of a single point of failure.

class RuleBasedMonitor(Monitor):
    """
    A simple monitor that checks a state-action pair against a set of hard-coded rules.
    This type of monitor is good for enforcing simple, absolute constraints.
    """
    def __init__(self, rules: List[Dict[str, Any]]):
        """
        Initializes the monitor with a set of rules.
        Example rule: {'feature': 'action.data', 'operator': 'contains', 'value': 'delete_all_files'}
        """
        self.rules = rules
        print(f"Initialized RuleBasedMonitor with {len(self.rules)} rules.")

    def evaluate(self, state: State, action: Action) -> bool:
        """
        Evaluates the action. Returns False (DENY) if any rule is violated.

        This is a mock implementation. A real one would need a structured way
        to access and evaluate features of the state and action objects.
        """
        # Mock logic: A simple rule that denies if action.data contains a forbidden keyword.
        for rule in self.rules:
            if rule.get("feature") == "action.data" and rule.get("operator") == "contains":
                forbidden_value = rule.get("value")
                if isinstance(action.data, str) and forbidden_value in action.data:
                    print(f"RuleBasedMonitor: DENY. Action '{action}' contains forbidden keyword '{forbidden_value}'.")
                    return False # DENY

        print(f"RuleBasedMonitor: ALLOW. Action '{action}' passed all rules.")
        return True # ALLOW

class ModelBasedMonitor(Monitor):
    """
    A monitor that uses a predictive model to forecast the safety of an action.
    For example, a model trained to predict whether an action will lead to a state
    with high risk or undesirable outcomes.
    """
    def __init__(self, model_path: str):
        """Initializes the monitor by loading a predictive model."""
        self.model_path = model_path
        # In a real implementation, you would load the model here, e.g.:
        # self.model = load_safety_prediction_model(model_path)
        print(f"Initialized ModelBasedMonitor with model from: {self.model_path}")

    def evaluate(self, state: State, action: Action) -> bool:
        """
        Evaluates the action using the predictive model.
        """
        # Mock logic: This monitor denies if the state data is a negative number,
        # simulating a model that predicts bad outcomes from negative states.
        if isinstance(state.data, (int, float)) and state.data < 0:
            print(f"ModelBasedMonitor: DENY. Predictive model forecasts negative outcome from state '{state}'.")
            return False # DENY

        print(f"ModelBasedMonitor: ALLOW. Predictive model forecasts safe outcome for action '{action}'.")
        return True # ALLOW

class AnomalyDetectionMonitor(Monitor):
    """
    A monitor that checks if a state-action pair is an outlier compared to a
    distribution of known-safe behaviors. This is useful for catching novel,
    unexpected behaviors that may not violate specific rules but are suspiciously
    different from normal operation.
    """
    def __init__(self, anomaly_threshold: float):
        """
        Initializes the monitor with an anomaly score threshold.
        """
        self.threshold = anomaly_threshold
        # In a real implementation, you would load a distribution model
        # (e.g., a Variational Autoencoder or a density estimator).
        print(f"Initialized AnomalyDetectionMonitor with threshold: {self.threshold}")

    def _calculate_anomaly_score(self, state: State, action: Action) -> float:
        # Mock logic: returns a high anomaly score if the action data is unusually long.
        # This simulates detecting an action that is abnormal in its structure.
        if isinstance(action.data, str) and len(action.data) > 50:
            return 0.99
        return 0.1

    def evaluate(self, state: State, action: Action) -> bool:
        """
        Evaluates the action by checking its anomaly score.
        """
        score = self._calculate_anomaly_score(state, action)
        if score > self.threshold:
            print(f"AnomalyDetectionMonitor: DENY. Anomaly score {score:.2f} exceeds threshold {self.threshold:.2f}.")
            return False # DENY

        print(f"AnomalyDetectionMonitor: ALLOW. Anomaly score {score:.2f} is within limits.")
        return True # ALLOW
