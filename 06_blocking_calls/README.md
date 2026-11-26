# 06 Blocking calls

A sync call inside a coroutine holds the thread until it returns. Nothing else runs: no tasks, no timers, no responses.

```python
async def bad():
    time.sleep(2)                  # freezes the whole loop
    requests.get(url)              # same

async def good():
    await asyncio.sleep(2)
    await client.get(url)                          # async client
    await asyncio.to_thread(blocking_fn, arg)      # blocking library you can't replace
```

- `to_thread(fn, arg)` takes the function and arguments **separately**. `to_thread(fn(arg))` calls `fn` right away on the loop thread, then fails.
- It is for **blocking IO**. For CPU-bound work threads share the GIL: use a [process pool](../09_process_pool).
- Check: would the call work if you removed `async`? Then it probably blocks.
- Debug: `asyncio.run(main(), debug=True)` warns about steps holding the loop longer than 0.1 s.

| | Time for 3 one-second calls |
|---|---|
| Called directly | ~3 s |
| `to_thread` | ~1 s |

Run: `python3 to_thread.py`.
