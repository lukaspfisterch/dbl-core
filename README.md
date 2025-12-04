# DBL Core

Deterministic Boundary Layer on top of KL Kernel Logic.

DBL Core evaluates governance boundaries for operations before they are executed by the KL kernel.

## Install

```bash
pip install dbl-core
```

Requires `kl-kernel-logic>=0.4.0` and Python 3.11+.

## API

### BoundaryContext

Input context for DBL evaluation.

```python
from dbl_core import BoundaryContext
from kl_kernel_logic import PsiDefinition

psi = PsiDefinition(psi_type="llm", name="generate")
ctx = BoundaryContext(
    psi=psi,
    caller_id="user-1",
    tenant_id="tenant-1",
    channel="api",
    metadata={"key": "value"},
)
```

Fields:

- `psi: PsiDefinition` - operation identifier
- `caller_id: str | None`
- `tenant_id: str | None`
- `channel: str | None`
- `metadata: Mapping[str, Any]` - arbitrary, read only from the caller perspective

BoundaryContext is immutable. DBL Core never mutates the instance or its metadata.

### DBLCore

Central entrypoint for boundary evaluation. Returns a BoundaryResult.

```python
from dbl_core import DBLCore

core = DBLCore(config={"limit.default": 100})
result = core.evaluate(ctx)

if result.is_allowed():
    # proceed with kernel execution
    pass
```

Methods:

- `evaluate(context: BoundaryContext) -> BoundaryResult`
- `describe_config() -> Mapping[str, Any]` - copy of the current configuration, safe for logging and diagnostics

### BoundaryResult

Aggregated evaluation result.

```python
result.final_outcome        # "allow" | "modify" | "block"
result.is_allowed()         # True if "allow" or "modify"
result.effective_psi        # PsiDefinition to use after policies
result.effective_metadata   # deep copy, no alias to context.metadata
result.decisions            # list[PolicyDecision]
result.context              # original BoundaryContext
result.describe()           # stable dict for audit and logging
```

The `effective_*` fields represent the state after all policies have been applied.

### PolicyDecision

Single policy evaluation step.

```python
from dbl_core import PolicyDecision

decision = PolicyDecision(
    outcome="allow",
    reason="passed all checks",
    details={"policy_chain": ["rate-limit", "content-filter"]},
)
```

Fields:

- `outcome: Literal["allow", "modify", "block"]`
- `reason: str` - human readable explanation
- `details: Mapping[str, Any]` - structured metadata for diagnostics or audit
- `modified_psi: PsiDefinition | None` - optional override of the original psi
- `modified_metadata: Mapping[str, Any] | None` - optional metadata override for this step

In the current default implementation DBL Core produces a single PolicyDecision with outcome "allow". The structure is designed for later composition of multiple policies.

## Guarantees

- No mutation of the input BoundaryContext
- `effective_metadata` is a deep copy, no aliasing back into `context.metadata`
- Thread safe evaluation for a shared DBLCore instance
- Deterministic output for identical input
- `describe()` returns stable, serializable snapshots suitable for logging and audit

## License

MIT
