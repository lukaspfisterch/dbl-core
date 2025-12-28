# Changelog

## [0.3.1] - 2025-12-28

- Documentation sync: canonicalization rejects non-str mapping keys and all floats
- Documentation sync: sets restricted to primitive-only values with deterministic ordering
- Documentation sync: unknown object types forbidden, no implicit to_dict admission
- Documentation sync: trace_digest is over sanitized trace mapping after timing-key stripping

## [0.3.0] - 2025-12-26

- Breaking: refocused DBL Core as deterministic event substrate
- Added contract specification for DBL Core
- Added canonical event model, digest, and behavior stream V
- Added gate decision event model (ALLOW/DENY)
- Embedded kernel traces as immutable facts
- Added tests for determinism, immutability, and t_index ordering

## [0.2.0] - 2025-12-04

- Single file architecture (104 LOC)
- deepcopy for effective_metadata
- describe_config() method
- Thread-safety and determinism tests

## [0.1.0] - 2025-12-03

Initial version.
