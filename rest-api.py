#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket; socket.setdefaulttimeout(10)

import random, time, threading, sys, json

from urllib import request, parse

from sdk import ApiClient

USE_HTTPS = True

#endpoint无需写https
API_HOST = 'api.btcdo.com'
#登录Btcdo账户，在“个人中心”→“安全中心”获取API-KEY和API-SECRET
API_KEY = '您的APIKEY'
API_SECRET = '您的APISECRET'


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
    #t = threading.Thread(target=lambda: do_query(host, key, secret, https))
    #t.start()
    createOrder(host, key, secret, https)
    queryOrder(host, key, secret, https)
    queryCurrency(host, key, secret, https)

#需要签名的post请求 创建订单
def createOrder(host, key, secret, https):
    client = ApiClient(key, secret, host, https)
    try:
        r = client.post('/v1/trade/orders', {
        'orderType': 'SELL_LIMIT',
        'symbol': 'BDB_ETH',
        'amount': 100,
        'price': 1.00000678,
        'features': 65536
        })
        print('place %s ok? %s' % ('~~~ create orders response ~~~', success(r)))
    except Exception as e:
        print(e)
        
#需要签名的get请求 获取最近交易记录
def queryOrder(host, key, secret, https):
    client = ApiClient(key, secret, host, https)
    try:
        r = client.get('/v1/trade/orders')
        print('place %s ok? %s' % ('~~~ get orders response ~~~', success(r)))
    except Exception as e:
        print(e)

#无需签名的get请求 获取所有币种信息
def queryCurrency(host, key, secret, https):
    client = ApiClient(key, secret, host, https)
    try:
        r = client.get('/v1/common/currencies')
        print('place %s ok? %s' % ('~~~ get currency response ~~~', success(r)))
    except Exception as e:
        print(e)


def success(result):
    return not hasattr(result, 'error')

if __name__ == '__main__':
    main()
