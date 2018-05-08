#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json, time, hmac, uuid, urllib, base64, hashlib

from urllib import request, parse, error

class ApiClient(object):

    def __init__(self, api_key, api_secret, host=None, https=True):
        self._api_key = api_key
        self._api_secret = api_secret.encode('utf-8')
        self._host = (host or 'bit.itranswarp.com').lower()
        self._protocol = 'https' if https else 'http'

    def _hostname(self):
        n = self._host.find(':')
        if n > 0:
            return self._host[:n]
        return self._host

    def get(self, path, **params):
        return self._http('GET', path, params, None)

    def post(self, path, obj=None):
        data = json.dumps(obj) if obj is not None else None
        return self._http('POST', path, {}, data)

    def _http(self, method, path, params, data):
        # build payload:
        param_list = ['%s=%s' % (k, v) for k, v in params.items()]
        param_list.sort()
        payload = [method, self._hostname(), path, '&'.join(param_list)]
        headers = {
            'API-Key': self._api_key,
            'API-Signature-Method': 'HmacSHA256',
            'API-Signature-Version': '1',
            'API-Timestamp': str(int(time.time() * 1000))
        }
        if method == 'POST' and path.startswith('/v1/trade/'):
            headers['API-Unique-ID'] = uuid.uuid4().hex
        headers_list = ['%s: %s' % (k.upper(), v) for k, v in headers.items()]
        headers_list.sort()
        payload.extend(headers_list)
        payload.append(data if data else '')
        payload_str = '\n'.join(payload)
        # signature:
        sign = hmac.new(self._api_secret, payload_str.encode('utf-8'), hashlib.sha256).hexdigest()
        debug('payload:\n----\n' + payload_str + '----\nsignature: ' + sign)
        headers['API-Signature'] = sign
        # build request:
        if data:
            data = data.encode('utf-8')
        else:
            data = None
        url = '%s://%s%s?%s' % (self._protocol, self._host, path, parse.urlencode(params))
        debug('%s: %s' % (method, url))
        req = request.Request(url, data=data, method=method)
        for k, v in headers.items():
            req.add_header(k, v)
        if data:
            req.add_header('Content-Type', 'application/json')
        try:
            with request.urlopen(req) as f:
                r = json.load(f, object_hook=lambda d: Dict(**d))
                debug(json.dumps(r))
                return r
        except error.HTTPError as err:
            s = err.read()
            debug(s)
            return json.load(s, object_hook=lambda d: Dict(**d))

_debug = True

def debug(msg):
    if _debug:
        print(msg)

class ApiError(Exception):
    pass

class Dict(dict):

    def __init__(self, **kw):
        super().__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value
