# DBL Core Contract (v0.3.x)

This contract defines the deterministic event substrate for DBL Core.
It is normative for dbl-core and contract-stable.

## Scope
dbl-core provides:
- A minimal DBL event model (INTENT, DECISION, EXECUTION, PROOF).
- Deterministic canonicalization and digests.
- An append-only ordered behavior stream V with deterministic replay of the normative projection.

dbl-core does not provide:
- Policy semantics, templates, orchestration, or execution.
- Any interpretation of trace meaning beyond canonicalization integrity.
- I/O side effects, randomness, time-based ordering, or background processing.

## Inputs
- DBL events: INTENT, DECISION, EXECUTION, PROOF.
- For EXECUTION events: a canonical trace representation (canonical dict or canonical bytes) plus a trace_digest.

## Outputs
- Canonical DBL event representations (dict and JSON).
- Event digests derived only from deterministic fields.
- Behavior stream V = [e0, e1, e2, ...] where t_index is derived solely from order in V.
- BehaviorV digest derived from ordered event digests.

## Non-Goals
- No policy engine, no domain validation, no convenience APIs that coerce inputs.
- No execution of user tasks.
- No time, randomness, or I/O side effects.

## Event Stream V
- DBL behavior is a single ordered stream: V = [e0, e1, e2, ...].
- t_index is the position in V (0..n-1).
- Ordering MUST be derived from index, not timestamps or wall-clock time.
- V MUST be append-only:
  - No reorder
  - No delete
  - No compaction or optimization that changes order or content

## Event Kinds
- INTENT: records proposed execution context and authoritative input descriptors.
- DECISION: records a normative decision outcome.
- EXECUTION: records an execution trace artifact (observational).
- PROOF: records evidence artifacts (observational).

Only DECISION is normative. All other kinds are non-normative.

## DENY is a DECISION
- DENY MUST be represented as a DECISION event.
- If a DECISION outcome is DENY, no corresponding EXECUTION event may exist for that correlation chain.

## Deterministic vs Observational Fields

### Deterministic segment
The deterministic segment of an event consists of:
- event_kind
- correlation_id
- deterministic payload (a JSON-safe structure restricted to allowed types)
- refs (if present, treated as deterministic structure)

### Observational segment
Observational fields include, but are not limited to:
- timestamps
- runtime or latency
- telemetry or metrics
- error text, exception repr
- non-deterministic execution outputs not explicitly admitted into the deterministic segment

Observational fields MUST NOT:
- influence event digests
- influence ordering
- be interpreted as semantic claims by dbl-core

## Canonicalization and Digests

### Canonical dict
- DblEvent.to_dict() MUST return a canonical mapping with a stable key order.
- The canonical dict MUST include both deterministic and observational segments, but canonicalization rules MUST be defined such that digests exclude observational data.

### Canonical JSON
- DblEvent.to_json() MUST serialize canonical dict deterministically:
  - sorted keys
  - stable separators
  - UTF-8 encoding
  - allow_nan = False (reject NaN and Infinity)
  - floats MUST be rejected in canonicalization

### Canonicalization rules (strict)
- Mapping keys MUST be str. Non-str keys are INVALID_EVENT.
- Floats MUST be rejected everywhere in canonicalized values.
- Sets are allowed only if elements are JSON primitives (str, int, bool, None) and MUST be deterministically ordered.
- Unknown object types MUST be rejected. There is no implicit to_dict admission.
- Non-serializable values MUST raise TypeError.
- Observational fields MUST be canonicalizable even though they are excluded from digests.

### Event digest
- DblEvent.digest() MUST be sha256 over canonical JSON bytes of the deterministic segment only.

### BehaviorV digest
- BehaviorV.digest() MUST be sha256 over the ordered list of event digests.
- The BehaviorV digest MUST change if and only if the ordered deterministic event history changes.

## EXECUTION Trace Embedding
- EXECUTION events MUST embed:
  - trace: canonical trace dict (or canonical trace bytes)
  - trace_digest: sha256 over canonical JSON bytes of the sanitized trace mapping
- dbl-core MUST NOT call Kernel.execute().
- dbl-core MUST validate trace integrity only as:
  - sha256(canonical JSON bytes of sanitized trace mapping) == trace_digest
- dbl-core MUST NOT validate domain semantics of trace fields.

## Failure Taxonomy
dbl-core MAY raise typed errors, but must at minimum distinguish:
- INVALID_EVENT: malformed event, missing required fields, invalid kind, invalid deterministic payload types
- INVALID_TRACE: missing trace, non-canonical trace, trace_digest mismatch

## Determinism Guarantees
- Changing observational fields MUST NOT change event digests.
- Changing observational fields MUST NOT change BehaviorV digest.
- Replaying V in order MUST yield the same normative projection (DECISION subsequence), independent of observational variation.

## Normative References
- KL Kernel Logic (library dependency)
- DBL Paper (conceptual model and invariants)
