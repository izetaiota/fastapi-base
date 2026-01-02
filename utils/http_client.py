import httpx


def client() -> httpx.AsyncClient:
    return httpx.AsyncClient()
