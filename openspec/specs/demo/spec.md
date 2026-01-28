# Demo Spec

## On-Rails Demo Requirements
- Provide `make demo` for a full simulate+verify run using fixtures.
- Provide `make demo-local` for a local-only flow without AWS dependencies.

## Rules
- Demo flows must use `/simulate-verify` and never bypass verification.
- Demo output must be deterministic for the same fixture and seed.
