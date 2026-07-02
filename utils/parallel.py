"""Small helper utilities for safe parallel searches.

This module keeps ThreadPoolExecutor logic out of app.py so the UI stays cleaner.
It uses only Python's standard library, so there are no new requirements.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, Iterable


def run_parallel(
    tasks: Iterable[Any],
    worker: Callable[[Any], Any],
    *,
    max_workers: int = 8,
    progress_callback: Callable[[int, int, Any], None] | None = None,
) -> tuple[list[Any], list[str]]:
    """Run independent tasks in parallel and collect results.

    Args:
        tasks: Items to pass to the worker function.
        worker: Function that accepts one task and returns one result.
        max_workers: Maximum threads. Kept modest to avoid overwhelming sites.
        progress_callback: Optional callback receiving completed, total, task.

    Returns:
        (results, errors). Errors are strings so Streamlit can display them.
    """
    task_list = list(tasks)
    total = len(task_list)
    if total == 0:
        return [], []

    results: list[Any] = []
    errors: list[str] = []
    workers = max(1, min(max_workers, total))

    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_task = {executor.submit(worker, task): task for task in task_list}
        completed = 0

        for future in as_completed(future_to_task):
            task = future_to_task[future]
            completed += 1

            if progress_callback:
                progress_callback(completed, total, task)

            try:
                results.append(future.result())
            except Exception as exc:
                errors.append(f"{task}: {exc}")

    return results, errors
