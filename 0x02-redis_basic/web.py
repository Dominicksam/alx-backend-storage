#!/usr/bin/env python3

import requests
import redis
from typing import Callable
from functools import wraps

# Initialize Redis
cache = redis.Redis()

def cache_page(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(url: str) -> str:
        # Check if the result is in the cache
        cached_result = cache.get(url)
        if cached_result:
            return cached_result.decode('utf-8')

        # Get the HTML content using the original function
        result = func(url)

        # Store the result in the cache with an expiration time of 10 seconds
        cache.setex(url, 10, result)

        return result
    return wrapper

@cache_page
def get_page(url: str) -> str:
    # Track the number of accesses to the URL
    cache.incr(f"count:{url}")

    # Get the HTML content
    response = requests.get(url)
    return response.text
