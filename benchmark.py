import asyncio
import argparse
import statistics
import time
from typing import Callable

from async_app import run_async
from threaded_app import run_threaded


def measure_sync(fn: Callable[[], object]) -> float:
    started = time.perf_counter()
    fn()
    return time.perf_counter() - started


def measure_async() -> float:
    started = time.perf_counter()
    asyncio.run(run_async())
    return time.perf_counter() - started


def summarize(samples: list[float]) -> dict[str, float]:
    return {
        "avg": statistics.mean(samples),
        "min": min(samples),
        "max": max(samples),
    }


def format_row(name: str, stats: dict[str, float], width: int = 14) -> str:
    return (
        f"{name:<{width}}"
        f"{stats['avg']:>10.4f}s"
        f"{stats['min']:>10.4f}s"
        f"{stats['max']:>10.4f}s"
    )


def main(rounds: int = 8, thread_workers: int = 8, async_limit: int = 40) -> None:
    threaded_samples: list[float] = []
    async_samples: list[float] = []

    print(f"Running benchmark for {rounds} rounds each...")
    print(
        f"Settings: thread_workers={thread_workers}, async_concurrency_limit={async_limit}"
    )

    for round_no in range(1, rounds + 1):
        t_time = measure_sync(lambda: run_threaded(max_workers=thread_workers))
        a_time = measure_sync(lambda: asyncio.run(run_async(concurrency_limit=async_limit)))

        threaded_samples.append(t_time)
        async_samples.append(a_time)

        print(
            f"Round {round_no:>2}: threaded={t_time:.4f}s | async={a_time:.4f}s"
        )

    thread_stats = summarize(threaded_samples)
    async_stats = summarize(async_samples)

    print("\nSummary (side by side)")
    print(f"{'Implementation':<14}{'Average':>10}{'Min':>10}{'Max':>10}")
    print("-" * 44)
    print(format_row("threaded", thread_stats))
    print(format_row("async", async_stats))

    speedup = thread_stats["avg"] / async_stats["avg"]
    print(f"\nAverage speedup (threaded/async): {speedup:.2f}x")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Benchmark threaded vs async implementations side by side."
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=8,
        help="Number of benchmark rounds per implementation (default: 8).",
    )
    parser.add_argument(
        "--thread-workers",
        type=int,
        default=8,
        help="Number of worker threads for threaded implementation (default: 8).",
    )
    parser.add_argument(
        "--async-limit",
        type=int,
        default=40,
        help="Concurrency limit for async implementation (default: 40).",
    )

    args = parser.parse_args()

    if args.rounds < 1:
        parser.error("--rounds must be >= 1")
    if args.thread_workers < 1:
        parser.error("--thread-workers must be >= 1")
    if args.async_limit < 1:
        parser.error("--async-limit must be >= 1")

    return args


if __name__ == "__main__":
    cli_args = parse_args()
    main(
        rounds=cli_args.rounds,
        thread_workers=cli_args.thread_workers,
        async_limit=cli_args.async_limit,
    )
