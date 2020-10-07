#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__      = 'Christophoros Petrou (game0ver)'
__description__ = 'FDsploit.py: File inclusion & directory traversal fuzzer/enumeration & exploitation framework'
__version__     = '1.2'

import os
import sys
import socket
import validators
from core.colors import *
from os.path import isfile, exists
from argparse import ArgumentTypeError, Action


class DictValues(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        my_dict = {}
        for kv in values[0].split(","):
            k,v = kv.split("=", 1)
            my_dict[k] = v
        setattr(namespace, self.dest, my_dict)


def validateFILE(file):
    """validate that the file exists and is readable"""
    if not os.path.isfile(file):
        raise ArgumentTypeError('{}[x] File does not exist{}'.format(FR,S))
    if os.access(file, os.R_OK):
        return file
    else:
        raise ArgumentTypeError('{}[x] File is not readable{}'.format(FR,S))


def validatePort(port):
    if isinstance(int(port), (int, long)):
        if 1 < int(port) < 65536:
            return int(port)
    else:
        raise ArgumentTypeError('{}[x] Port must be in range 1-65535{}'.format(FR,F))


def validateIP(ip):
    try:
        if socket.inet_aton(ip):
            return ip
    except socket.error:
        raise ArgumentTypeError('{}[x] Invalid ip provided{}'.format(FR,S))


def validateURL(url):
    try:
        if validators.url(url):
            return url
        else:
            print('\n{}[x] Invalid url!{}\n'.format(FR,S))
            sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(0)


def validateProxy(proxy):
    if not ':' in proxy or proxy.count(':') != 1:
        raise ArgumentTypeError('\n{}[x] Proxy must be in the form: host:port{}\n'.format(FR,S))
    else:
        host, port = proxy.split(':')
        if validateIP(host) and validatePort(port):
            return proxy
