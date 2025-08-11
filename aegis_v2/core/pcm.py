# aegis_v2/core/pcm.py

from typing import Set, Dict, Any

class Capability:
    """
    Represents a single, unique capability token in a lattice structure.
    A capability implies all of its parents up to the root.
    For example, 'fs_write' might have 'fs_read' as a parent, which has 'fs_access'.
    Granting 'fs_write' implicitly grants the others.
    """
    def __init__(self, name: str, parent: 'Capability' = None):
        self.name = name
        self.parent = parent

    def __repr__(self) -> str:
        return f"Capability({self.name})"

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Capability) and self.name == other.name

class Action:
    """
    Represents a structured action proposed by the AI model.
    The 'type' of the action corresponds to a capability name.
    """
    def __init__(self, type: str, payload: Dict[str, Any]):
        self.type = type
        self.payload = payload

    def __repr__(self) -> str:
        return f"Action(type='{self.type}', payload={self.payload})"


class PolicyEnforcementPoint:
    """
    The core Policy Enforcement Point (PEP) for the PCM.
    It checks proposed actions against a given capability policy based on a
    pre-defined capability lattice.
    """
    def __init__(self, capability_map: Dict[str, Capability]):
        """
        Initializes the PEP with a map of all known capabilities in the system.
        The keys are the string names of the capabilities.

        Args:
            capability_map: A dictionary mapping capability names to Capability objects.
        """
        self.capability_map = capability_map

    def get_required_caps(self, action: Action) -> Set[Capability]:
        """
        Maps a structured action to the set of capability tokens it requires.
        In a real system, this mapping would be more complex, formally specified,
        and part of the system's Trusted Computing Base (TCB).
        """
        # If the action type is a known capability, return that capability token.
        if action.type in self.capability_map:
            return {self.capability_map[action.type]}

        # If the action type is unknown, it requires a special, non-grantable capability.
        # This ensures that malformed or novel action types are always denied by default.
        return {Capability("unknown_action_type")}

    def is_allowed(self, action: Action, policy: Set[Capability]) -> bool:
        """
        The core enforcement rule of the PCM. Checks if an action is permitted
        by the current policy.

        Args:
            action: The proposed action from the AI agent.
            policy: The set of capabilities currently granted to the agent.

        Returns:
            True if the action is allowed, False otherwise.
        """
        required_capabilities = self.get_required_caps(action)

        for required_cap in required_capabilities:
            if not self._is_implied_by_policy(required_cap, policy):
                return False
        return True

    def _is_implied_by_policy(self, required_cap: Capability, policy: Set[Capability]) -> bool:
        """
        Checks if a required capability is implied by any of the capabilities
        granted in the policy, by traversing the lattice structure upwards from
        each granted capability.
        """
        for granted_cap in policy:
            # Start checking from the granted capability itself.
            current_cap_in_lattice = granted_cap
            # Traverse up the hierarchy (e.g., from fs_write to fs_read to fs_access)
            while current_cap_in_lattice is not None:
                if current_cap_in_lattice == required_cap:
                    return True
                current_cap_in_lattice = current_cap_in_lattice.parent
        return False
