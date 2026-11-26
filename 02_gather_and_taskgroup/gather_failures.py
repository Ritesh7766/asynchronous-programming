"""``gather(return_exceptions=True)``: a failure becomes a value in the results.

The other tasks keep running and finish normally. Check each result with
``isinstance`` to find out which task failed.
"""

import asyncio


async def work(n: int) -> int:
    """Return ``n`` squared after 1 s; task 3 raises."""
    print(f"task {n} initiated")
    await asyncio.sleep(1)
    if n == 3:
        raise ValueError("I don't like 3")
    return n * n


async def main() -> None:
    results = await asyncio.gather(
        *(work(i) for i in range(5)), return_exceptions=True
    )
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"task {i} failed: {result!r}")
        else:
            print(f"task {i} -> {result}")


if __name__ == "__main__":
    asyncio.run(main())
