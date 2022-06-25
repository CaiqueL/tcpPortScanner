#!/usr/bin/env python3

import argparse
import ipaddress
import socket
import os.path


def args_feeder():

    parser = argparse.ArgumentParser(description="simple tcp port scan , will default to port 80 if no ports specified")
    # add positional arguments add_argument
    parser.add_argument(
        'HOST',
        type=ipaddress.IPv4Address,
        help='host IPv4 Address'
    )

    parser.add_argument(
        '-p',
        dest='PORT',
        type=int,
        help='port'
    )

    parser.add_argument(
        '-l',
        dest='PORTLIST',
        type=lambda file: is_valid_file(parser, file),
        help='file input for a list of ports'
    )

    parser.add_argument(
        '-lR',
        dest='PORTRANGE',
        type=str,
        help='port range with split at \'-\' , example : 1-400'
    )

    return parser


def port_range_splitter(args):
    range = args.PORTRANGE
    min_range, max_range = range.split('-')
    return min_range, max_range


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')


def create_client(default_timeout=0.5):

    client_create = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_create.settimeout(default_timeout)
    return client_create


def port_scan(args, client):

    if args.PORT is None and args.PORTLIST is None and args.PORTRANGE is None:
        print('using default port 80')
        code = client.connect_ex((str(args.HOST), 80))
        if code == 0:
            print("[+] port 80 in {} open".format(args.HOST))
        else:
            print("[-] port 80 in {} closed".format(args.HOST))

    if args.PORT is not None:
        code = client.connect_ex((str(args.HOST), args.PORT))
        if code == 0:
            print("[+] port {} in {} open".format(args.PORT, args.HOST))
        else:
            print("[-] port {} in {} closed".format(args.PORT, args.HOST))

    if args.PORTLIST is not None:

        file = is_valid_file(parser,str(args.PORTLIST.name))
        for line in file:
            code = client.connect_ex((str(args.HOST), int(line)))
            if code == 0:
                print("[+] port {} in {} open".format(line, args.HOST))
            else:
                print(code)
                continue


    if args.PORTRANGE is not None:
        min_range, max_range = port_range_splitter(args)
        for port in range(int(min_range),int(max_range)):
            code = client.connect_ex((str(args.HOST), port))
            if code == 0:
                print("[+] port {} in {} open".format(port, args.HOST))




#tcp code 0 == Success
#code = client.connect_ex((args.HOST, args.PORT))

#if code == 0:
#     print("[+} port {} in {} open".format(PORT,HOST))

#else:
#    print("[-] port {} in {} closed".format(PORT,HOST))
#args = parser.parse_args()


if __name__ == "__main__":

    parser = args_feeder()
    args = parser.parse_args()

    client = create_client()

    port_scan(args, client)
