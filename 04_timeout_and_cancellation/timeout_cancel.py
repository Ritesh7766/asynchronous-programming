"""``asyncio.timeout``: cancel what is being awaited after a deadline.

After 2 s the timeout cancels ``main``'s ``await task``; the cancellation
passes on to ``work``, whose ``finally`` runs, and ``main`` sees a
``TimeoutError``.
"""

import asyncio


async def work(n: int) -> int:
    """Sleep for 5 s, then return ``n`` squared."""
    try:
        await asyncio.sleep(5)
        return n * n
    finally:
        print("work: cleanup ran")  # runs when the task is cancelled


async def main() -> None:
    task = asyncio.create_task(work(5))
    try:
        async with asyncio.timeout(2):
            print(await task)
    except TimeoutError:
        print("timed out")
    finally:
        print("main: clean")
    print("task cancelled?", task.cancelled())  # True


if __name__ == "__main__":
    asyncio.run(main())
