#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket; socket.setdefaulttimeout(10)

import random, time, threading, sys, json

from urllib import request, parse

from sdk import ApiClient

USE_HTTPS = True

API_HOST = 'bw-test-api.btcdo.org'
API_KEY = 'AAAAAYax9qOFYqfPJ2R27f5Eg629bJt3'
API_SECRET = 'n6qKwe7teNH8udkJShyP'

def main():
    host = API_HOST
    key = API_KEY
    secret = API_SECRET
    https = USE_HTTPS
    for arg in sys.argv:
        if arg.startswith('-host='):
            host = arg[6:]
        if arg.startswith('-key='):
            key = arg[5:]
        if arg.startswith('-secret='):
            secret = arg[8:]
    t = threading.Thread(target=lambda: do_jobs(host, key, secret, https))
    t.start()

def do_jobs(host, key, secret, https):
    client = ApiClient(key, secret, host, https)
    try:
        r = client.post('/v1/trade/orders', {
        'orderType': 'BUY_LIMIT',
        'symbol': 'BDB_BTC',
        'amount': 108,
        'price': 0.00000678,
        'features': 65536
        })
        print('place %s ok? %s' % ('~~~ create orders response ~~~', success(r)))
    except Exception as e:
        print(e)

def success(result):
    return not hasattr(result, 'error')

if __name__ == '__main__':
    main()
