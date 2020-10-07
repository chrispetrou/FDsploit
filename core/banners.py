#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__      = 'Christophoros Petrou (game0ver)'
__description__ = 'FDsploit.py: File inclusion & directory traversal fuzzer/enumeration & exploitation framework'
__version__     = '1.2'

from core.utils import *
from core.colors import *
from random import randint


def banner1():
    print(BT+"""
    ███████╗██████╗ ███████╗██████╗ ██╗      ██████╗ ██╗████████╗
    ██╔════╝██╔══██╗██╔════╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
    █████╗  ██║  ██║███████╗██████╔╝██║     ██║   ██║██║   ██║
    ██╔══╝  ██║  ██║╚════██║██╔═══╝ ██║     ██║   ██║██║   ██║
    ██║     ██████╔╝███████║██║     ███████╗╚██████╔╝██║   ██║...ver. {}\n\nAuthor: Christoforos Petrou (game0ver) !""".format(FR+__version__+S))


def banner2():
    print(BT+"""
    ▒█▀▀▀ ▒█▀▀▄ █▀▀ █▀▀█ █░░ █▀▀█ ░▀░ ▀▀█▀▀
    ▒█▀▀▀ ▒█░▒█ ▀▀█ █░░█ █░░ █░░█ ▀█▀ ░░█░░
    ▒█░░░ ▒█▄▄▀ ▀▀▀ █▀▀▀ ▀▀▀ ▀▀▀▀ ▀▀▀ ░░▀░░...ver. {0}
                                              {1}Author:{2} Christoforos Petrou (game0ver) !\n""".format(FR+__version__+S, BT, S))


def banner3():
    print(BT+"""
    ╔═══╦═══╗     ╔╗    ╔╗
    ║╔══╩╗╔╗║     ║║   ╔╝╚╗
    ║╚══╗║║║╠══╦══╣║╔══╬╗╔╝
    ║╔══╝║║║║══╣╔╗║║║╔╗╠╣║
    ║║  ╔╝╚╝╠══║╚╝║╚╣╚╝║║╚╗
    ╚╝  ╚═══╩══╣╔═╩═╩══╩╩═╝
               ║║
               ╚╝...ver. {0}
                    {1}Author:{2} Christoforos Petrou (game0ver) !\n""".format(FR+__version__+S, BT, S))


def banner4():
    print(BT+"""
     _______ _____               __         __ __
    |    ___|     \.-----.-----.|  |.-----.|__|  |_
    |    ___|  --  |__ --|  _  ||  ||  _  ||  |   _|
    |___|   |_____/|_____|   __||__||_____||__|____|
                         |__|...ver. {0}
                                {1}Author:{2} Christoforos Petrou (game0ver) !\n""".format(FR+__version__+S, BT, S))


def banner5():
    print(BT+"""
     _____ ____          _     _ _
    |   __|    \ ___ ___| |___|_| |_
    |   __|  |  |_ -| . | | . | |  _|
    |__|  |____/|___|  _|_|___|_|_|
                    |_|...ver. {0}
                          {1}Author:{2} Christoforos Petrou (game0ver) !\n""".format(FR+__version__+S, BT, S))


def banner6():
    print(BT+"""
        __________             __      _ __
       / ____/ __ \_________  / /___  (_) /_
      / /_  / / / / ___/ __ \/ / __ \/ / __/
     / __/ / /_/ (__  ) /_/ / / /_/ / / /_
    /_/   /_____/____/ .___/_/\____/_/\__/
                    /_/...ver. {0}
                          {1}Author:{2} Christoforos Petrou (game0ver) !\n""".format(FR+__version__+S, BT, S))


def banner7():
    print(BT+"""
     _____ ____            _       _ _
    |  ___|  _ \ ___ _ __ | | ___ (_) |_
    | |_  | | | / __| '_ \| |/ _ \| | __|
    |  _| | |_| \__ \ |_) | | (_) | | |_
    |_|   |____/|___/ .__/|_|\___/|_|\__|
                    |_|...ver. {0}
                          {1}Author:{2} Christoforos Petrou (game0ver) !\n""".format(FR+__version__+S, BT, S))


baner = {
    1: banner1,
    2: banner2,
    3: banner3,
    4: banner4,
    5: banner5,
    6: banner6,
    7: banner7
}


def banner():
    clear_screen()
    baner[randint(1,7)]()
