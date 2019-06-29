#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__      = 'Christophoros Petrou (game0ver)'
__description__ = 'FDsploit.py: File inclusion & directory traversal fuzzer/enumeration & exploitation framework'
__version__     = '1.2'

from core.utils import *
from core.colors import *
from core.validations import *
from argparse import ArgumentParser, RawTextHelpFormatter, SUPPRESS

USER_AGENT = 'FDsploit_{}_agent'.format(__version__)

def console():
    """argument parser"""
    parser = ArgumentParser(description="{}FDsploit.py:{} Automatic (L|R)FI & directory traversal enumeration & exploitation.".format(BT+FG, S),
                            formatter_class=RawTextHelpFormatter, 
                            epilog='{0}[!]{1} For More Details please read the {0}README.md{1} file!'.format(FG, S), 
                            add_help=False)

    # MUTUALLY EXCLUSIVE REQUIRED PARAMETERS...
    required = parser.add_mutually_exclusive_group()
    parser._optionals.title = '{}Required (one of the following){}'.format(BT, S)

    required.add_argument('-u', "--url", 
                        type=validateURL, 
                        help='Specify a url or', 
                        metavar='')

    required.add_argument('-f', "--file",
                        type=validateFILE, 
                        help='Specify a file containing urls', 
                        metavar='')

    # OPTIONAL PARAMETERS...
    optional = parser.add_argument_group('{}Optional{}'.format(BT, S))

    optional.add_argument('-h', '--help', 
                        action='help', 
                        default=SUPPRESS, 
                        help='Show this help message and exit')

    optional.add_argument('-p', "--payload", 
                        default='', 
                        help="Specify a payload-file to look for [{0}default {2}{1}None{2}]".format(BT, FC, S), 
                        metavar='',
                        required=False)

    optional.add_argument('-d', "--depth", 
                        type=int, 
                        help='Specify max depth for payload [{0}default {2}{1}5{2}]'.format(BT, FC, S), 
                        default=5, 
                        metavar='',
                        required=False)

    optional.add_argument('-e', "--urlencode", 
                        default=0, 
                        choices=['0', '1', '2'],
                        help="Url-encode the payload [{0}default: {2}{1}False{2}]".format(BT, FC, S),
                        required=False)

    optional.add_argument('-t', "--tchar", 
                        choices=['%00','?'], 
                        help="Use a termination character ('%%00' or '?') [{0}default {2}{1}None{2}]".format(BT, FC, S), 
                        metavar='',
                        required=False)

    optional.add_argument('-b', "--b64", 
                        help="Use base64 encoding [{0}default {2}{1}False{2}]".format(BT, FC, S), 
                        action='store_true',
                        required=False)

    optional.add_argument('-x', "--proxy", 
                        type=validateProxy, 
                        default=None, 
                        help="Specify a proxy to use [{0}form: {2}{1}host:port{2}]".format(BT, FC, S), 
                        metavar='',
                        required=False)

    optional.add_argument('-c', "--cookie", 
                        default=None, 
                        help="Specify a session-cookie to use [{0}default {2}{1}None{2}]".format(BT, FC, S), 
                        metavar='',
                        required=False)

    optional.add_argument('-v', "--verb", 
                        choices=['GET','POST'], 
                        help="Specify request type ('GET' or 'POST') [{0}default {2}{1}GET{2}]".format(BT, FC, S), 
                        default='GET', 
                        metavar='',
                        required=False)

    optional.add_argument("--params",  
                        help="Specify POST parameters to use ({0}applied only with POST requests{2}) \n{1}Form:{2} {0}param1:value1,param2:value2,...{2}".format(IT, FC, S), 
                        action=DictValues, 
                        nargs="+", 
                        metavar='',
                        required=False)

    optional.add_argument('-k', "--keyword", 
                        type=str, 
                        default=None,
                        help="Search for a certain keyword(s) on the response [{0}default: {2}{1}None{2}]".format(BT, FC, S), 
                        metavar='',
                        required=False)

    optional.add_argument('-a', "--useragent", 
                        help="Use a random user-agent [{0}default user-agent: {2}{1}{3}{2}]".format(BT, FC ,S, USER_AGENT), 
                        action='store_true')

    optional.add_argument("--cmd", 
                        default=None,
                        help="Test for command execution through PHP functions [{0}default command: {2}{1}None{2}]".format(BT, FC, S), 
                        metavar='',
                        required=False)

    optional.add_argument("--lfishell", 
                        default=None,
                        choices=[None, 'simple', 'expect', 'input'],
                        help="LFI pseudoshell [{0}default {2}{1}None{2}]".format(BT, FC, S), 
                        required=False)

    args = parser.parse_args()
    return args
