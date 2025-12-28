# Domainrunner Contract (v0.3.x)

This contract defines domain-level semantics and stress-runner behavior.
It is NOT part of dbl-core and may evolve faster.
It must not weaken dbl-core invariants.

## Purpose
- Define domain semantics for DECISION payloads (reason codes, taxonomy, schemas).
- Define what constitutes a valid correlation chain per scenario.
- Define any trace field semantics beyond canonical integrity checks.
- Define stress verdict logic (PASS/FAIL criteria).

## Inputs
- Domain requests and scenario definitions.
- dbl-core event stream V produced by the runner or boundary service.
- Optional execution engine outputs used only as observational artifacts.

## Outputs
- Scenario verdicts (PASS/FAIL) plus failure_signals.
- Explanations and reports derived from V and runner rules.
- Optional exports (JSONL) for analysis.

## Non-Goals
- No changes to dbl-core canonicalization rules.
- No post-hoc mutation of V.
- No reliance on timestamps for ordering or correctness.

## DECISION Semantics (Domain Level)
A domainrunner MAY require DECISION deterministic payload to include:
- outcome: "ALLOW" or "DENY"
- policy_version: pinned and explicit
- reason_code: stable within the domain policy lifecycle
- rule_id or control_id: optional domain identifier
- justification: optional, but must be deterministic if included

The domainrunner MAY enforce:
- "stable reason_code" rules
- schema validation of DECISION payload
- allowed enumerations for reason_code and failure_code

dbl-core MUST NOT enforce these semantics.

## Correlation Chain Rules (Domain Level)
The domainrunner defines correlation structure, for example:
- INTENT -> DECISION -> (optional) EXECUTION -> (optional) PROOF
- DENY implies:
  - DECISION(outcome=DENY)
  - no EXECUTION for the same correlation_id

The domainrunner may define how refs must look, uniqueness rules, and cross-links.

dbl-core may enforce only structural validity, not domain chain semantics.

## Trace Semantics (Domain Level)

### Trace core fields
If the domainrunner relies on specific trace core fields such as:
- psi
- success
- failure_code
- exception_type

then the domainrunner must define:
- exact canonical field set
- allowed types and allowed values
- how missing fields are treated
- whether field changes are considered observational drift or deterministic change

### Trace digest policy
A domainrunner MAY define an additional digest over a subset of trace fields, for example:
- trace_core_digest = sha256(c14n({psi, success, failure_code, exception_type}))

If used, the runner must:
- compute it deterministically
- record it deterministically (preferably in deterministic payload, not observational)
- treat it as domain semantics, not dbl-core semantics

dbl-core MUST only validate canonical integrity of trace_digest over the sanitized trace mapping
(after stripping observational timing keys) and its canonical JSON bytes.

## Stress Runner Verdict Logic (Domain Level)

### Typical failure_signals
A stress runner may emit signals such as:
- decision_missing
- decision_after_execution
- policy_version_not_pinned
- governance_reads_observations
- replay_requires_execution
- observational_drift

These signals are domainrunner-defined. dbl-core MUST NOT implement or interpret them.

### Replay requirement
A stress runner may require:
- normative replay from V alone
- deterministic reconstruction of the DECISION sequence
- no dependence on EXECUTION outputs for governance correctness

This is checked by the runner against V and runner rules.

## Compatibility Rules
- The domainrunner may extend deterministic payload schemas, but must never:
  - introduce new dbl-core event kinds
  - alter dbl-core canonicalization
  - allow observational data into dbl-core digests
  - reorder or mutate V
