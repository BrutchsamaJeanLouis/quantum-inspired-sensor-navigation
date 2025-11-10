"""
Module: src\\__init__.py
Depends on:
  - src.core.toy_world (ToyWorld)
  - src.visualization.visualizer (WorldVisualizer, export_field_matplotlib)

Quantum-Inspired World Model (QIWM)
Phase 1: Classical Potential Field Simulation
"""

__version__ = "0.1.0"
__author__ = "QIWM Project"

from .core import ToyWorld
from .visualization import WorldVisualizer, export_field_matplotlib

__all__ = ['ToyWorld', 'WorldVisualizer', 'export_field_matplotlib']
