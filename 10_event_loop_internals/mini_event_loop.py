"""A minimal event loop in ~60 lines: ready queue, timers, tasks, ``gather``.

A reference implementation for understanding asyncio, not for real use.
It supports ``create_task``, ``sleep`` and ``gather``. There is no real IO,
cancellation or exception handling.

How it maps to asyncio:
    ready deque              the ready queue
    task.coro.send(None)     resume a task from the line after its last await
    yield self (__await__)   ``await`` handing control back to the loop
    StopIteration            a coroutine returning (the value is the result)
    timers heap              ``asyncio.sleep`` timers
    task.waiters             tasks parked until another task finishes
"""

import heapq
import itertools
import time
from collections import deque

ready: deque = deque()  # tasks that can run now
timers: list = []  # (wake_time, tie_breaker, task)
_tie = itertools.count()


class Sleep:
    """What a task hands to the loop when it must wait for ``secs``."""

    def __init__(self, secs: float) -> None:
        self.secs = secs

    def __await__(self):
        yield self  # suspends the coroutine; the loop receives ``self``


class Task:
    """A coroutine plus its stored result and the tasks waiting on it."""

    def __init__(self, coro) -> None:
        self.coro, self.done, self.result, self.waiters = coro, False, None, []

    def __await__(self):
        if not self.done:
            yield self  # "I'm waiting for this task"
        return self.result


def create_task(coro) -> Task:
    """Schedule ``coro``: it joins the ready queue but does not start yet."""
    task = Task(coro)
    ready.append(task)
    return task


async def sleep(secs: float) -> None:
    """Suspend the calling task for ``secs`` seconds."""
    await Sleep(secs)


async def gather(*coros) -> list:
    """Schedule all coroutines, then collect their results in input order."""
    tasks = [create_task(c) for c in coros]
    return [await t for t in tasks]


def run(main_coro):
    """Run ``main_coro`` to completion and return its result."""
    main = create_task(main_coro)
    while not main.done:
        now = time.monotonic()
        while timers and timers[0][0] <= now:  # wake tasks whose timer expired
            ready.append(heapq.heappop(timers)[2])
        if not ready:  # nothing to run: idle until the next timer
            time.sleep(max(0, timers[0][0] - time.monotonic()))
            continue
        task = ready.popleft()
        try:
            request = task.coro.send(None)  # resume until the next await
        except StopIteration as stop:  # the coroutine returned
            task.done, task.result = True, stop.value
            ready.extend(task.waiters)  # wake whoever awaited it
            continue
        if isinstance(request, Sleep):
            heapq.heappush(timers, (time.monotonic() + request.secs, next(_tie), task))
        elif request.done:  # awaited task already finished
            ready.append(task)
        else:
            request.waiters.append(task)  # park until that task finishes
    return main.result


async def work(n: int) -> int:
    """Demo job: sleep 1 s and return ``n`` squared."""
    print(f"start {n}")
    await sleep(1)
    print(f"end   {n}")
    return n * n


async def demo() -> list:
    return await gather(work(1), work(2), work(3))


if __name__ == "__main__":
    t0 = time.monotonic()
    print(run(demo()), f"in {time.monotonic() - t0:.1f}s")  # [1, 4, 9] in ~1.0s
