# Beyond Tokens — Builder Lab

Beyond Tokens — Builder Lab is a deployable world-model planning lab with a strict **simulate → verify → commit** flow.

This repository accompanies the **Beyond Tokens** essay series. The essays explain *why*; this repo demonstrates *how*.

## Staged Versions
- **v1.0 Minimum Viable World Model (local)**
- **v1.1 Executable World Model on AWS**
- **v2 Agent-governed world models (planned)**

## Setup

```bash
make setup
```

## Lint

```bash
make lint
```

## Tests

```bash
make test
```

## Local Demo

```bash
make demo-local
```

## AWS Demo

```bash
AWS_PROFILE=beyond-tokens-dev make cdk-synth
AWS_PROFILE=beyond-tokens-dev make cdk-deploy
AWS_PROFILE=beyond-tokens-dev make demo-aws
```

## What you should see
- Scenario A rejects with clear verification errors.
- Scenario B approves and executes with updated state.

## One-command checks
```bash
make lint
make test
make demo-local
```
