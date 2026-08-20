"""
Core physics simulation modules for QIWM.
"""

from .toy_world import ToyWorld
from .quantum_world import QuantumInspiredWorld
from .coherence import compute_phi, compute_phi_map
from .agents import NanoAgent, AgentSwarm

__all__ = ['ToyWorld', 'QuantumInspiredWorld', 'compute_phi', 'compute_phi_map', 'NanoAgent', 'AgentSwarm']
