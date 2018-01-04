#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Easy PS4 Exploit Hosting by Al-Azif
   Source: https://github.com/Al-Azif/ps4-exploit-host
"""

from __future__ import print_function

try:
    import argparse
    import hashlib
    from http.server import BaseHTTPRequestHandler
    from http.server import HTTPServer
    import mimetypes
    import os
    import re
    import socket
    from socketserver import ThreadingMixIn
    import sys
    import threading
    import time

    import FakeDns.fakedns as fakedns
    from makeftp import make_ftp
except ImportError:
    if sys.version_info.major < 3:
        print('ERROR: This must be run on Python 3')
        try:
            input('Press [ENTER] to exit')
        finally:
            sys.exit()
    else:
        print('ERROR: Import Error')
        print('Download from the releases page or clone with `--recursive`')
        try:
            input('Press [ENTER] to exit')
        finally:
            sys.exit()

SCRIPT_LOC = os.path.realpath(__file__)
CWD = os.path.dirname(SCRIPT_LOC)
EXPLOIT_LOC = os.path.join(CWD, 'exploit')
PAYLOAD_LOC = os.path.join(CWD, 'payloads')
DEBUG = False
AUTOSEND = None


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


class MyHandler(BaseHTTPRequestHandler):
    error_message_format = ''

    def send_response(self, code, message=None):
        """Blanks out default headers"""
        self.log_request(code)
        self.send_response_only(code, message)

    def my_sender(self, mime, content):
        """Here to prevent code duplication"""
        try:
            self.send_response(200)
            self.send_header('Content-type', mime)
            self.end_headers()
            self.wfile.write(content)
        except socket.error:
            print('ERROR: Broken Pipe (Out of Memory?)')

    def updatelist(self):
        region = self.path.split('/')[4]
        path = os.path.join(CWD, 'updates', 'ps4-updatelist.xml')
        with open(path, 'rb') as buf:
            xml = buf.read()
        xml = xml.replace(b'{{REGION}}', bytes(region, 'utf-8'))
        self.my_sender('application/xml', xml)

    def updatefeature(self):
        path = os.path.join(CWD, 'updates', 'ps4-updatefeature.html')
        with open(path, 'rb') as buf:
            self.my_sender('text/html', buf.read())

    def update_pup(self):
        if 'sys' in self.path:
            check_update_pup('SYSTEM', '203C76C97F7BE5B881DD0C77C8EDF385')
            path = 'PS4UPDATE_SYSTEM.PUP'
        elif 'rec' in self.path:
            check_update_pup('RECOVERY', '741CFE2F0DEC1BB4663571DE78AE31CF')
            path = 'PS4UPDATE_RECOVERY.PUP'
        else:
            path = ''
        path = os.path.join(CWD, 'updates', path)
        with open(path, 'rb') as buf:
            self.my_sender('text/plain', buf.read())

    def network_test(self, size):
        data = b'\0' * size
        self.my_sender('text/plain', data)

    def exploit_matcher(self):
        path = self.path.rsplit('/', 1)[-1]
        if not path or path == '/':
            path = 'index.html'
        mime = mimetypes.guess_type(path)
        if not mime[0]:
            mime[0] = 'application/octet-stream'
        with open(os.path.join(EXPLOIT_LOC, path), 'rb') as buf:
            data = buf.read()
            if path == 'index.html':
                data = self.inject_exploit_html(data)
            self.my_sender(mime[0], data)

    def exploit(self):
        path = self.path.rsplit('/', 1)[-1]
        if not path or path == '/':
            path = 'index.html'
        which = self.path.rsplit('/')[-2]
        mime = mimetypes.guess_type(path)
        if not mime[0]:
            mime[0] = 'application/octet-stream'
        with open(os.path.join(EXPLOIT_LOC, which, path), 'rb') as buf:
            data = buf.read()
            if path == 'index.html':
                data = self.inject_credits(data)
            self.my_sender(mime[0], data)

    def payload_launcher(self):
        payload_menu = True
        for thread in threading.enumerate():
            if thread.name == 'Payload_Brain':
                payload_menu = False

        if payload_menu:
            print('>> Exploit Sent...')
            thread = threading.Thread(name='Payload_Brain',
                                      target=payload_brain,
                                      args=(self.client_address[0],),
                                      daemon=True)
            thread.start()

    def inject_exploit_html(self, html):
        inject = b'<a href="{URL}"><button class="btn btn-main">{EXP}</button></a>'
        data = b''
        try:
            i = 0
            for exploit in os.listdir(EXPLOIT_LOC):
                if exploit != 'index.html':
                    if i >= 3:
                        data += b'<br/>'
                        i = 0
                    url = '/exploits/{}/'.format(exploit)
                    temp = inject.replace(b'{EXP}', bytes(exploit, 'utf-8'))
                    data += temp.replace(b'{URL}', bytes(url, 'utf-8'))
                    i += 1
        except IOError:
            pass

        return html.replace(b'{EXPLOITS}', data)

    def inject_credits(self, html):
        inject = b'<center><h1 id=clck>...</h1>PS4 Exploit Host by ' + \
                 b'<a href="https://twitter.com/_AlAzif">Al Azif</a><br/>'

        return html.replace(b'<center><h1 id=clck>...</h1>', inject)

    def do_GET(self):
        """Determines how to handle HTTP requests"""
        try:
            if re.match('^/update/ps4/list/[a-z]{2}/ps4-updatelist.xml', self.path):
                self.updatelist()
            elif re.match('^/update/ps4/html/[a-z]{2}/[a-z]{2}/ps4-updatefeature.html', self.path):
                self.updatefeature()
            elif re.match('^/update/ps4/image/[0-9]{4}_[0-9]{4}/(sys|rec)_[a-f0-9]{32}/PS4UPDATE.PUP', self.path):
                self.update_pup()
            elif re.match('^/networktest/get_2m', self.path):
                self.network_test(2097152)
            elif re.match('^/networktest/get_6m', self.path):
                self.network_test(6291456)
            elif re.match('^/document/[a-zA-Z\-]{2,5}/ps4/index.html', self.path):
                self.exploit_matcher()
            elif re.match('^/exploits/[a-zA-Z0-9\-\_]*/', self.path):
                self.exploit()
            else:
                self.send_error(404)
        except IOError:
            self.send_error(404)

        if self.path.rsplit('/', 1)[-1] == 'rop.js':
            self.payload_launcher()

    def do_POST(self):
        """Custom POST handler for network test"""
        if re.match('^/networktest/post_128', self.path):
            self.send_response(200)
            self.end_headers()


def check_root():
    """Checks if the user is root.

    Windows returns true because there are no priviledged ports
    """
    try:
        root = bool(os.getuid() == 0)
    except AttributeError:
        root = True

    return root


def get_lan():
    """Gets the computer's LAN IP"""
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        soc.connect(('10.255.255.255', 1))
        lan = str(soc.getsockname()[0])
        soc.close()
    except socket.error:
        soc.close()
        closer('ERROR: Unable to find LAN IP')

    return lan


def generate_dns_rules(lan):
    """Creates domain array for FakeDns"""
    rules = []

    rules.append('A manuals.playstation.net ' + lan)
    rules.append('A (get|post).net.playstation.net ' + lan)
    rules.append('A (d|f|h)[a-z]{2}01.ps4.update.playstation.net ' + lan)
    rules.append('A gs2.ww.prod.dl.playstation.net ' + lan)
    rules.append('A [a-z0-9\.\-]*.akadns.net 0.0.0.0')
    rules.append('A [a-z0-9\.\-]*.akamai.net 0.0.0.0')
    rules.append('A [a-z0-9\.\-]*.akamaiedge.net 0.0.0.0')
    rules.append('A [a-z0-9\.\-]*.cddbp.net 0.0.0.0')
    rules.append('A [a-z0-9\.\-]*.ea.com 0.0.0.0')
    rules.append('A [a-z0-9\.\-]*.edgekey.net 0.0.0.0')
    rules.append('A [a-z0-9\.\-]*.edgesuite.net 0.0.0.0')
    rules.append('A [a-z0-9\.\-]*.llnwd.net 0.0.0.0')
    rules.append('A [a-z0-9\.\-]*.playstation.com 0.0.0.0')
    rules.append('A [a-z0-9\.\-]*.playstation.net 0.0.0.0')
    rules.append('A [a-z0-9\.\-]*.playstation.org 0.0.0.0')
    rules.append('A [a-z0-9\.\-]*.ribob01.net 0.0.0.0')
    rules.append('A [a-z0-9\.\-]*.sbdnpd.com 0.0.0.0')
    rules.append('A [a-z0-9\.\-]*.scea.com 0.0.0.0')
    rules.append('A [a-z0-9\.\-]*.sonyentertainmentnetwork.com 0.0.0.0')

    return rules


def check_update_pup(type, md5):
    try:
        update_name = 'PS4UPDATE_{}.PUP'.format(type)
        with open(os.path.join(CWD, 'updates', update_name), 'rb') as buf:
            check = '>> Checking {}\'s checksum'.format(update_name)
            print(check, end='\r')
            hasher = hashlib.md5()
            data = buf.read()
            hasher.update(data)
            system_hash = hasher.hexdigest().upper()
            if system_hash != md5:
                closer('ERROR: {} is not version 4.05'.format(update_name))
            print('>> {} checksum matches   '.format(update_name))
    except IOError:
        pass


def start_servers(rules):
    """Start DNS and HTTP servers on seperate threads"""
    fakedns.main(rules, DEBUG)
    print('>> DNS server thread is running...')

    try:
        server = ThreadedHTTPServer(('', 80), MyHandler)
        thread = threading.Thread(name='HTTP_Server',
                                  target=server.serve_forever,
                                  args=(),
                                  daemon=True)
        thread.start()
        print('>> HTTP server thread is running...')
    except (socket.error, OSError):
        closer('ERROR: Could not start server, is another program on tcp:80?')


def payload_brain(ipaddr):
    """Decides which payloads to send"""
    payloads = []
    try:
        for files in os.listdir(os.path.join(PAYLOAD_LOC)):
            if not files.endswith('PUT PAYLOADS HERE'):
                payloads.append(files)
    except IOError:
        pass

    if AUTOSEND in payloads:
        with open(os.path.join(PAYLOAD_LOC, AUTOSEND), 'rb') as buf:
            print('>> Sending {}...'.format(AUTOSEND))
            content = buf.read()
        send_payload(ipaddr, 9020, content)

    payloads.insert(0, 'Don\'t send a payload')
    payloads.insert(1, 'Integrated FTP')
    choice = menu('Payload', payloads)
    if choice == 1:
        print('>> Sending integrated FTP...')
        content = make_ftp(ipaddr)
        send_payload(ipaddr, 9020, content)
        print('>> Connect at {}:1337'.format(ipaddr))
        send_another(ipaddr)
    elif choice != 0:
        path = os.path.join(PAYLOAD_LOC, payloads[choice])
        with open(path, 'rb') as buf:
            print('>> Sending {}...'.format(payloads[choice]))
            content = buf.read()
        send_payload(ipaddr, 9020, content)
        send_another(ipaddr)
    else:
        print('>> No payload sent')


def send_another(ipaddr):
    choice = 0
    while choice != 'Y' and choice != 'N':
        choice = input('Send another payload? (Y/n): ')
        try:
            choice = choice.upper()
        except (ValueError, NameError):
            choice = 0
    if choice == 'Y':
        thread = threading.Thread(name='Payload_Brain',
                                  target=payload_brain,
                                  args=(ipaddr,),
                                  daemon=True)
        thread.start()


def send_payload(hostname, port, content):
    """Netcat implementation"""
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    timeout = time.time() + 15
    while True:
        result = soc.connect_ex((hostname, port))
        if result == 0:
            print('>> Connected to PS4')
            timed_out = False
            break
        if time.time() >= timeout:
            print('ERROR: Payload sender timed out')
            timed_out = True
            break
    if not timed_out:
        try:
            soc.sendall(content)
            soc.shutdown(socket.SHUT_WR)
            while True:
                data = soc.recv(1024)
                if not data:
                    break
            print('>> Payload Sent!')
        except socket.error:
            print('ERROR: Broken Pipe')
    soc.close()


def menu(type, input_array):
    """Display a menu

    Type is what ends up in the header of the box
    input array is an array of options
    """
    i = 1
    choice = 0
    print('┌────────────────────────────────────────────────────────┐')
    title = '│  {}'.format(type)
    print(format_menu_item(title))
    print('├────────────────────────────────────────────────────────┤')
    for entry in input_array:
        entry = '│  {}. {}'.format(i, entry)
        print(format_menu_item(entry))
        i += 1
    print('└────────────────────────────────────────────────────────┘')
    while choice < 1 or choice >= i:
        input_prompt = 'Choose a {} to send: '.format(type.lower())
        choice = input(input_prompt)
        try:
            choice = int(choice)
        except (ValueError, NameError):
            choice = 0

    return choice - 1


def format_menu_item(entry):
    """Format a menu item to have the box line up"""
    if len(entry) > 58:
        entry = entry[:56]
    while len(entry) < 56:
        entry += ' '
    entry += ' │'
    return entry


def silence_http(self, format, *args):
    """Just blackhole this method to prevent printing"""
    pass


def getch():
    """MIT Licensed: https://github.com/joeyespo/py-getch"""
    import termios
    import tty

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def closer(message):
    """Closing method"""
    print(message)
    if message != '\r>> Exiting...                                           ':
        print('Press any key to exit...', end='')
        sys.stdout.flush()
        if os.name == 'nt':
            from msvcrt import getch as w_getch
            w_getch()
        else:
            getch()
        print()
    sys.exit()


def menu_header():
    """Very first thing that prints"""
    print('┌────────────────────────────────────────────────────────┐')
    print('│  PS4 Exploit Host                           by Al Azif │')
    print('└────────────────────────────────────────────────────────┘')


def main():
    """The main logic"""
    global DEBUG
    global AUTOSEND
    global EXPLOIT_LOC

    menu_header()

    if not check_root():
        closer('ERROR: This must be run by root as it requires port 53 & 80')

    parser = argparse.ArgumentParser(description='PS4 Exploit Host')
    parser.add_argument('--autosend', dest='autosend', action='store',
                        default='', required=False,
                        help='Automatically send payload when exploit loads')
    parser.add_argument('--debug', action='store_true',
                        required=False, help='Print debug statements')
    args = parser.parse_args()

    try:
        if args.debug:
            DEBUG = True
        else:
            MyHandler.log_message = silence_http

        if args.autosend:
            if os.path.isfile(os.path.join(PAYLOAD_LOC, args.autosend)):
                AUTOSEND = args.autosend
            else:
                closer('ERROR: Autosend payload not found')

        check_update_pup('SYSTEM', '203C76C97F7BE5B881DD0C77C8EDF385')
        check_update_pup('RECOVERY', '741CFE2F0DEC1BB4663571DE78AE31CF')

        lan = get_lan()

        rules = generate_dns_rules(lan)
        start_servers(rules)

        while len(lan) < 15:
            lan += ' '

        dns_ip = 'Your DNS IP is {}'.format(lan)
        num = int((56 - len(dns_ip)) / 2)
        dns_ip = '║' + (' ' * num) + dns_ip + (' ' * num) + '║'
        if len(dns_ip) < 58:
            dns_ip = dns_ip[:-1] + ' ║'
        print('╔════════════════════════════════════════════════════════╗')
        print('║                  Servers are running!                  ║')
        print(dns_ip)
        print('╚════════════════════════════════════════════════════════╝')

        while True:
            pass
    except KeyboardInterrupt:
        closer('\r>> Exiting...                                           ')


if __name__ == '__main__':
    main()
