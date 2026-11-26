# 05 Queue (producer / consumer)

```python
async def consumer(queue):
    while True:
        item = await queue.get()        # parked here while the queue is empty
        try:
            ...                         # work
        finally:
            queue.task_done()           # one per get()

workers = [create_task(consumer(queue)) for _ in range(3)]
await producer(queue)
await queue.join()                      # all items processed
for w in workers: w.cancel()
await asyncio.gather(*workers, return_exceptions=True)
```

- The queue keeps a count of unfinished items: `put` +1, `task_done` -1, `join()` waits for 0. `get()` alone doesn't change it.
- An empty queue means "no items left to take", not "all work finished": that is why you need `join()`.
- Don't write `while not queue.empty()` in a consumer: the check goes stale before `get()` and a worker can wait forever.
- `put` on an unbounded queue never suspends. Use `Queue(maxsize=n)` for backpressure.
- A woken worker resumes on the same line. A `put` only marks a parked worker ready; it runs when the producer next suspends.
- Always call `task_done()` in a `finally`, or `join()` can hang.

Run: `python3 producer_consumer.py` (3 workers, 10 one-second items, about 4 s).
