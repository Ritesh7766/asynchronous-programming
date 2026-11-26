"""A blocking call freezes the event loop; ``asyncio.to_thread`` fixes it.

``blocking_task`` sleeps with ``time.sleep``, which never yields to the loop.
Called directly, three of them take ~3 s. Run in worker threads they overlap
and take ~1 s. Pass the function and its arguments *separately*:
``to_thread(fn, arg)``, not ``to_thread(fn(arg))``.
"""

import asyncio
import time


def blocking_task(n: int) -> int:
    """A plain (sync) function that blocks for 1 s."""
    print(f"task {n}")
    time.sleep(1)
    return n


async def in_loop(n: int) -> int:
    """Call the blocking function on the loop's thread: nothing else can run."""
    return blocking_task(n)


async def in_thread(n: int) -> int:
    """Run the blocking function in a worker thread; the loop stays free."""
    return await asyncio.to_thread(blocking_task, n)


async def timed(label: str, fn) -> None:
    """Run ``fn`` for three jobs concurrently and print the wall-clock time."""
    t0 = time.perf_counter()
    results = await asyncio.gather(*(fn(i) for i in range(3)))
    print(f"{label}: {results} in {time.perf_counter() - t0:.1f}s\n")


async def main() -> None:
    await timed("in loop (blocks) ", in_loop)  # ~3 s
    await timed("to_thread        ", in_thread)  # ~1 s


if __name__ == "__main__":
    asyncio.run(main())
