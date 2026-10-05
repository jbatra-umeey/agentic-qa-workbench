# Five-minute walkthrough

1. Run `demo` and show the failing 80-character boundary case.
2. Run `plan`, inspect the test oracle, and approve the exact digest.
3. Change the saved plan and demonstrate that execution is rejected.
4. Show the disallowed-tool test and the bounded retry test.
5. Explain why a structurally valid generated test can still assert the wrong behavior.

Discussion prompts: How would a mobile automation adapter fit the registry?
What changes when approval comes from a different user? How would checkpoints
work across concurrent workers or retries after a crash?

Describe this as an AI-assisted reference implementation. Use real deployments
and business results only when you can substantiate them from your own work.
