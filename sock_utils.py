#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - sock_utils.py
Grupo: 54
Números de aluno: 55852 e 56909
"""
import socket as s
def create_tcp_server_socket(address, port, queue_size):

    sock = s.socket(s.AF_INET, s.SOCK_STREAM)

    sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)

    sock.bind((address,port))

    sock.listen(queue_size)

    return sock

def create_tcp_client_socket(address, port):

    sock = s.socket(s.AF_INET, s.SOCK_STREAM)

    sock.connect((address, port))

    return sock

def receive_all(socket,length): 

    full_array = bytearray()
    while len(full_array) < length:
        data = socket.recv(length)
        if not data:
            break
        full_array.extend(data)
    return full_array

