# py-retry-decorator

[![PyPI version](https://img.shields.io/badge/pypi-v0.1.0-blue.svg)](https://pypi.org/project/py-retry-decorator/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Lightweight zero-dependency retry decorator supporting both sync and async functions with exponential backoff and randomized jitter.

---

## 🚀 Features

- 🪶 **Zero Dependencies**: Pure Python standard library.
- 🔄 **Async & Sync Transparent**: One decorator `@retry` handles both `def` and `async def`.
- 📈 **Exponential Backoff & Jitter**: Avoids thundering herds on external services.
- 🎯 **Specific Exception Filtering**: Catch only retriable exceptions (e.g., `(TimeoutError, ConnectionError)`).
- 🪝 **Retry Callback**: Execute custom logging or metrics reporting on each retry attempt.

---

## 📦 Installation

```bash
pip install py-retry-decorator
```

---

## 🛠️ Quickstart

### Async Functions

```python
import httpx
from py_retry_decorator import retry

@retry(max_attempts=3, delay=0.5, backoff=2.0, exceptions=(httpx.RequestError,))
async def fetch_api(url: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(url, timeout=2.0)
        res.raise_for_status()
        return res.json()
```

### Sync Functions with Custom Callback

```python
from py_retry_decorator import retry

def on_retry_hook(attempt: int, exc: Exception, next_delay: float):
    print(f"Attempt {attempt} failed with {exc}. Retrying in {next_delay:.2f}s...")

@retry(max_attempts=4, delay=1.0, jitter=True, on_retry=on_retry_hook)
def connect_db():
    # Database connection logic
    pass
```

---

## ☕ Support My Studies / Buy Me a Coffee

I am an independent developer and student building open-source developer productivity tools. If this retry decorator helped your applications survive transient network glitches, please consider supporting my studies:

- ☕ **Buy Me a Coffee:** [ko-fi.com/me1121118](https://ko-fi.com/)
- ⭐ **Star this repository** on GitHub!

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
