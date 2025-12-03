# DBL Core

**Deterministic Boundary Layer on KL Kernel Logic 0.4.0**

---

## Architecture

```
┌─────────────────────────────────────────┐
│  DBL Gateways / Runtimes                │
│  (LLM Gateway, Tool Gateway, API)       │
├─────────────────────────────────────────┤
│  DBL Core                               │
│  (Session, Policy, Shadow State, Flows) │
├─────────────────────────────────────────┤
│  KL Kernel Logic 0.4.0                  │
│  (Δ, V, t only)                         │
└─────────────────────────────────────────┘
```

---

## Core Concepts

### DblSession

Container for everything the Kernel does not know.

- `run_id`: unique identifier
- `created_at`: UTC timestamp
- `caller`: user, system, tenant
- `context`: structured dict
- `shadow_state`: risk, confidence, mode
- `traces`: list of ExecutionTrace from Kernel
- `tags`: set of strings

### DblTask

Abstract execution unit that uses Kernel internally.

Types:
- `LlmTask`: LLM API calls
- `ToolTask`: Tool execution
- `HttpTask`: External HTTP calls
- `CompositeTask`: Plans using CAEL internally

Interface:
- `build_psi(session) -> PsiDefinition`
- `build_callable(session) -> Callable`
- `build_kwargs(session) -> dict`
- `postprocess(session, trace) -> Any`

### PolicyEngine

Central policy hook for DBL.

- `before_execute(session, task) -> PolicyDecision`
- `after_execute(session, task, trace) -> None`

PolicyDecision:
- `action`: ALLOW | DENY | MODIFY | SIMULATE
- `reason`: explanation
- `modified_task`: optional replacement

### ShadowState

DBL-internal adaptive state, not visible to Kernel.

Fields:
- `risk_score`
- `confidence`
- `guard_mode`: normal, strict, readonly
- `llm_temperature_cap`
- `tool_usage_mode`: allowed, restricted, off

### ExecutionPlan / DblFlow

Higher orchestration layer above CAEL.

- List of `DblStep`
- Conditions based on shadow state or previous results
- Internally converts to `(psi, callable, kwargs)` for CAEL

---

## Module Structure

```
dbl_core/
  core/
    session.py         # DblSession
    task.py            # DblTask, LlmTask, ToolTask
    flow.py            # ExecutionPlan, DblStep
    shadow_state.py    # ShadowState, ShadowStateController
  policy/
    engine.py          # PolicyEngine, PolicyDecision
    rules.py           # Predefined rules
  adapters/
    llm.py             # LLM adapter base
    tool.py            # Tool adapter base
    http.py            # HTTP adapter base
  audit/
    recorder.py        # DblAuditLog
  runtime/
    gateway.py         # Sync orchestrator
```

---

## Dependency

```
dbl-core depends on kl-kernel-logic >= 0.4.0
```

DBL Core calls Kernel. Nothing flows back into Kernel.

---

## Execution Flow

1. Create session: `session = DblSession(...)`
2. Define flow: `plan = ExecutionPlan([...DblStep...])`
3. Run via gateway: `result = gateway.run(plan, session)`

Gateway internally:
- Iterates over steps
- Calls `PolicyEngine.before_execute()`
- Builds psi, callable, kwargs via DblTask
- Calls `Kernel.execute()`
- Updates `session.shadow_state`
- Appends trace to `session.traces`
- Calls `PolicyEngine.after_execute()`
- Records to AuditLog

---

## License

MIT

