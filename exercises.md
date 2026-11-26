# Exercises and where the solutions are

| # | Problem | Solution |
|---|---|---|
| P1-P6 | Predict the output and timing (sequential vs tasks, `create_task` order, blocking `sleep`) | No code: see the answers in [cheatsheet.md](cheatsheet.md) |
| C1 | Run three sleepers concurrently | [concurrent_sleep.py](01_concurrency_basics/concurrent_sleep.py) |
| C2 | Limit 10 tasks to N at a time | [semaphore_limit.py](03_semaphore/semaphore_limit.py) |
| C3 | One task fails: `gather` vs `TaskGroup` | [gather_failures.py](02_gather_and_taskgroup/gather_failures.py), [taskgroup_failures.py](02_gather_and_taskgroup/taskgroup_failures.py) |
| C4 | Timeout a slow task | [timeout_cancel.py](04_timeout_and_cancellation/timeout_cancel.py) |
| C5 | Producer and consumers with a queue | [producer_consumer.py](05_queue/producer_consumer.py) |
| C6 | Make a blocking call concurrent | [to_thread.py](06_blocking_calls/to_thread.py) |
| C7 | Open-Meteo geocoding: loop vs `gather` vs semaphore | not done |
| G1 | Cancellation, with and without re-raising | [cancellation.py](04_timeout_and_cancellation/cancellation.py) |
| G2 | `TaskGroup` cancels siblings | [taskgroup_failures.py](02_gather_and_taskgroup/taskgroup_failures.py) |
| G3 | Async context manager (class and decorator) | [async_context_manager.py](08_async_context_and_generators/async_context_manager.py) |
| G4 | Async generators | [async_generator.py](08_async_context_and_generators/async_generator.py) |
| G5 | `Lock`: a race across an `await` | [lock_counter.py](07_event_and_lock/lock_counter.py) |
| G6 | `Event` as a start signal | [event_gate.py](07_event_and_lock/event_gate.py) |
| G7 | Debug mode (`asyncio.run(..., debug=True)`) | not done |
| G8 | Testing async code with `pytest-asyncio` | not done |
| extra | CPU-bound work in a process pool | [process_pool.py](09_process_pool/process_pool.py) |
| extra | A mini event loop | [mini_event_loop.py](10_event_loop_internals/mini_event_loop.py) |
