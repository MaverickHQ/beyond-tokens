# Testing Spec

## Required Test Suites
- **Unit tests**: core domain, simulator, verifier, and utilities.
- **Contract tests**: API request/response shapes including error format.
- **Integration tests**: orchestration flow including Step Functions interface.
- **AWS smoke tests**: minimal end-to-end run in a staging AWS environment.

## Deterministic Fixtures
- Fixtures must be versioned and deterministic.
- The same fixture + seed must produce identical simulation outputs across runs.

## Coverage Expectations
- All required endpoints must have contract tests.
- All failure paths in safety rules must be tested.
