#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import socket
import sys

# Constantes. Dirección IP del servidor y contenido a enviar
SERVER = sys.argv[1]
PORT = int(sys.argv[2])
MType = sys.argv[3]
User = sys.argv[4]
expires_value = sys.argv[5]
LINE = ""

if MType == 'register':
    LINE = ('REGISTER sip:' + User + ' SIP/2.0 ')
    LINE += ('Expires: ' + expires_value + '\r\n\r\n')

#for words in sys.argv[5:]:
 #   LINE = LINE + " " + words

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
        my_socket.connect((SERVER, PORT))
        print("Enviando:", LINE)
        my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
        data = my_socket.recv(1024)
        print('Recibido -- ', data.decode('utf-8'))
else:
    sys.exit('Usage: client.py ip puerto register sip_address expires_value')

print("Socket terminado.")
