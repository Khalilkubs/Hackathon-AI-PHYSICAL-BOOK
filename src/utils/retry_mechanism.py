"""
Implement retry mechanism with exponential backoff
Task T008: Implement retry mechanism with exponential backoff
"""

import time
import random
from functools import wraps
from typing import Callable, Type, Any
import logging

logger = logging.getLogger(__name__)


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """
    Decorator that implements retry with exponential backoff
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_retries:
                        # Last attempt, raise the exception
                        logger.error(f"Function {func.__name__} failed after {max_retries} retries: {e}")
                        raise e

                    # Calculate delay with exponential backoff and jitter
                    delay = min(base_delay * (backoff_factor ** attempt), max_delay)
                    jitter = random.uniform(0, 0.1 * delay)  # Add up to 10% jitter
                    total_delay = delay + jitter

                    logger.warning(
                        f"Attempt {attempt + 1} failed for {func.__name__}: {e}. "
                        f"Retrying in {total_delay:.2f} seconds..."
                    )
                    time.sleep(total_delay)

            # This should never be reached, but included for type safety
            raise last_exception

        return wrapper
    return decorator


class RetryHandler:
    """
    Class-based approach for retry mechanism with exponential backoff
    """
    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        backoff_factor: float = 2.0,
        exceptions: tuple = (Exception,)
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.exceptions = exceptions

    def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute a function with retry logic
        """
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except self.exceptions as e:
                last_exception = e
                if attempt == self.max_retries:
                    # Last attempt, raise the exception
                    logger.error(f"Function {func.__name__} failed after {self.max_retries} retries: {e}")
                    raise e

                # Calculate delay with exponential backoff and jitter
                delay = min(self.base_delay * (self.backoff_factor ** attempt), self.max_delay)
                jitter = random.uniform(0, 0.1 * delay)  # Add up to 10% jitter
                total_delay = delay + jitter

                logger.warning(
                    f"Attempt {attempt + 1} failed for {func.__name__}: {e}. "
                    f"Retrying in {total_delay:.2f} seconds..."
                )
                time.sleep(total_delay)

        # This should never be reached, but included for type safety
        raise last_exception


# Example usage functions
def retry_on_api_errors(func: Callable) -> Callable:
    """
    Convenience decorator for API calls that might fail
    """
    return retry_with_backoff(
        max_retries=3,
        base_delay=1.0,
        max_delay=30.0,
        backoff_factor=2.0,
        exceptions=(ConnectionError, TimeoutError, RuntimeError)
    )


def retry_on_network_errors(func: Callable) -> Callable:
    """
    Convenience decorator for network operations that might fail
    """
    return retry_with_backoff(
        max_retries=5,
        base_delay=0.5,
        max_delay=60.0,
        backoff_factor=2.0,
        exceptions=(ConnectionError, TimeoutError, ConnectionResetError)
    )