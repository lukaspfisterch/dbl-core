# Changelog

## [0.2.0] - 2025-12-04

Minimal core. Single file architecture.

### Core (104 LOC)

- BoundaryContext: immutable input context
- PolicyDecision: single policy evaluation result
- BoundaryResult: aggregated evaluation result
- DBLCore: deterministic boundary evaluator

### Guarantees

- No mutation of input context (deepcopy)
- Thread-safe evaluation
- Deterministic output for same input
- describe() returns stable snapshots

### Tests

- 10 tests (7 core + 3 stress)
- Determinism, immutability, thread-safety coverage
