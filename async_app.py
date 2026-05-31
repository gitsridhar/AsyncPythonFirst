import asyncio
import random
import time

URLS = [f"https://service.local/resource/{i}" for i in range(1, 41)]


# Simulates a non-blocking I/O operation using asyncio.
async def fetch_resource(url: str, semaphore: asyncio.Semaphore) -> dict:
    async with semaphore:
        latency = random.uniform(0.05, 0.25)
        await asyncio.sleep(latency)
        return {
            "url": url,
            "latency": latency,
            "task": asyncio.current_task().get_name() if asyncio.current_task() else "unknown",
        }


async def run_async(concurrency_limit: int = 40) -> list[dict]:
    started = time.perf_counter()
    semaphore = asyncio.Semaphore(concurrency_limit)

    tasks = [
        asyncio.create_task(fetch_resource(url, semaphore), name=f"fetch-{i}")
        for i, url in enumerate(URLS, start=1)
    ]

    results = await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - started

    print(
        f"Async run finished in {elapsed:.3f}s with concurrency limit {concurrency_limit}."
    )
    print(f"Collected {len(results)} responses.")

    return results


if __name__ == "__main__":
    asyncio.run(run_async())
