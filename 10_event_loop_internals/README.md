# 10 Event loop internals

[mini_event_loop.py](mini_event_loop.py) is a working event loop in about 60 lines (`create_task`, `sleep`, `gather`). It is a teaching aid, not a library.

| In the code | In asyncio |
|---|---|
| `ready` deque | The ready queue |
| `task.coro.send(None)` | Resume a task from the line after its last `await` |
| `yield self` in `__await__` | `await` handing control back to the loop |
| `StopIteration` | A coroutine returning; its value becomes the task's result |
| `timers` heap, `time.sleep` when idle | `asyncio.sleep`, and the idle thread |
| `task.waiters` | A task parked until another task finishes |

- A coroutine is like a generator: it keeps its own frame (locals and position), so it can pause and resume.
- The loop has no notion of "concurrency": it runs one task step at a time. Overlap comes from tasks yielding at their `await`s.
- Each waiting task is registered with what it waits for: the OS selector for sockets, a timer heap, a queue's list of getters, another task's callbacks.
- Not covered: real IO (`selectors`), exceptions, cancellation.

[event_loop.html](../assets/event_loop.html): the same mechanism as a step-by-step animation.

Run: `python3 mini_event_loop.py`.
