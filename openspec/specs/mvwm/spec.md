# MVWM (Minimum Viable World Model) Spec

## Purpose
Define the minimal deterministic world model needed for simulate+verify gating.

## Core Concepts
- **State**: a deterministic, serializable structure produced from fixtures and previous steps.
- **Action**: a deterministic input that advances the state.
- **Simulation result**: the predicted next state and derived artifacts.
- **Verification result**: a deterministic pass/fail with reasons.

## Required Behavior
- Simulations are deterministic with fixed seeds and fixtures.
- Verifier receives the simulation output and **must** run before any acceptance of results.
- No bypass rule: any path that attempts to persist, publish, or return results **must** use simulate+verify.

## Artifacts
- Simulation artifacts are stored in a structured, versioned format.
- Verification artifacts include the decision, reasons, and timestamp.
