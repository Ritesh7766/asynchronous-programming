# 02 gather and TaskGroup

What happens when one task fails.

| | `gather(..., return_exceptions=True)` | `TaskGroup` (3.11+) |
|---|---|---|
| Others when one fails | Keep running and finish | **Cancelled** |
| The failure | A value in the result list | Raised as an `ExceptionGroup` |
| Results | List in input order | From each task object |
| Use when | Partial results are useful | One failure makes the rest pointless |

```python
results = await asyncio.gather(*coros, return_exceptions=True)
failed = [r for r in results if isinstance(r, Exception)]
```

```python
try:
    async with asyncio.TaskGroup() as tg:          # leaving the block = wait for all
        tasks = [tg.create_task(work(i)) for i in range(5)]
except* ValueError as eg:                          # except*, not except
    print([repr(e) for e in eg.exceptions])
for t in tasks:                                    # results come from the tasks
    if t.cancelled():
        print("cancelled")
    elif t.exception() is not None:
        print("failed:", t.exception())
    else:
        print(t.result())
```

- No `await` line is needed with `TaskGroup`: the end of the `async with` block is the wait.
- Check `t.cancelled()` before `t.exception()` (it raises on a cancelled task).
- `t.result()` only works on a finished task; `await t` is the form that waits.
- `return_exceptions=True` hides errors if you never look at the results.

Run: `python3 gather_failures.py`, `python3 taskgroup_failures.py`.
