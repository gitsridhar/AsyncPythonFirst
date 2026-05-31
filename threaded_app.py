import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

URLS = [f"https://service.local/resource/{i}" for i in range(1, 41)]


# Simulates a blocking I/O operation like a network request.
def fetch_resource(url: str) -> dict:
    latency = random.uniform(0.05, 0.25)
    time.sleep(latency)
    return {
        "url": url,
        "latency": latency,
        "thread": threading.current_thread().name,
    }


def run_threaded(max_workers: int = 8) -> list[dict]:
    started = time.perf_counter()
    results: list[dict] = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(fetch_resource, url): url for url in URLS}

        for future in as_completed(future_to_url):
            results.append(future.result())

    elapsed = time.perf_counter() - started
    print(f"Threaded run finished in {elapsed:.3f}s using {max_workers} worker threads.")
    print(f"Collected {len(results)} responses.")

    return results


if __name__ == "__main__":
    run_threaded()
