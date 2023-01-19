from curses import keyname
import pickle, struct
import net_client as netc

class ListStub:

    def __init__(self,address,port):
        
        self.conn_sock = netc.server_connection(address, port)
        self.connect()
    
    def connect(self):

        self.conn_sock.connect()
    
    def disconnect(self):

        self.conn_sock.close()
    
    def send_receive(self,pedidoEmBytes):

        resposta = self.conn_sock.send_receive(pedidoEmBytes)

        return resposta

    def get_value(self,keyName,type = None):
        dic = {"LOCK-W":10,"LOCK-R":10,"UNLOCK-W":20,"UNLOCK-R":20,'STATUS':30, 'STATS': [40,50,60],'PRINT':70}
        
        if keyName == 'STATS': 

            if type == 'K':
                return dic[keyName][0]
            elif type == 'N':
                return dic[keyName][1]
            else:
                return dic[keyName][2]

        return dic[keyName]
    
    def lock(self,comando,IDcliente):

        pedidoLista = comando.split()
        tipoPedido = pedidoLista[0]
        tipo = tipoPedido[-1]
        numeroRecurso = pedidoLista[1]
        limiteTempo = pedidoLista[2]
        
        pedido = [self.get_value(tipoPedido), tipo, numeroRecurso, limiteTempo, IDcliente]

        resposta = self.send_receive(pickle.dumps(pedido))
        
        return resposta 

    def unlock(self,comando,IDcliente):

        pedidoLista = comando.split()
        tipoPedido = pedidoLista[0]
        tipo = tipoPedido[-1]
        numeroRecurso = pedidoLista[1]
        
        pedido = [self.get_value(tipoPedido), tipo, numeroRecurso, IDcliente]

        resposta = self.send_receive(pickle.dumps(pedido))
        
        return resposta 

    def status(self,comando):

        pedidoLista = comando.split()
        tipoPedido = pedidoLista[0]
        numeroRecurso = pedidoLista[1]
        
        pedido = [self.get_value(tipoPedido), numeroRecurso]
        resposta = self.send_receive(pickle.dumps(pedido))
        
        return resposta 

    def stats(self,comando):
        
        pedidoLista = comando.split()
        tipoPedido = pedidoLista[0]
        tipo = pedidoLista[1]
        pedido = []
        
        if len(pedidoLista) == 3:
            numeroRecurso = pedidoLista[2]
            pedido = [self.get_value(tipoPedido,tipo), numeroRecurso]
        
        else:
            pedido =  [self.get_value(tipoPedido,tipo)]

        resposta = self.send_receive(pickle.dumps(pedido))
        
        return resposta 

    def print(self,comando):
        
        pedidoLista = comando.split()
        tipoPedido = pedidoLista[0]

        pedido = [self.get_value(tipoPedido)]

        resposta = self.send_receive(pickle.dumps(pedido))

        return resposta