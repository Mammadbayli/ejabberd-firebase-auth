#!/usr/bin/python3

import sys
import struct
import urllib.request as request
import urllib.parse as parse
import urllib.error as error
import os
import logging
import json

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='extauth.log',
                    filemode='a')

API_KEY = os.environ["FIREBASE_API_KEY"]

def read():
    logging.info('Ready to read')
    (pkt_size,) = struct.unpack('>H', sys.stdin.buffer.read(2))
    logging.info('Packet size: ' + str(pkt_size))
    pkt = sys.stdin.read(pkt_size)
    cmd = pkt.split(':')[0]

    if cmd == 'auth':
        u, s, p = pkt.split(':', 3)[1:]
        url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=" + API_KEY
        headers = {
            "Content-Type": "application/json"
            }
        data = json.dumps({
                "email": u + "@" + s,
                "password": p,
             })
        logging.info('Body: ' + str(data))
        data = data.encode("utf-8")
        req = request.Request(url, data, headers, method='POST')
        try:
            with request.urlopen(req) as response:
                try:
                    resp = json.loads(response.read())
                    logging.info('Response: ' + str(resp))
                    write(True)
                    return read()
                except ValueError:
                    write(False)
                    return read()
        except error.HTTPError as e:
            logging.info('Error: ' + str(e.read().decode()))
            write(False)
            return read()
    elif cmd == 'isuser':
        u, s = pkt.split(':', 2)[1:]
        url = "https://identitytoolkit.googleapis.com/v1/accounts:createAuthUri?key=" + API_KEY
        headers = {
            "Content-Type": "application/json"
            }
        data = json.dumps({
                "identifier": u + "@" + s,
                "continueUri": "http://localhost:8080/app",
             })
        logging.info('Body: ' + str(data))
        data = data.encode("utf-8")
        req = request.Request(url, data, headers, method='POST')
        try:
            with request.urlopen(req) as response:
                try:
                    resp = json.loads(response.read())
                    logging.info('Response: ' + str(resp))
                    write(resp["registered"])
                    return read()
                except ValueError:
                    write(False)
                    return read()
        except error.HTTPError as e:
            logging.info('Error: ' + str(e.read().decode()))
            write(False)
            return read()
    elif cmd == 'setpass':
        u, s, p = pkt.split(':', 3)[1:]
        write(True)
    elif cmd == 'tryregister':
        u, s, p = pkt.split(':', 3)[1:]
        url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=" + API_KEY
        headers = {
            "Content-Type": "application/json"
            }
        data = json.dumps({
                "email": u + "@" + s,
                "password": p,
             })
        logging.info('Body: ' + str(data))
        data = data.encode("utf-8")
        req = request.Request(url, data, headers, method='POST')
        try:
            with request.urlopen(req) as response:
                try:
                    resp = json.loads(response.read())
                    logging.info('Response: ' + str(resp))
                    write(True)
                    return read()
                except ValueError:
                    write(False)
                    return read()
        except error.HTTPError as e:
            logging.info('Error: ' + str(e.read().decode()))
            write(False)
            return read()
    elif cmd == 'removeuser':
        u, s = pkt.split(':', 2)[1:]
        write(True)
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
    logging.info('Start read')
    read()
except struct.error:
    logging.info(struct.error)
    pass
