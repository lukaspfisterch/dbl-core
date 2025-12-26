# DBL Core Contract (v0.3.0)

This contract defines the deterministic event substrate for DBL Core. It is normative and contract-stable.

## Inputs
- DBL events representing intent, decisions, executions, and proofs.
- Kernel ExecutionTrace objects or canonical trace dicts for EXECUTION events.

## Outputs
- Canonical DBL events and behavior streams with deterministic digests.
- Deterministic t_index derived solely from event order.

## Non-Goals
- No policy engine, templates, or orchestration.
- No execution of user tasks.
- No time, randomness, or I/O side effects.

## Event Stream V
- DBL behavior is a single ordered stream: V = [e0, e1, e2, ...].
- t_index is the position in V (0..n-1).
- Ordering MUST be derived from index, not timestamps.

## Event Kinds
- INTENT: proposed execution package (psi and input descriptors).
- DECISION: gate decision ALLOW or DENY with stable reason_code.
- EXECUTION: embeds a kernel ExecutionTrace as immutable fact.
- PROOF: placeholder for derived proofs (no intelligence in core).

## DENY is a Delta
- DENY is represented as a DECISION event.
- If DENY occurs, no EXECUTION event exists for that correlation chain.

## Kernel Trace Embedding
- EXECUTION event data MUST embed:
  - trace: canonical trace dict
  - trace_digest: deterministic digest of the trace
- DBL Core MUST NOT call Kernel.execute().
- DBL Core MUST verify trace_digest against the deterministic core fields:
  - psi, success, failure_code, exception_type
- trace_digest MUST equal sha256(json_dumps(canonicalize(core))) where core is:
  - {psi, success, failure_code, exception_type}

## Canonicalization and Digest
- DblEvent.to_dict() MUST return a canonical mapping.
- DblEvent.to_json() MUST return canonical JSON (sorted keys, stable encoding).
- DblEvent.digest() MUST hash canonical JSON of deterministic fields.
- BehaviorV.digest() MUST hash the ordered list of event digests.

## Observational Fields
- Observational fields MUST NOT be used for ordering or semantic claims.
- Observational fields MUST be excluded from event digests.
- Examples: timestamps, runtime, error text, exception repr.

## Failure Taxonomy
- INVALID_EVENT: malformed event or missing required fields.
- INVALID_TRACE: missing or invalid trace or trace_digest.

## Determinism
- Deterministic fields are event_kind, correlation_id, and data (excluding observational trace data).
- Observational fields are excluded from digest and MUST NOT affect decisions.

## Normative References
- KL Execution Theory v0.1.0
  https://github.com/lukaspfisterch/kl-execution-theory
- KL Kernel Logic v0.5.0
  https://github.com/lukaspfisterch/kl-kernel-logic
