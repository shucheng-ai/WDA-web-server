#!/usr/bin/env python3
# coding:utf-8
import redis
from config import CONFIG

rdb = redis.Redis(
    host=CONFIG.ENV_REDIS_HOST,
    port=CONFIG.ENV_REDIS_PORT,
    db=CONFIG.ENV_REDIS_DB,
)
