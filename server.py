#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import json
import time


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    OK reply server class
    """
    dicc_register = {}
 
    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        self.wfile.write(b"Hemos recibido tu peticion ")
        self.json2registered()

        info_user= {}

        for line in self.rfile:
            if line.decode('utf-8') != "\r\n":
                print("El cliente nos manda ", line.decode('utf-8'))
                text_rec = line.decode('utf-8').split(" ")
                expires_value = int(text_rec[4])
                if text_rec[0] == "REGISTER":
                    user = text_rec[1]
                    self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                    info_user["address"] = self.client_address[0]
                   # info_user["expires_value"] = expires_value
                    self.dicc_register[user] = info_user
                if text_rec[3] == "Expires:":
                    if expires_value == 0 and user in self.dicc_register:
                        del self.dicc_register[user]
                        print("Borrado usuario " + user)
                        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                    else:
                        expires_date = time.strftime('%Y-%m-%d %H:%M:%S',
                                      time.gmtime(time.time() + expires_value))
                        info_user["expires_value"] = expires_date
        self.registered2json()

    def registered2json(self):

        file = open("registered.json", 'w') 
        json.dump(self.dicc_register, file)

    def json2registered(self):

        try:
            file = open('registered.json')
            data = json.load(file)
            self.dicc_register = data
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    Port = int(sys.argv[1])
    # Listens at localhost ('') port 6001 
    # and calls the EchoHandler class to manage the request
    serv = socketserver.UDPServer(('', Port), SIPRegisterHandler)

    print("Lanzando servidor UDP de registro...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
