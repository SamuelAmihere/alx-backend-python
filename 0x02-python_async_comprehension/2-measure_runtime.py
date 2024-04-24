#!/usr/bin/env python3
"""
Async - Comprehension:

execute async_comprehension four times in parallel using asyncio.gather.
"""
import asyncio
from time import time
from typing import List
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    Coroutine that will execute async_comprehension four times in
    parallel using asyncio.gather
    """
    start = time()
    await asyncio.gather(*(async_comprehension() for _ in range(4)))
    end = time()
    return end - start
