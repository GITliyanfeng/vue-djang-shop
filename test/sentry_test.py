# -*- coding: utf-8 -*-
# __author__ : py_lee
# __time__   : '18-12-21 上午10:38'

from raven import Client
SDN = "http://d598f6fef84147d886e6d5a72b563efb:b140da77594e4c399bb3fa9abe6270d3@127.0.0.1:9000/2"

client = Client(SDN)

try:
    1 / 0
except ZeroDivisionError:
    client.captureException()