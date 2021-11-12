#!/usr/bin/env python3
# coding:utf-8
import sys
import json
from config import BASE_PROJECT_PATH
import cad_decoder as baseCad

path = f"{BASE_PROJECT_PATH}/hehe"
print(sys.path)
print(path)
print(baseCad.decode_dxf)

output = f"{path}/hehe.json"
data = baseCad.decode_dxf(path)

with open(output, "w") as f:
    f.write(json.dumps(data))
