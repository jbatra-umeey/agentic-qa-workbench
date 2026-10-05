# Architecture decisions

## Bound the planner

A maximum of two attempts makes failure behavior and model-call count understandable. Invalid plans fail closed instead of being executed.

## Bind review to content

The requirements and plan have hashes. Execution requires approval of the exact plan hash, so a later edit cannot accidentally reuse an earlier approval.

## Execute known operations

The registry maps allowed tool names to existing Python functions. The model proposes inputs, not executable source code. Review remains necessary for the test oracle.

## Next engineering step

Add a real application adapter, independent reference oracles, a durable state store with compare-and-swap updates, authenticated reviewers and mutation testing.
