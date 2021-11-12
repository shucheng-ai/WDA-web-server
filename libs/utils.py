#!/usr/bin/env python3
# coding:utf-8
import os
import json
import time
import random
from hashlib import md5
from shutil import rmtree, copytree, copy2


def is_file_exist(path):
    if not os.path.exists(path):
        return False
    else:
        return True


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def cleandir(path):
    if os.path.exists(path):
        rmtree(path)


def copy_dir(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            copy2(s, d)


def make_session_id(sstr=None):
    ti = int(time.time())
    if not sstr:
        string = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        random.shuffle(string)
        sstr = ''.join(string)
    rand = str(random.randint(0, 99999))
    res = str(ti) + sstr + rand
    res = res.encode("utf-8")
    res = md5(res).hexdigest()
    return res


def generate_md5(data):
    data = f"{data}"
    data = data.encode("utf-8")
    data = md5(data).hexdigest()
    return data


def save_json(path, data):
    with open(path, "w") as f:
        f.write(json.dumps(data))


def get_json(path, default={}):
    try:
        with open(path, "r") as f:
            return json.loads(f.read())
    except:
        return default


def dic_to_list(data):
    res = []
    if type(data) == dict:
        for k, v in data.items():
            if type(v) == dict:
                v['id'] = k
                res.append(v)
            else:
                res.append({
                    "id": k,
                    "value": v
                })
    return res
