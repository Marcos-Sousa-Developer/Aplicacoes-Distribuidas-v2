import pickle

from lock_pool import lock_pool

class ListSkeleton:

    def __init__(self,N,K):
        self.lp = lock_pool(N, K) 

    def get_formatoResposta(self,n,resposta):

        formatoResposta = []

        if resposta == 'OK': 
            formatoResposta = [n+1,True]

        elif resposta == 'NOK':
            formatoResposta = [n+1,False]

        elif resposta == 'UNKNOWN RESOURCE':
            formatoResposta = [n+1,None] 
                    
        elif resposta in ['LOCKED-W', 'LOCKED-R',  'UNLOCKED', 'DISABLED']:
            formatoResposta = [n+1,resposta] 
        
        elif resposta == int:
            formatoResposta = [n+1,resposta]
        
        else:
            formatoResposta = [n+1,resposta]

        return formatoResposta

    
    def processMessage(self, pedidoEmBytes) :

        pedido = self.bytesToList(pedidoEmBytes)

        self.lp.clear_expired_locks()

        print(pedido) 

        formatoResposta = ''
        tipoPedido = pedido[0]
        
        if tipoPedido == 10: 
            numero_recurso = int(pedido[2]) 
            limite_tempo = int(pedido[-1])
            id_cliente = int(pedido[3])
            resposta = self.lp.lock(pedido[1],numero_recurso,limite_tempo,id_cliente)  

            formatoResposta = self.get_formatoResposta(tipoPedido,resposta)
        
        elif tipoPedido == 20:
            numero_recurso = int(pedido[2]) 
            id_cliente = int(pedido[-1])
            resposta = self.lp.unlock(pedido[1],numero_recurso,id_cliente)

            formatoResposta = self.get_formatoResposta(tipoPedido,resposta)
        
        elif tipoPedido == 30:
            numero_recurso = int(pedido[-1])
            resposta = self.lp.status(numero_recurso)

            formatoResposta = self.get_formatoResposta(tipoPedido,resposta)
        
        elif tipoPedido == 40:
            numero_recurso = int(pedido[-1])
            resposta = self.lp.stats('K', numero_recurso) 

            formatoResposta = self.get_formatoResposta(tipoPedido,resposta)
        
        elif tipoPedido == 50:
            resposta = self.lp.stats('N',None) 

            formatoResposta = self.get_formatoResposta(tipoPedido,resposta)
        
        elif tipoPedido == 60:
            resposta = self.lp.stats('D',None)

            formatoResposta = self.get_formatoResposta(tipoPedido,resposta) 
        
        else:
            formatoResposta = self.get_formatoResposta(tipoPedido,self.lp)
        
        return self.listToBytes(formatoResposta)


    def bytesToList(self,msg_bytes):

        return pickle.loads(msg_bytes)
    
    def listToBytes(self,obj):

        return pickle.dumps(obj)

    #fim do metodo processMessage
    #outros métodos possíveis