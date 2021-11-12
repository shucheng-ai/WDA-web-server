#!/usr/bin/env python3
# coding:utf-8
import os

from libs.utils import mkdir, cleandir

import cad_decoder as baseCad


class LayoutCad(object):
    title = "layout cad"

    @staticmethod
    def decode_cad(path):
        data = baseCad.decode_dxf(path)
        return data
