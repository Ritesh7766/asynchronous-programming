"""Async context managers: the class form and the decorator form.

``async with`` awaits ``__aenter__`` before the block and ``__aexit__`` after
it, even if the block raises. ``as x`` receives what ``__aenter__`` returns.
"""

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager


class Resource:
    """Class form: implement ``__aenter__`` and ``__aexit__``."""

    async def __aenter__(self) -> "Resource":
        await asyncio.sleep(0.2)
        print("open")
        return self  # this is what `as r` receives

    async def __aexit__(self, exc_type, exc, tb) -> bool:
        await asyncio.sleep(0.2)
        print("close", f"(error: {exc_type.__name__})" if exc_type else "")
        return False  # a truthy value would suppress the exception


@asynccontextmanager
async def resource() -> AsyncIterator[str]:
    """Decorator form: code before ``yield`` is enter, after it is exit."""
    await asyncio.sleep(0.2)
    print("open")
    try:
        yield "the resource"  # the block runs here
    finally:  # without try/finally, an error in the block skips the cleanup
        await asyncio.sleep(0.2)
        print("close")


async def main() -> None:
    async with Resource() as r:
        print("class: inside", r)
    try:
        async with Resource():
            raise ValueError("boom")
    except ValueError as e:
        print("class: caught", e)

    async with resource() as r:
        print("generator: inside", r)
    try:
        async with resource():
            raise ValueError("boom")
    except ValueError as e:
        print("generator: caught", e)


if __name__ == "__main__":
    asyncio.run(main())
