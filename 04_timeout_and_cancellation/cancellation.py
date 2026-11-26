"""Cancelling a task, and why swallowing ``CancelledError`` is a bug.

``forever`` ticks every second and is cancelled after 3.5 s. It catches
``CancelledError`` to clean up, then either re-raises it (correct) or not.
"""

import asyncio


async def forever(reraise: bool) -> None:
    """Tick once a second until cancelled."""
    tick = 0
    try:
        while True:
            await asyncio.sleep(1)
            tick += 1
            print(f"tick {tick}")
    except asyncio.CancelledError:
        print("cleaning up")
        if reraise:
            raise  # let the cancellation propagate


async def main(reraise: bool) -> None:
    print(f"--- reraise={reraise}")
    task = asyncio.create_task(forever(reraise))
    await asyncio.sleep(3.5)  # 3.5 s so tick 3 isn't racing the cancel
    task.cancel()
    try:
        result = await task
        print("await task returned normally:", result)
    except asyncio.CancelledError:
        print("await task raised CancelledError")
    print("task.cancelled():", task.cancelled())


if __name__ == "__main__":
    asyncio.run(main(reraise=True))  # task.cancelled() is True
    asyncio.run(main(reraise=False))  # looks like a normal finish: the bug
