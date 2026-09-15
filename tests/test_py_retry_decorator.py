import pytest
from py_retry_decorator import retry

def test_sync_retry_success():
    calls = 0
    @retry(max_attempts=3, delay=0.01, jitter=False)
    def flaky_func():
        nonlocal calls
        calls += 1
        if calls < 3:
            raise ValueError("Temporary failure")
        return "success"

    res = flaky_func()
    assert res == "success"
    assert calls == 3

def test_sync_retry_failure():
    calls = 0
    @retry(max_attempts=2, delay=0.01, jitter=False, exceptions=(ValueError,))
    def always_fails():
        nonlocal calls
        calls += 1
        raise ValueError("Permanent failure")

    with pytest.raises(ValueError, match="Permanent failure"):
        always_fails()
    assert calls == 2

@pytest.mark.asyncio
async def test_async_retry_success():
    calls = 0
    retried_attempts = []

    def on_retry_hook(attempt, exc, delay):
        retried_attempts.append(attempt)

    @retry(max_attempts=3, delay=0.01, jitter=False, on_retry=on_retry_hook)
    async def async_flaky():
        nonlocal calls
        calls += 1
        if calls < 2:
            raise RuntimeError("Async glitch")
        return 42

    res = await async_flaky()
    assert res == 42
    assert calls == 2
    assert retried_attempts == [1]
