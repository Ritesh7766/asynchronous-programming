# 09 Process pool (CPU-bound work)

Threads can't run Python code in parallel (the GIL), so CPU-bound jobs go to worker **processes**.

```python
loop = asyncio.get_running_loop()
with ProcessPoolExecutor() as pool:          # default: one worker per core
    results = await asyncio.gather(
        *(loop.run_in_executor(pool, count_primes, 200_000) for _ in range(4))
    )
```

`run_in_executor` submits the call and returns a future immediately. `await` suspends your task, so the loop stays free. Tested on a 20-core machine: four prime counts took 1.7 s in a row or in threads, 0.6 s in a pool.

## Rules

- The function must be at module level (picklable). No lambdas or local functions.
- Arguments and return values are pickled (copied). Don't pass large data; load it in the worker.
- Keep the `if __name__ == "__main__":` guard.
- Positional arguments only; use `functools.partial` for keyword arguments.
- Create the pool once and reuse it. Send chunks of work, not many tiny calls.
- Cancelling stops the waiting, not a job already running in a worker.

## How the pool works

One pool, many workers, one shared job queue. A worker that finishes takes the next job. The **OS** schedules worker processes onto cores. More workers than cores means time-slicing, so every job slows down and total time doesn't improve (uneven job lengths can show a small gain; real overhead removes it). Aim for about one worker per core.

[process_pool.html](../assets/process_pool.html) · [process_pool_vs_cores.html](../assets/process_pool_vs_cores.html)

## asyncio vs threads vs processes

| | asyncio | Threads | Processes |
|---|---|---|---|
| Parallel Python code? | No (one thread) | No (GIL) | Yes |
| Switches at | `await` only | Any point | OS decides |
| Best for | Many IO waits, async libraries | Blocking IO libraries | CPU-bound pure Python |
| Cost | Tiny per task | Small | Large (startup, pickling) |

Only CPU-bound work: use `ProcessPoolExecutor` directly. IO and CPU in one program, or CPU work inside something that must stay responsive: asyncio for coordination plus `run_in_executor` for the heavy parts.

Run: `python3 process_pool.py`.
