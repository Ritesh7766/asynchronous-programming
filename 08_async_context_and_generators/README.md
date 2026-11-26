# 08 Async context managers and generators

## `async with`

Awaits `__aenter__` before the block and `__aexit__` after it, even if the block raises. `as x` receives what `__aenter__` returns.

```python
class Resource:
    async def __aenter__(self):
        ...                                   # open
        return self                           # what `as r` receives

    async def __aexit__(self, exc_type, exc, tb):
        ...                                   # close (runs on error too)
        return False                          # a truthy value would suppress the error

@asynccontextmanager
async def resource():
    ...                       # enter
    try:
        yield value           # the block runs here
    finally:
        ...                   # exit (runs on error too)
```

`asyncio.timeout(...)`, `TaskGroup()` and `async with sem` are all async context managers.

## `async for`

```python
async def countdown(n) -> AsyncIterator[int]:
    for i in range(n, 0, -1):
        await asyncio.sleep(0.2)
        yield i

async for i in countdown(3): ...
values = [i async for i in countdown(3)]
```

- No `yield from` in an async generator. The return type is `AsyncIterator`, not `Iterator`.
- A plain `for` on one raises `TypeError`. Each step may suspend, so the loop needs `async for`.

Run: `python3 async_context_manager.py`, `python3 async_generator.py`.
