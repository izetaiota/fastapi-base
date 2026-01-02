from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis

from core.config import settings


def setup_cache(app: FastAPI) -> None:
    redis = Redis.from_url(settings.redis_url, decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
