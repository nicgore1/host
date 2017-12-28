#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Easy PS4 Exploit Hosting by Al-Azif
   Source: https://github.com/Al-Azif/ps4-exploit-host
"""

from __future__ import print_function

import argparse
import os
import re
import SimpleHTTPServer
import socket
import SocketServer
import struct
import subprocess
import sys
import threading
import time

SCRIPT_LOC = os.path.realpath(__file__)
CWD = os.path.dirname(SCRIPT_LOC)
FAKE_LOC = os.path.join(CWD, 'FakeDns', 'fakedns.py')
DNS_LOC = os.path.join(CWD, 'dns.conf')
EXPLOIT_LOC = os.path.join(CWD, 'exploit', '')
FILETYPES = {
    '.css': 'text/css',
    '.eot': 'application/vnd.ms-fontobject',
    '.gif': 'image/gif',
    '.html': 'text/html',
    '.ico': 'image/x-icon',
    '.jpg': 'image/jpeg',
    '.js': 'application/javascript',
    '.otf': 'application/x-font-opentype',
    '.png': 'image/png',
    '.sfnt': 'application/font-sfnt',
    '.svg': 'image/svg+xml',
    '.ttf': 'application/x-font-truetype',
    '.woff': 'application/font-woff',
    '.woff2': 'application/font-woff2'
}


class MyTCPServer(SocketServer.TCPServer):
    """TCPServer to allow instant reuse of port 80"""
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)


class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """Handler for HTTP Requests (This is so it works for all languages)

       *ALL* requests will be directed to like named files in EXPLOIT_LOC
    """
    def do_GET(self):
        """Modify default do_GET method"""
        client = self.client_address[0]
        if client == '127.0.0.1' or checklan(client, getnetwork(getlan())):
            try:
                path = self.path.rsplit('/', 1)[-1]
                if self.path.endswith('ps4-updatelist.xml'):
                    region = self.path.split('/')[4]
                    with open(os.path.join(CWD, 'updates', 'ps4-updatelist.xml'), 'rb') as f:
                        xml = f.read()
                        xml = xml.replace('{{REGION}}', region)
                        self.send_response(200)
                        self.send_header('Content-type', 'application/xml')
                        self.end_headers()
                        self.wfile.write(xml)
                elif self.path.endswith('ps4-updatefeature.html'):
                    with open(os.path.join(CWD, 'updates', path), 'rb') as f:
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(f.read())
                elif self.path.endswith('.PUP'):
                    with open(os.path.join(CWD, 'updates', path), 'rb') as f:
                        self.send_response(200)
                        self.send_header('Content-type', 'text/plain')
                        self.end_headers()
                        self.wfile.write(f.read())
                elif re.match('/document/[a-z]{2}/ps4/', self.path):
                    if not path:
                        path = 'index.html'
                    ext = '.' + path.rsplit('.', 1)[-1]
                    with open(os.path.join(EXPLOIT_LOC, path), 'rb') as f:
                        self.send_response(200)
                        self.send_header('Content-type', FILETYPES[ext])
                        self.end_headers()
                        self.wfile.write(f.read())
            except (IOError, KeyError):
                self.send_error(404)

            if path == 'rop.js':
                print('>> Sending exploit...')
                payloads = []
                for files in os.listdir(os.path.join(CWD, 'payloads')):
                    if files.endswith('.bin'):
                        payloads.append(files)
                if not payloads:
                    print('>> No payloads found')
                for payload in payloads:
                    with open(os.path.join(CWD, 'payloads', payload), 'rb') as f:
                        content = f.read()
                    thread = threading.Thread(target=netcat, args=(client, 9020, content))
                    thread.daemon = True
                    thread.start()
        else:
            self.send_error(403)

    def do_HEAD(self):
        """The update process requests this and fails without it"""
        self.send_response(200)
        self.send_header('Content-Length', '0')
        self.end_headers()


def checkroot():
    """Checks if the user is root

       Returns True on Windows by default
       Returns: Boolean
    """
    try:
        root = os.getuid() == 0
    except AttributeError:
        root = True

    return root


def getlan():
    """Gets the computer's LAN IP

       Returns: String
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        lan = str(s.getsockname()[0])
        s.close()
    except socket.error:
        s.close()
        sys.exit('>> Unable to find LAN IP')

    return lan


def getnetwork(ipaddr):
    """Guesses the private network based on the IP address

       Returns the default IPv4 route if it isn't a private network
       Returns: String
    """
    ipaddr = ipaddr.split('.')

    if ipaddr[0] == '10':
        network = '10.0.0.0/8'
    elif ipaddr[0] == '172' and 16 <= int(ipaddr[1]) <= 31:
        network = '172.16.0.0/12'
    elif ipaddr[0] == '192' and ipaddr[1] == '168':
        network = '192.168.0.0/16'
    else:
        print('WARNING: Could not figure out private network' + os.linesep +
              'WARNING: LAN blocking will NOT work')
        network = '0.0.0.0/0'

    return network


def checklan(ipaddr, network):
    """Checks to see if the IP address is contained within the network

       Returns: Boolean
    """
    ipaddr = socket.inet_aton(ipaddr)
    netaddr = network.split('/')[0]
    netmask = network.split('/')[1]
    netaddr = socket.inet_aton(netaddr)

    ipint = struct.unpack('!I', ipaddr)[0]
    netint = struct.unpack('!I', netaddr)[0]
    maskint = (0xffffffff << (32 - int(netmask))) & 0xffffffff

    return ipint & maskint == netint


def writeconf(lan):
    """Writes the configuration file for FakeDns

        Input:   IPv4 Address as String
        Returns: Boolean
    """
    exists = os.path.isfile(DNS_LOC)

    try:
        with open(DNS_LOC, 'w+') as f:
            f.write('A manuals.playstation.net ' + lan + '\n')
            f.write('A update.playstation.net ' + lan + '\n')
            f.write('A f[a-z]{2}01.ps4.update.playstation.net ' + lan + '\n')
            f.write('A h[a-z]{2}01.ps4.update.playstation.net ' + lan + '\n')
            f.write('A [a-z0-9\.\-]*.cddbp.net 0.0.0.0\n')
            f.write('A [a-z0-9\.\-]*.ea.com 0.0.0.0\n')
            f.write('A [a-z0-9\.\-]*.llnwd.net 0.0.0.0\n')
            f.write('A [a-z0-9\.\-]*.playstation.com 0.0.0.0\n')
            f.write('A [a-z0-9\.\-]*.playstation.net 0.0.0.0\n')
            f.write('A [a-z0-9\.\-]*.playstation.org 0.0.0.0\n')
            f.write('A [a-z0-9\.\-]*.ribob01.net 0.0.0.0\n')
            f.write('A [a-z0-9\.\-]*.sbdnpd.com 0.0.0.0\n')
            f.write('A [a-z0-9\.\-]*.scea.com 0.0.0.0\n')
            f.write('A [a-z0-9\.\-]*.sonyentertainmentnetwork.com 0.0.0.0\n')
        if not exists:
            fixpermissions()
        return True
    except IOError:
        return False


def fixpermissions():
    """Make FakeDNS config file the same permissions as start.py

       This should only be run if the config didn't exist before
       It will not include execution privileges
    """
    try:
        stats = os.stat(SCRIPT_LOC)

        os.chown(DNS_LOC, stats.st_uid, stats.st_gid)

        mask = oct(stats.st_mode & 0o777)
        newmask = ''

        for i in mask:
            if i != 'o':
                if int(i) % 2 != 0:
                    i = str(int(i) - 1)
            newmask += i

        mask = int(newmask, 8)
        os.chmod(DNS_LOC, mask)
    except AttributeError:
        pass
    except OSError:
        print('>> Unable to change permissions of ' + DNS_LOC + os.linesep +
              '   ^^ This is a non-fatal error ^^')


def silence_http(self, format, *args):
    """Just blackhole this method to prevent printing"""
    return


def toggle_dns_display():
    """Enable/Disable FakeDns's "Matched Request" dialogue"""
    try:
        with open(FAKE_LOC, 'r+') as f:
            data = f.read()
            if DEBUG:
                if '# print ">> Matched Request - " + query.domain' in data:
                    data = data.replace('# print ">> Matched Request - " + query.domain', 'print ">> Matched Request - " + query.domain')
            if not DEBUG:
                if '# print ">> Matched Request - " + query.domain' not in data:
                    data = data.replace('print ">> Matched Request - " + query.domain', '# print ">> Matched Request - " + query.domain')
            f.seek(0)
            f.write(data)
            f.truncate()
    except IOError:
        print('>> Unable to silence FakeDNS ' + os.linesep +
              '   ^^ This is a non-fatal error ^^')


def startservers():
    """Start the DNS and HTTP Server"""
    try:
        dns = subprocess.Popen(['python', FAKE_LOC, '-c', DNS_LOC])
    except IOError:
        sys.exit('>> Unable to locate FakeDns')

    try:
        httpd = MyTCPServer(('', 80), MyHandler)
    except socket.error:
        dns.kill()
        sys.exit('>> Port 80 already in use')
    try:
        print('>> Starting HTTP server...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()
        httpd.server_close()
        dns.kill()
        sys.exit()


def netcat(hostname, port, content):
    """Python netcat implementation"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    timeout = time.time() + 60
    while True:
        result = s.connect_ex((hostname, port))
        if result == 0:
            print('>> Connected to PS4')
            timed_out = False
            break
        if time.time() >= timeout:
            print('>> Netcat service timed out')
            timed_out = True
            break
    if not timed_out:
        s.sendall(content)
        s.shutdown(socket.SHUT_WR)
        while 1:
            data = s.recv(1024)
            if not data:
                break
        print('>> Payload Sent!')
    s.close()


def main():
    """The main logic"""
    global DEBUG

    if not checkroot():
        sys.exit('>> This must be run by root as it requires port 53 & 80')

    parser = argparse.ArgumentParser(description='PS4 Exploit Host')
    parser.add_argument('--debug', action='store_true',
                        required=False, help='Print debug statements')
    args = parser.parse_args()

    lan = getlan()

    if writeconf(lan):
        print('>> Your DNS IP is ' + lan)
    else:
        sys.exit('>> Unable to write ' + DNS_LOC)

    if not args.debug:
        DEBUG = False
        MyHandler.log_message = silence_http
    else:
        DEBUG = True

    toggle_dns_display()

    startservers()


if __name__ == '__main__':
    main()
