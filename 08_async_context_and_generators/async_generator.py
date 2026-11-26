"""Async generators: ``yield`` inside ``async def``, consumed with ``async for``.

There is no ``yield from`` in async generators, and the return type is
``AsyncIterator`` (not ``Iterator``). Each step may suspend at an ``await``.
"""

import asyncio
from collections.abc import AsyncIterator


async def countdown(n: int) -> AsyncIterator[int]:
    """Yield ``n`` down to 1, pausing between values."""
    for i in range(n, 0, -1):
        await asyncio.sleep(0.2)  # a real suspension point
        yield i


async def pages(total: int, page_size: int) -> AsyncIterator[list[int]]:
    """Stream fake 'pages' of items until the source is exhausted."""
    start = 0
    while start < total:
        await asyncio.sleep(0.2)  # pretend this is an API call
        yield list(range(start, min(start + page_size, total)))
        start += page_size


async def main() -> None:
    async for i in countdown(3):
        print(i)
    print([i async for i in countdown(3)])  # async comprehension
    async for page in pages(total=7, page_size=3):
        print("page:", page)


if __name__ == "__main__":
    asyncio.run(main())
