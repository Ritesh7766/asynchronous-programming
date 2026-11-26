"""Producer / consumer with ``asyncio.Queue``.

Workers wait on ``queue.get()`` (parked while the queue is empty). ``main``
waits for ``queue.join()``, which returns once every item has been marked
done with ``task_done()``, then cancels the idle workers.

Don't use ``while not queue.empty()`` in a consumer: the check goes stale
before the ``get()`` and a worker can wait forever.
"""

import asyncio

N_WORKERS = 3
N_ITEMS = 10


async def producer(queue: asyncio.Queue, pid: int, n: int) -> None:
    """Put ``n`` items on the queue, 0.1 s apart."""
    for i in range(n):
        print(f"producer put {i}")
        await queue.put(f"producer {pid}_{i}")
        await asyncio.sleep(0.1)


async def consumer(queue: asyncio.Queue, cid: int) -> None:
    """Take items forever; stops only when cancelled."""
    while True:
        item = await queue.get()  # waits here when the queue is empty
        try:
            await asyncio.sleep(1)  # "work"
            print(f"{item} handled by worker {cid}")
        finally:
            queue.task_done()  # one task_done() per get()


async def main() -> None:
    queue: asyncio.Queue = asyncio.Queue()
    workers = [asyncio.create_task(consumer(queue, i)) for i in range(N_WORKERS)]
    await producer(queue, 1, N_ITEMS)  # all items are queued
    await queue.join()  # waits until every item had task_done()
    for w in workers:
        w.cancel()  # workers are parked in queue.get(); stop them
    await asyncio.gather(*workers, return_exceptions=True)  # wait for them to stop


if __name__ == "__main__":
    asyncio.run(main())
