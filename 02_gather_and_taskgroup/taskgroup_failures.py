"""``TaskGroup``: one failure cancels the rest and raises an ``ExceptionGroup``.

Task 3 fails after 1 s; the others would sleep for 10 s. The group cancels
them, so the whole block ends after ~1 s. Their ``finally`` blocks still run.
"""

import asyncio
import time


async def work(i: int) -> int:
    """Sleep for 10 s and return ``i``; task 3 raises after 1 s instead."""
    try:
        if i == 3:
            await asyncio.sleep(1)
            raise ValueError(f"task {i} failed")
        await asyncio.sleep(10)
        return i
    finally:
        print(f"task {i} cleanup")


def describe(task: asyncio.Task) -> str:
    """Summarise a finished task. Check ``cancelled()`` first: ``exception()`` raises on a cancelled task."""
    if task.cancelled():
        return "cancelled"
    if task.exception() is not None:
        return f"failed: {task.exception()!r}"
    return f"result {task.result()}"


async def main() -> None:
    t0 = time.perf_counter()
    tasks: list[asyncio.Task] = []  # defined up front so it exists if the group fails
    try:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(work(i)) for i in range(5)]
        # leaving the block waits for every task in the group
    except* ValueError as eg:  # except*, because errors arrive wrapped in a group
        print("caught:", [repr(e) for e in eg.exceptions])
    print(f"block took {time.perf_counter() - t0:.1f}s")
    for i, task in enumerate(tasks):
        print(i, describe(task))


if __name__ == "__main__":
    asyncio.run(main())
