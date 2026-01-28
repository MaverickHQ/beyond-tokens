# AGENTS

## Owner
- **Product owner**: defines acceptance criteria and prioritizes version milestones.

## Core contributors
- **Core domain**: implements simulator, verifier, fixtures, and deterministic state transitions.
- **API**: implements HTTP endpoints and contract validation.
- **Infra**: implements AWS orchestration and deployment boundaries.
- **QA/Testing**: maintains test suite requirements and fixture coverage.

## Responsibilities
- Every change must cite the relevant OpenSpec section.
- All tests in `openspec/specs/testing/spec.md` are mandatory.
- Demo scripts must use the on-rails flows defined in `openspec/specs/demo/spec.md`.
