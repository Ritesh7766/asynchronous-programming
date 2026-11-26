"""``asyncio.Lock``: races are still possible when an ``await`` sits in the middle.

asyncio never interrupts a task, but at any ``await`` another task can run.
A read-modify-write with an ``await`` between the read and the write loses
updates unless the whole sequence is inside a lock.
"""

import asyncio

N_WORKERS = 100


async def unsafe_worker(state: dict[str, int]) -> None:
    """Read, yield to the loop, then write back a possibly stale value."""
    value = state["counter"]  # read
    await asyncio.sleep(0)  # other tasks run here
    state["counter"] = value + 1  # write


async def safe_worker(state: dict[str, int], lock: asyncio.Lock) -> None:
    """Same sequence, but only one task at a time can be inside the lock."""
    async with lock:
        value = state["counter"]
        await asyncio.sleep(0)
        state["counter"] = value + 1


async def main() -> None:
    state = {"counter": 0}
    await asyncio.gather(*(unsafe_worker(state) for _ in range(N_WORKERS)))
    print(f"without lock: {state['counter']} (expected {N_WORKERS})")

    state = {"counter": 0}
    lock = asyncio.Lock()
    await asyncio.gather(*(safe_worker(state, lock) for _ in range(N_WORKERS)))
    print(f"with lock:    {state['counter']} (expected {N_WORKERS})")


if __name__ == "__main__":
    asyncio.run(main())
