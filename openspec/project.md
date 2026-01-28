# Beyond Tokens — Builder Lab OpenSpec

This OpenSpec defines the domain, API, infrastructure, safety controls, testing requirements, and demo expectations for the Beyond Tokens — Builder Lab repository. It is the single source of truth for expected behavior and is intended to make future implementation unambiguous.

## Lab Scenarios
- **Trading MVWM** is the first lab scenario and establishes the minimum viable world model (MVWM) architecture.

## Scope
- Deterministic simulation and verification of world-model steps.
- Strict safety gating: **simulate + verify** is mandatory for all execution paths.
- Versioned staging of simulation capabilities with explicit defaults.

## Principles
- Determinism first: fixtures, seeds, and outputs are reproducible.
- No bypass: the simulate+verify gate is always enforced.
- Explicit interfaces: endpoints, fields, and error formats are fixed and validated.

## References
- [AGENTS](./AGENTS.md)
- [Specs](./specs)
- [Changes](./changes)
