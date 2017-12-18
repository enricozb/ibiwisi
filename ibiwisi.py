#!/usr/local/bin/python3

import argparse
import capture
import mouse
import window

import os
import time
import sys

from master import Master
from slave import Slave

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--master", action="store_true")
    parser.add_argument("--slave", action="store_true")
    parser.add_argument("port", type=int)
    return parser.parse_args(args)

if __name__ == '__main__':
    args = parse_args(sys.argv[1:])

    if not (args.master or args.slave):
        print('wrong args')

    if args.master:
        print(f'starting master on port {args.port}')
        master = Master(args.port)
        master.set_size(864, 540)
        master.set_slave(('localhost', int(input('slave port? '))))
        master.run()

    if args.slave:
        print(f'starting slave on port {args.port}')
        slave = Slave(args.port)
        slave.set_master(('localhost', int(input('master port? '))))
        slave.run()

