#!/usr/local/bin/python3

import argparse
import socket
import sys

from master import Master
from slave import Slave

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

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
        print(f'starting master on {get_ip()}:{args.port}')
        master = Master(args.port)
        master.set_size(864, 540)
        addr, port = input('slave port? ').split(':')
        master.set_slave((addr, int(port)))
        master.run()

    if args.slave:
        print(f'starting slave on {get_ip()}:{args.port}')
        slave = Slave(args.port)
        addr, port = input('master port? ').split(':')
        slave.set_master((addr, int(port)))
        slave.run()

