#!/usr/bin/env python3
""" b2s.py -> burp-to-device
A proxy between device and burp
mitmdump -k -p 8082 -m regular -s b2s.py
"""
from json import loads, dumps

from mitmproxy.http import HTTPFlow
from termcolor import colored

from header import Header

URL = 'https://example.com'


def request(flow: HTTPFlow) -> None:
    """ To the request, do:
    1. Load plain_body as json
    2. Encrypt as crypt_body
    3. Pack crypt_body in the expected form (json)

    :param flow: HTTPFlow that includes request as well as response
    :return: None
    """

    if URL in flow.request.pretty_url:
        # 1. Load plain_body as json
        print(colored(f'Modified Request Body: {flow.request.content}', 'cyan'))
        plain_body = loads(flow.request.content)
        # 2. Encrypt as crypt_body
        crypt_body = Header().encrypt(plain_body)
        # 3. Pack crypt_body in the expected form (json)
        flow.request.content = dumps(crypt_body, separators=(',', ':')).encode()
        print(colored(f'b2s.py request -> {flow.request.content}', 'green'))


def response(flow: HTTPFlow) -> None:
    """ To the response, do:
    1. Load crypt_body as json
    2. Decrypt as plain_body
    3. Pack plain_body in the expected form (json)

    :param flow: HTTPFlow that includes request as well as response
    :return: None
    """

    if URL in flow.request.pretty_url:
        # 1. Load crypt_body as json
        print(colored(f'Original Response Body: {flow.response.content}', 'green'))
        crypt_body = loads(flow.response.content)
        # 2. Decrypt as plain_body
        plain_body = Header().decrypt(crypt_body)
        # 3. Pack plain_body in the expected form (json)
        flow.response.content = dumps(plain_body, separators=(',', ':')).encode()
        print(colored(f'b2s.py request -> {flow.response.content}', 'blue'))
