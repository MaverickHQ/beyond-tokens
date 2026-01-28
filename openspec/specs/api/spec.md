# API Spec

## Base
- **Protocol**: HTTPS/HTTP
- **Content-Type**: `application/json`

## Required Endpoints
### `GET /health`
- **Response (200)**
  - `status`: string, required, must be `"ok"`
  - `version`: string, required, semantic version of API

### `POST /simulate`
- **Request**
  - `fixture_id`: string, required
  - `action`: object, required
  - `seed`: integer, required
- **Response (200)**
  - `simulation_id`: string, required
  - `state`: object, required
  - `artifacts`: object, required

### `POST /verify`
- **Request**
  - `simulation_id`: string, required
  - `state`: object, required
  - `artifacts`: object, required
- **Response (200)**
  - `verification_id`: string, required
  - `status`: string, required, one of `"pass" | "fail"`
  - `reasons`: array of string, required (empty array if pass)

### `POST /simulate-verify`
- **Request**
  - `fixture_id`: string, required
  - `action`: object, required
  - `seed`: integer, required
- **Response (200)**
  - `simulation_id`: string, required
  - `verification_id`: string, required
  - `status`: string, required, one of `"pass" | "fail"`
  - `state`: object, required
  - `artifacts`: object, required
  - `reasons`: array of string, required (empty array if pass)

## Error Format (All endpoints)
- **Response (4xx/5xx)**
  - `error`: object, required
    - `code`: string, required
    - `message`: string, required
    - `details`: object, required (can be empty)
    - `request_id`: string, required

## Rules
- The API **must not** return simulation artifacts without a verify step. Use `/simulate-verify` as the default public path.
- Deterministic fixtures are required for any non-test simulation request.
