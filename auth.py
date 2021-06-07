#!/usr/bin/python3

import sys
import struct
import urllib.request as request
import urllib.parse as parse
import urllib.error as error
import os
import logging
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='extauth.log',
                    filemode='a')


API_URL = os.environ["NFS_API_URL"]
API_KEY = os.environ["NFS_API_KEY"]

headers = {
            "Content-Type": "application/json",
            "Authorization": API_KEY
}

def read():
    (pkt_size,) = struct.unpack('>H', sys.stdin.buffer.read(2))
    logging.info('Packet size: ' + str(pkt_size))
    pkt = sys.stdin.read(pkt_size)
    cmd = pkt.split(':')[0]

    global headers
    if cmd == 'auth':
        u, s, p = pkt.split(':', 3)[1:]
        url = API_URL + "/user/authenticate"

        data = json.dumps({
                "username": u,
                "hostname": s,
                "password": p,
            })

        logging.info('Body: ' + str(data))
        data = data.encode("utf-8")
        req = request.Request(url, data, headers, method='POST')
        try:
            with request.urlopen(req) as response:
                write(True)
        except error.HTTPError as e:
            logging.info('Error: ' + str(e.read().decode()))
            write(False)
            return read()
    elif cmd == 'isuser':
        u, s = pkt.split(':', 2)[1:]
        url = API_URL + "/user/" + s+ "/"+ u
        logging.info(url)
        data = ""
        data = data.encode("utf-8")
        req = request.Request(url, data, headers, method='GET')
        try:
            with request.urlopen(req) as response:
                write(True)
        except error.HTTPError as e:
            logging.info('Error: ' + str(e.read().decode()))
            write(False)
            return read()
    elif cmd == 'setpass':
        u, s, p = pkt.split(':', 3)[1:]
        write(True)
    elif cmd == 'tryregister':
        u, s, p = pkt.split(':', 3)[1:]
        url = API_URL + "/user"

        data = json.dumps({
                "username": u,
                "hostname": s,
                "password": p,
             })
        logging.info('Body: ' + str(data))
        data = data.encode("utf-8")
        req = request.Request(url, data, headers, method='POST')
        try:
            with request.urlopen(req) as response:
                write(True)
        except error.HTTPError as e:
            logging.info('Error: ' + str(e.read().decode()))
            write(False)
            return read()
    elif cmd == 'removeuser':
        u, s = pkt.split(':', 2)[1:]
        url = API_URL + "/user/" + s + "/"+ u
        data = ""
        data = data.encode("utf-8")
        req = request.Request(url, data, headers, method='DELETE')
        try:
            with request.urlopen(req) as response:
                write(True)
        except error.HTTPError as e:
            logging.info('Error: ' + str(e.read().decode()))
            write(False)
            return read()
    elif cmd == 'removeuser3':
        u, s, p = pkt.split(':', 3)[1:]
        write(True)
    else:
        write(False)
    read()


def write(result):
    if result:
        sys.stdout.write('\x00\x02\x00\x01')
    else:
        sys.stdout.write('\x00\x02\x00\x00')
    sys.stdout.flush()


# read config
try:
    read()
except struct.error:
    logging.info(struct.error)
    pass
