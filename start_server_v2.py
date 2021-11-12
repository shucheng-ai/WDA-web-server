#!/usr/bin/env python3
# coding:utf-8
import sys
from app.app import app
from config import DEBUG, HOST, PORT

print(sys.path)
print(f"app run debug:{DEBUG};host:{HOST},{PORT};debug:{DEBUG}")

app.run(
    debug=DEBUG,
    host=HOST,
    port=PORT
)
