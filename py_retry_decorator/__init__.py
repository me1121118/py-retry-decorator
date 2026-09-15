import time
import random
import asyncio
import functools
import inspect
from typing import Tuple, Type, Callable, Optional, Any, Union

def retry(
    max_attempts: int = 3,
    delay: float = 0.5,
    backoff: float = 2.0,
    jitter: bool = True,
    exceptions: Union[Type[BaseException], Tuple[Type[BaseException], ...]] = (Exception,),
    on_retry: Optional[Callable[[int, BaseException, float], Any]] = None,
):
    """
    Decorator for retrying synchronous or asynchronous functions with exponential backoff.
    """
    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")

    def decorator(func: Callable):
        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                current_delay = delay
                for attempt in range(1, max_attempts + 1):
                    try:
                        return await func(*args, **kwargs)
                    except exceptions as exc:
                        if attempt == max_attempts:
                            raise
                        
                        sleep_time = current_delay
                        if jitter:
                            sleep_time *= (0.5 + random.random())

                        if on_retry:
                            res = on_retry(attempt, exc, sleep_time)
                            if inspect.iscoroutine(res):
                                await res

                        await asyncio.sleep(sleep_time)
                        current_delay *= backoff
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                current_delay = delay
                for attempt in range(1, max_attempts + 1):
                    try:
                        return func(*args, **kwargs)
                    except exceptions as exc:
                        if attempt == max_attempts:
                            raise
                        
                        sleep_time = current_delay
                        if jitter:
                            sleep_time *= (0.5 + random.random())

                        if on_retry:
                            on_retry(attempt, exc, sleep_time)

                        time.sleep(sleep_time)
                        current_delay *= backoff
            return sync_wrapper

    return decorator
