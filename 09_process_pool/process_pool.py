"""CPU-bound work: ``loop.run_in_executor`` with a ``ProcessPoolExecutor``.

Threads can't run Python code in parallel (the GIL), so CPU-bound jobs go to
worker *processes*. ``run_in_executor`` submits the call and returns a future
that ``await``/``gather`` can wait on, so the event loop stays free.

Rules: the function must be defined at module level (picklable), arguments
and results are pickled, and the ``__main__`` guard is required.
"""

import asyncio
import time
from concurrent.futures import ProcessPoolExecutor

N_JOBS = 8
LIMIT = 200_000


def count_primes(limit: int) -> int:
    """Count the primes below ``limit`` (CPU-bound, top-level, picklable)."""
    count = 0
    for n in range(2, limit):
        if all(n % d for d in range(2, int(n**0.5) + 1)):
            count += 1
    return count


async def main() -> None:
    loop = asyncio.get_running_loop()
    t0 = time.perf_counter()
    with ProcessPoolExecutor() as pool:  # default: one worker per core
        results = await asyncio.gather(
            *(loop.run_in_executor(pool, count_primes, LIMIT) for _ in range(N_JOBS))
        )
    print(results, f"in {time.perf_counter() - t0:.1f}s")


if __name__ == "__main__":
    asyncio.run(main())
