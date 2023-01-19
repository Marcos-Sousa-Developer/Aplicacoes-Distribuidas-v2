import sock_utils, argparse, struct, sys

from lock_skel import ListSkeleton

import select as sel


parser = argparse.ArgumentParser()

parser.add_argument('adress', type=str, help='O IP ou hostname do servidor que fornece os recursos')

parser.add_argument('port', type=int, help='o porto TCP onde o servidor recebe pedidos de ligação')

parser.add_argument('N', type=int, help='Número de recursos que serão geridos pelo servidor')

parser.add_argument('K', type=int, help='Número de bloqueios de escrita permitidos em cada recurso')

argument = parser.parse_args()

print()

HOST = argument.adress

PORT = argument.port

listen_socket = sock_utils.create_tcp_server_socket(HOST,PORT,1)

answer = ""

lskel = ListSkeleton(argument.N, argument.K) 

socket_list = [listen_socket, sys.stdin] 

def processMessage(socket,req_size_bytes):
    
    req_size = struct.unpack('i',req_size_bytes)[0]
    req_bytes = sock_utils.receive_all(socket,req_size)

    return lskel.processMessage(req_bytes) 

def sendMessage(socket,resp_bytes):
    
    resp_size_bytes = struct.pack('i',len(resp_bytes))
    socket.sendall(resp_size_bytes)
    socket.sendall(resp_bytes)

    resposta = lskel.bytesToList(resp_bytes) 

    if 71 in resposta: 
        print("Resposta Enviada:")
        for x in range(len(resposta)):
            print(resposta[x])
        print()
    
    else: 
        print("Resposta Enviada:", resposta)
        print()

while True:

    try:

        R, W, X = sel.select(socket_list, [], [])

        for socket in R:

            if socket is listen_socket:
                
                conn_sock, addrlisten_socket = socket.accept()
                addr, port = conn_sock.getpeername()
                print('Novo cliente ligado no HOST: {} e PORT: {}'.format(addr,port))
                print()
                socket_list.append(conn_sock) # Adiciona ligação à lista   

            elif socket is sys.stdin:
                pedido = socket.readline().strip()
                if pedido == 'EXIT':
                    sys.exit(0)

            else:

                req_size_bytes = socket.recv(4)
                
                if req_size_bytes:
                    addr, port = socket.getpeername()
                    print('Cliente com IP ({}) na porta ({}) fez o sequinte pedido: '.format(addr,port), end='')
                    resp_bytes = processMessage(socket,req_size_bytes)
                    sendMessage(socket,resp_bytes)
                    
                else:
                    addr, port = socket.getpeername()
                    socket.close() # cliente fechou ligação
                    socket_list.remove(socket)
                    print('Cliente com IP: {} na porta: {} fechou ligação'.format(addr,port))

    except (KeyboardInterrupt,SystemExit):
        break

    except:
        print(sys.exc_info()) 
        break

print()
print("Vou encerrar o Servidor")
listen_socket.close()
sys.exit()