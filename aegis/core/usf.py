# aegis/core/usf.py

import yaml
import math
from abc import ABC, abstractmethod
from typing import Dict, Any

from aegis.core.agent import UniversalSafetyFunctional, State, Action

# --- Interfaces for USF Components ---

class BaseUSFComponent(ABC):
    """Abstract base class for a component of the USF."""
    def __init__(self, params: Dict[str, Any]):
        self.params = params
        print(f"Initialized {self.__class__.__name__} with params: {params}")

    @abstractmethod
    def calculate(self, state: State, action: Action) -> float:
        """Calculates the component's contribution to the USF score."""
        pass

# --- Concrete Implementations of USF Components (Placeholders) ---
# In a full implementation, these would be much more complex, likely involving
# calls to simulation environments, predictive models, or formal methods tools.

class RiskComponent(BaseUSFComponent):
    """
    Estimates the probability of immediate safety violation.
    Returns a value in (0, 1], where higher is more risky.
    """
    def calculate(self, state: State, action: Action) -> float:
        # Placeholder logic: returns a constant risk value.
        return self.params.get("mock_risk_value", 0.1)

class ImpactComponent(BaseUSFComponent):
    """
    Measures the distributional shift from a baseline.
    Returns a non-negative value, where higher is more impactful.
    """
    def calculate(self, state: State, action: Action) -> float:
        # Placeholder logic: returns a constant impact value.
        return self.params.get("mock_impact_value", 0.05)

class CorrigibilityComponent(BaseUSFComponent):
    """
    Scores the agent's predicted compliance with corrections.
    Returns a value, where higher is better (more corrigible).
    """
    def calculate(self, state: State, action: Action) -> float:
        # Placeholder logic: returns a constant corrigibility score.
        return self.params.get("mock_corr_value", 0.9)


# --- Factory to create components based on config ---

COMPONENT_REGISTRY = {
    "risk": RiskComponent,
    "impact": ImpactComponent,
    "corr": CorrigibilityComponent,
}

def create_component(name: str, params: Dict[str, Any]) -> BaseUSFComponent:
    """Factory function to create a USF component instance from its name."""
    component_class = COMPONENT_REGISTRY.get(name)
    if not component_class:
        raise ValueError(f"Unknown USF component type in config: {name}")
    return component_class(params)

# --- Main Configurable USF Implementation ---

class ConfigurableUSF(UniversalSafetyFunctional):
    """
    A Universal Safety Functional that is configured via a YAML file.
    It computes a safety score based on a weighted combination of pluggable
    sub-components for risk, impact, and corrigibility.
    """
    def __init__(self, config_path: str):
        """
        Initializes the USF by loading and parsing a YAML configuration file.

        Args:
            config_path: The path to the YAML configuration file.
        """
        print(f"Loading USF configuration from: {config_path}")
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.weights = self.config["weights"]
        self.gating_threshold = self.config["gating_threshold"]["value"]

        self.components: Dict[str, BaseUSFComponent] = {}
        for name, component_config in self.config["components"].items():
            self.components[name] = create_component(name, component_config.get("parameters", {}))

        print("USF configuration loaded successfully.")

    def estimate_score(self, state: State, action: Action) -> float:
        """
        Estimates the final USF score based on the formula in the config.
        The formula is assumed to be a weighted sum of component outputs,
        with logarithmic penalties for risk and impact.

        Formula: S = w_risk * log(RISK) + w_impact * log(IMPACT) + w_corr * CORR

        A very low (highly negative) score indicates high danger.
        """
        # Add a small epsilon to prevent log(0) for risk/impact values of 0.
        epsilon = 1e-9

        risk_val = self.components["risk"].calculate(state, action)
        impact_val = self.components["impact"].calculate(state, action)
        corr_val = self.components["corr"].calculate(state, action)

        # The logarithmic penalty heavily punishes risk and impact values that
        # approach zero, as log(x) -> -inf as x -> 0.
        # We assume RISK and IMPACT are probabilities/divergences in [0,1].
        # Corrigibility is treated as a direct score.
        score = (
            self.weights["risk"] * math.log(risk_val + epsilon) +
            self.weights["impact"] * math.log(impact_val + epsilon) +
            self.weights["corr"] * corr_val
        )

        return score

    def get_gating_threshold(self) -> float:
        """Returns the gating threshold loaded from the configuration."""
        return self.gating_threshold
