#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - lock_client.py
Grupo: 54
Números de aluno: 55852 e 56909
"""
# Zona para fazer imports

import argparse

import net_client as netc

import sys

import time as t

from lock_stub import ListStub


# Programa principal

comando = None

def typeInt(value):

    try:
        return type(int(value)) == int
    except:
        return False
        

def verifica():

    global comando

    while True:

        while True:
            comando = input('comando > ') 

            list_comando = comando.split()

            if len(list_comando) > 0:
                break
        
        if list_comando[0] in ["LOCK-W","LOCK-R"]:

            if len(list_comando) < 3:

                print("MISSING ARGUMENTS")

            elif len(list_comando) == 3 and typeInt(list_comando[1]) == True and typeInt(list_comando[2]) == True:

                return True

            else:

                print("UNKNOWN COMMAND")

        elif list_comando[0] in ["UNLOCK-W", "UNLOCK-R", 'STATUS'] :

            if len(list_comando) < 2:

                print("MISSING ARGUMENTS")

            elif len(list_comando) == 2 and typeInt(list_comando[1]) == True:

                return True

            else:
                
                print("UNKNOWN COMMAND")
            
        elif list_comando[0] == 'STATS':

            if len(list_comando) > 1:
            
                if list_comando[1] == 'K':

                    if len(list_comando) == 3:

                        if typeInt(list_comando[2]) == True:
                            return True
                        else:
                            print("UNKNOWN COMMAND")
                                
                    elif len(list_comando) < 3:

                        print("MISSING ARGUMENTS")

                    else:
                        print("UNKNOWN COMMAND")                 

                elif list_comando[1] in ['N','D']:
                        
                    if len(list_comando) == 2:
                        return True

                    elif len(list_comando) < 2:

                        print("MISSING ARGUMENTS")
                        
                    else:
                        print("UNKNOWN COMMAND")

                else:
                    print("UNKNOWN COMMAND")
            else:
                print("MISSING ARGUMENTS")


        elif list_comando[0] in ['PRINT']:

            if len(list_comando)== 1:

                return True

            else:
                print("UNKNOWN COMMAND")

        elif list_comando[0] == 'EXIT':

            if len(list_comando) == 1:
                print("Eu cliente " + str(argument.ID_cliente) + " vou encerrar")
                sys.exit(0)

            else:

                print("UNKNOWN COMMAND")

        elif list_comando[0] == 'SLEEP':

            if len(list_comando) == 2 and typeInt(list_comando[-1]) == True:

                t.sleep(int(list_comando[-1]))

            elif len(list_comando) < 2:
                
                print("MISSING ARGUMENTS")

            else:
                print("UNKNOWN COMMAND")
                
        else:
            
            print("UNKNOWN COMMAND")
        print()
        
def terminaCliente():

    print("Eu cliente " + str(argument.ID_cliente) + " vou encerrar")
    lstub.disconnect()
    sys.exit(0)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('ID_cliente', type=int, help='O ID único do cliente')

    parser.add_argument('HOST', type=str, help='O IP ou hostname do servidor que fornece os recursos')

    parser.add_argument('PORT', type=int, help='o porto TCP onde o servidor recebe pedidos de ligação')

    argument = parser.parse_args()
    print()

    try:
        lstub = ListStub(argument.HOST,argument.PORT) 
    except ConnectionRefusedError:
        print("Servidor não está conectado")
        sys.exit(1)

    while True:

        try:
            if verifica() == True:

                pedido = comando.split()

                resposta = ''

                if pedido[0] in ["LOCK-W","LOCK-R"]:

                    resposta = lstub.lock(comando,argument.ID_cliente)
                    
                elif pedido[0] in ["UNLOCK-W", "UNLOCK-R"]:
                    
                    resposta = lstub.unlock(comando,argument.ID_cliente)

                elif pedido[0] == 'STATUS':

                    resposta = lstub.status(comando)

                elif pedido[0] == 'STATS': 
                    
                    resposta = lstub.stats(comando)

                else:
                    resposta = lstub.print(comando)

                if "PRINT" not in comando:
                    print("Resposta Recebida: ",resposta)
                    print()
                else:
                    print("Resposta Enviada: ")
                    for x in range(len(resposta)):
                        print(resposta[x])
                    print()

        except BrokenPipeError:
            print("Servidor foi desconectado")
            break

        except KeyboardInterrupt:
            print()
            break

    terminaCliente()

    

        

        

    

    

