"""``asyncio.Event``: a one-time "go" signal that wakes every waiter.

Workers park on ``event.wait()``. ``event.set()`` moves all of them to the
ready queue at once. A worker arriving after ``set()`` doesn't wait at all.
"""

import asyncio
import time


async def worker(i: int, event: asyncio.Event, t0: float) -> None:
    """Wait for the event, then start."""
    print(f"{time.perf_counter() - t0:3.1f}s  worker {i} waiting")
    await event.wait()  # parked here until event.set()
    print(f"{time.perf_counter() - t0:3.1f}s  worker {i} started")


async def main() -> None:
    t0 = time.perf_counter()
    event = asyncio.Event()
    workers = [asyncio.create_task(worker(i, event, t0)) for i in range(3)]
    await asyncio.sleep(2)
    print(f"{time.perf_counter() - t0:3.1f}s  main: setting the event")
    event.set()  # wakes every waiting worker
    await asyncio.gather(*workers)


if __name__ == "__main__":
    asyncio.run(main())
