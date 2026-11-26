# 07 Event and Lock

## Event: a one-time "go" signal

```python
event = asyncio.Event()
await event.wait()      # in each worker: parks until set()
event.set()             # wakes ALL waiters at once
```

- Each worker suspends itself at `wait()`. `set()` moves every waiter to the ready queue.
- `wait()` returns immediately if the event is already set. `clear()` closes the gate again.
- Uses: start signal, "initialisation done", a shutdown flag (`while not stop.is_set()`).

| Wakes | |
|---|---|
| `Event.set()` | **all** waiters, and stays open |
| `Semaphore` slot freed | **one** waiter |
| `Queue.put()` | **one** getter |

## Lock: races across an `await`

asyncio never interrupts a task, but at any `await` another task can run. A read-modify-write with an `await` in the middle loses updates.

```python
value = counter
await asyncio.sleep(0)       # other tasks run here
counter = value + 1          # writes a stale value
```

Without the lock, 100 workers give a counter of **1**; with `async with lock:` around the whole sequence it is 100. A single statement with no `await` (`counter += 1`) is safe.

Run: `python3 event_gate.py`, `python3 lock_counter.py`.
