# Python Multithreading to Async Example

This mini project shows the same I/O-heavy workflow in two styles:

- `threaded_app.py`: thread-based concurrency using `ThreadPoolExecutor`
- `async_app.py`: event-loop concurrency using `asyncio`

## 1) Multithreading Version

The threaded app simulates downloading 40 resources.
Each request blocks for a small delay using `time.sleep`.
Multiple threads run these blocking calls concurrently.

Run:

```bash
python3 threaded_app.py
```

## 2) Disadvantages of the Multithreading Approach

Even though multithreading can speed up I/O-bound workloads, it has drawbacks:

1. **Higher memory overhead**
Each thread has stack and scheduling overhead.
With high concurrency (thousands of requests), thread count can become expensive.

2. **Context-switch cost**
The OS switches between threads, adding overhead as thread counts grow.

3. **Synchronization complexity**
Shared state often requires locks/queues.
This increases bug risk (deadlocks, race conditions).

4. **Harder observability/debugging**
Interleaved execution and timing-sensitive bugs can be difficult to reproduce.

5. **Not ideal for extreme I/O fan-out**
For workloads dominated by waiting (network, sockets), event-loop models typically scale better.

## 3) Async Enhancement

The async app does the same simulation with coroutines (`asyncio`).
Instead of blocking each worker thread, tasks cooperatively yield control using `await`.

Run:

```bash
python3 async_app.py
```

## Why Async Is Better Here

- Lower overhead for large numbers of waiting operations
- Fewer OS-level threads
- Explicit, cooperative scheduling at `await` points
- Easier to cap concurrency with an `asyncio.Semaphore`

## Notes

- Async gives the largest benefit for I/O-bound workloads.
- For CPU-bound tasks, use multiprocessing or native extensions.
- In CPython, the GIL limits true parallelism for pure Python CPU-bound threads.

## 4) Benchmark Both Versions Side by Side

Run:

```bash
python3 benchmark.py
```

Optional tuning flags:

```bash
python3 benchmark.py --rounds 12 --thread-workers 10 --async-limit 60
```

This executes both implementations multiple times and prints:

- Per-round timing for threaded vs async
- Aggregate `Average`, `Min`, and `Max` for each
- Average speedup ratio (`threaded / async`)
