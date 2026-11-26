# 04 Timeout and cancellation

`task.cancel()` is a **request**. The task receives `CancelledError` at the `await` where it is suspended.

```python
try:
    async with asyncio.timeout(2):       # cancels what is awaited inside the block
        await task
except TimeoutError:                     # the cancellation becomes a TimeoutError
    ...
```

- Cancellation is delivered into the task. `finally` blocks run.
- Catch `CancelledError` only to clean up, then **re-raise** it (or use `try/finally`).
- If a task swallows it, `await task` returns normally and `task.cancelled()` is `False`. Cancellers (timeouts, `TaskGroup`) can't tell it was cancelled. Swallowing inside a loop makes the task never stop.
- `asyncio.timeout` only cancels what is awaited **inside** the block.
- After `cancel()`, `await` the task (or `gather` it) to wait for it to actually stop.
- `TimeoutError` is the built-in from Python 3.11. Older versions use `asyncio.TimeoutError`.

| `reraise` | `await task` | `task.cancelled()` |
|---|---|---|
| `True` | raises `CancelledError` | `True` |
| `False` | returns `None` | `False` (the bug) |

Run: `python3 timeout_cancel.py`, `python3 cancellation.py`.
