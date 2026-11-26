"""Sequential vs concurrent: the same three jobs, three ways.

Each ``work(n)`` sleeps ``n`` seconds. Awaiting them one by one takes about
1 + 2 + 3 = 6 s. Running them concurrently takes about 3 s, the slowest one.
"""

import asyncio
import time


async def work(n: int) -> int:
    """Sleep for ``n`` seconds, then return ``n`` squared."""
    await asyncio.sleep(n)
    return n * n


async def sequential() -> list[int]:
    """Await each coroutine in turn: the waits add up (~6 s)."""
    return [await work(n) for n in range(1, 4)]


async def with_gather() -> list[int]:
    """Schedule all coroutines as tasks inside ``gather`` (~3 s)."""
    coros = [work(n) for n in range(1, 4)]  # coroutine objects: nothing runs yet
    return await asyncio.gather(*coros)


async def with_tasks() -> list[int]:
    """Create the tasks explicitly, then wait for all of them (~3 s)."""
    tasks = [asyncio.create_task(work(n)) for n in range(1, 4)]  # scheduled now
    return [await t for t in tasks]  # awaiting after creating: still concurrent


async def timed(label: str, fn) -> None:
    """Run ``fn`` and print its result and wall-clock time."""
    t0 = time.perf_counter()
    result = await fn()
    print(f"{label:<10} {result} in {time.perf_counter() - t0:.1f}s")


async def main() -> None:
    await timed("sequential", sequential)
    await timed("gather", with_gather)
    await timed("tasks", with_tasks)


if __name__ == "__main__":
    asyncio.run(main())
