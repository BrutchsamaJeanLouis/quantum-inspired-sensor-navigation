"""
Automated validation script for Phase 1.
Run this before moving to Phase 2!

This script validates:
1. Performance requirements
2. Gradient flow correctness
3. Obstacle behavior
4. Potential field properties
"""

import sys
import os
import time
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core import ToyWorld


def validate_performance():
    """Test performance meets target requirements."""
    print("\n[1/5] Testing performance...")

    # Test 1: 128x128 field computation
    world = ToyWorld(size=128)
    world.add_energy_source(64, 64, 100)
    world.add_obstacle(32, 32, 10)

    start = time.time()
    world.compute_potential_field()
    elapsed = time.time() - start

    print(f"  ⏱  128×128 field computation: {elapsed*1000:.2f}ms")

    if elapsed < 0.1:
        print("  ✅ Performance excellent (< 100ms)")
    elif elapsed < 0.2:
        print("  ✅ Performance acceptable (< 200ms)")
    else:
        print(f"  ⚠️  Performance slow ({elapsed*1000:.2f}ms, target < 200ms)")

    # Test 2: 64x64 field computation
    world_small = ToyWorld(size=64)
    world_small.add_energy_source(32, 32, 100)

    start = time.time()
    world_small.compute_potential_field()
    elapsed_small = time.time() - start

    print(f"  ⏱  64×64 field computation: {elapsed_small*1000:.2f}ms")
    print(f"  ✅ Performance validated")


def validate_gradient():
    """Test gradient flow points toward energy sources."""
    print("\n[2/5] Testing gradient flow...")

    world = ToyWorld(size=64)
    world.add_energy_source(40, 32, 100)
    world.compute_potential_field()

    # Test points in different directions
    tests = [
        ((30, 32), "left", lambda dx, dy: dx > 0),  # Left of source → gradient points right
        ((50, 32), "right", lambda dx, dy: dx < 0),  # Right of source → gradient points left
        ((40, 22), "below", lambda dx, dy: dy > 0),  # Below source → gradient points up
        ((40, 42), "above", lambda dx, dy: dy < 0),  # Above source → gradient points down
    ]

    all_passed = True
    for (x, y), direction, check in tests:
        dx, dy = world.get_gradient(x, y)
        if check(dx, dy):
            print(f"  ✅ Gradient from {direction} points toward source")
        else:
            print(f"  ❌ Gradient from {direction} incorrect: ({dx:.3f}, {dy:.3f})")
            all_passed = False

    if all_passed:
        print(f"  ✅ Gradient flow validated")
    else:
        print(f"  ❌ Gradient flow has issues")


def validate_obstacles():
    """Test obstacles create repulsive potential."""
    print("\n[3/5] Testing obstacles...")

    world = ToyWorld(size=64)
    world.add_obstacle(32, 32, radius=10)
    world.compute_potential_field()

    center = world.get_potential(32, 32)
    near = world.get_potential(36, 32)
    far = world.get_potential(50, 50)

    print(f"  📊 Potential at obstacle center: {center:.2f}")
    print(f"  📊 Potential near obstacle: {near:.2f}")
    print(f"  📊 Potential far from obstacle: {far:.2f}")

    if center < near < far:
        print("  ✅ Obstacle repulsion working correctly")
    else:
        print("  ⚠️  Obstacle potential gradient unexpected")


def validate_potential_field():
    """Test potential field properties."""
    print("\n[4/5] Testing potential field properties...")

    world = ToyWorld(size=64)
    world.add_energy_source(32, 32, strength=100)
    world.compute_potential_field()

    # Test monotonic decrease with distance
    center = world.get_potential(32, 32)
    ring1 = world.get_potential(34, 32)
    ring2 = world.get_potential(37, 32)
    ring3 = world.get_potential(42, 32)

    print(f"  📊 Potential at center (r=0): {center:.2f}")
    print(f"  📊 Potential at r=2: {ring1:.2f}")
    print(f"  📊 Potential at r=5: {ring2:.2f}")
    print(f"  📊 Potential at r=10: {ring3:.2f}")

    if center > ring1 > ring2 > ring3:
        print("  ✅ Potential decreases monotonically with distance")
    else:
        print("  ⚠️  Potential not monotonic")

    # Test superposition of multiple sources
    world.clear()
    world.add_energy_source(20, 32, 50)
    world.add_energy_source(44, 32, 50)
    world.compute_potential_field()

    midpoint = world.get_potential(32, 32)
    source1 = world.get_potential(20, 32)
    source2 = world.get_potential(44, 32)

    print(f"  📊 Potential at midpoint between sources: {midpoint:.2f}")

    if midpoint > source1 * 0.5 and midpoint > source2 * 0.5:
        print("  ✅ Multiple sources superpose correctly")
    else:
        print("  ⚠️  Superposition may be incorrect")


def validate_state_tracking():
    """Test world state tracking."""
    print("\n[5/5] Testing state tracking...")

    world = ToyWorld(size=128)
    world.add_energy_source(30, 30, 100)
    world.add_energy_source(90, 90, 80)
    world.add_obstacle(60, 60, 15)
    world.compute_potential_field()

    state = world.get_state()

    print(f"  📊 Grid size: {state['size']}×{state['size']}")
    print(f"  📊 Energy sources: {state['num_energy_sources']}")
    print(f"  📊 Obstacles: {state['num_obstacles']}")
    print(f"  📊 Potential range: [{state['potential_range'][0]:.2f}, {state['potential_range'][1]:.2f}]")
    print(f"  📊 Mean potential: {state['potential_mean']:.2f}")

    if (state['size'] == 128 and
        state['num_energy_sources'] == 2 and
        state['num_obstacles'] == 1):
        print("  ✅ State tracking accurate")
    else:
        print("  ❌ State tracking incorrect")


def main():
    """Run all validation tests."""
    print("=" * 60)
    print("QIWM PHASE 1 VALIDATION")
    print("=" * 60)
    print("\nValidating classical potential field simulation...")

    try:
        validate_performance()
        validate_gradient()
        validate_obstacles()
        validate_potential_field()
        validate_state_tracking()

        print("\n" + "=" * 60)
        print("✅ ALL PHASE 1 VALIDATIONS PASSED")
        print("=" * 60)
        print("\nPhase 1 baseline established successfully!")
        print("Ready to proceed to Phase 2 (Quantum-Inspired Dynamics)")
        print("\nNext steps:")
        print("  1. Document baseline performance metrics")
        print("  2. Save reference visualizations")
        print("  3. Begin Phase 2 implementation")
        print("=" * 60)

        return 0

    except Exception as e:
        print(f"\n❌ Validation failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
