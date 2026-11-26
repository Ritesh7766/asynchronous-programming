"""Limit concurrency with a semaphore.

All 10 tasks are created and start, but only ``MAX_CONCURRENCY`` at a time get
inside ``async with sem``. The rest wait at that line. With a limit of 5 and
1 s of work each, the run takes ~2 s (two batches).
"""

import asyncio
import time

MAX_CONCURRENCY = 5
N_TASKS = 10


async def work(n: int, sem: asyncio.Semaphore, t0: float) -> int:
    """Do 1 s of 'work' inside the semaphore and return ``n`` squared."""
    async with sem:  # at most MAX_CONCURRENCY tasks in here at once
        print(f"{time.perf_counter() - t0:3.1f}s  task {n} initiated")
        await asyncio.sleep(1)
    return n * n


async def main() -> None:
    t0 = time.perf_counter()
    sem = asyncio.Semaphore(MAX_CONCURRENCY)
    results = await asyncio.gather(*(work(i, sem, t0) for i in range(N_TASKS)))
    print(f"{time.perf_counter() - t0:3.1f}s  completed: {results}")


if __name__ == "__main__":
    asyncio.run(main())
