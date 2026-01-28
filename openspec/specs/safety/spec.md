# Safety Spec

## No Bypass Rule
- The **simulate+verify gate is mandatory** for all runtime paths.
- No component may persist, publish, or return results without verification.

## Failure Handling
- Verification failure must return `status: "fail"` with `reasons` populated.
- Failures are logged with a request id and artifact pointers.

## Determinism
- Simulation inputs are fixed via deterministic fixtures and explicit seeds.
- Any nondeterministic behavior is treated as a safety failure.
