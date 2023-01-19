#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - lock_server.py
Grupo: 54
Números de aluno: 55852 e 56909 
"""

# Zona para fazer importação

import time as t

from operator import itemgetter

###############################################################################

class resource_lock:
    def __init__(self, resource_id):
        """
        Define e inicializa as propriedades do recurso para os bloqueios.
        """
        self.resource_id = resource_id #ID do recurso

        self._status = 'UNLOCKED' #estado_inicial
        
        self._counterWriteBlocks = 0 #contador de bloqueios de escrita com o valor 0

        self.blockListW = [] #listas de bloqueios de escrita vazias.

        self.blockListR = [] #listas de bloqueios de leitura vazias.

    def lock(self, type, client_id, time_limit):
        """
        Tenta bloquear o recurso pelo cliente client_id, durante time_limit 
        segundos. Retorna OK ou NOK. O bloqueio pode ser de escrita (type=W)
        ou de leitura (type=R).
        """

        if type == 'W':

            if self.status() == 'UNLOCKED':
            
                self._status = 'LOCKED-W'
                
                self._counterWriteBlocks += 1

                deadline = t.time() + time_limit

                self.blockListW.append((client_id,deadline))

                return 'OK'

            else:

                return 'NOK'
                
        elif type == 'R':

            if self.status() in ['UNLOCKED','LOCKED-R']:

                deadline = t.time() + time_limit

                self.blockListR.append((client_id,deadline))
                

                if self.status() == 'UNLOCKED':
                    self._status = 'LOCKED-R'
                
                return 'OK'
            
            else:
                return 'NOK'
            

    def release(self):
        """
        Liberta o recurso incondicionalmente, alterando os valores associados
        ao bloqueio.
        """
        
        self._status = 'UNLOCKED'

    def removeRblocks(self, lista):

        for x in lista:
            self.blockListR.remove(x)
            

    def unlock(self, type, client_id):
        """
        Liberta o recurso se este está bloqueado pelo cliente client_id.
        Retorna OK ou NOK.O desbloqueio pode ser relacionado a bloqueios 
        de escrita (type=W) ou de leitura (type=R), consoante o tipo.
        """
        if type == 'W':

            if self.status() == 'LOCKED-W':

                if self.blockListW[0][0] == client_id:

                    self.blockListW.remove(self.blockListW[0])
            
                    self.release()
                
                    return 'OK'
                else:
                    return 'NOK'

            else:
                return 'NOK'
                
        elif type == 'R':
            lremoveRblocks = list()
            if self.status() == 'LOCKED-R':
                inBlockList = False
                for x in self.blockListR:
                    if x[0] == client_id:
                        inBlockList = True
                        lremoveRblocks.append(x)
          
                self.removeRblocks(lremoveRblocks)    
                if len(self.blockListR) == 0:
                    self.release()
                    return 'OK'
                        
                elif inBlockList == False:
                    return 'NOK'

                elif inBlockList == True:
                    return 'OK'
           
            else:
                return 'NOK'

    def status(self):
        """
        Obtém o estado do recurso. Retorna LOCKED-W ou LOCKED-R ou UNLOCKED 
        ou DISABLED.
        """
        return self._status

    def stats(self):
        """
        Retorna o número de bloqueios de escrita feitos neste recurso. 
        """
        return self._counterWriteBlocks
   
    def disable(self):
        """
        Coloca o recurso como desabilitado incondicionalmente, alterando os 
        valores associados à sua disponibilidade.
        """
        self._status = 'DISABLED'

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print ou str.
        """
    
        output = "R {} {} {} ".format(self.resource_id,self.status(),self.stats())
        if self.status() == 'LOCKED-W':

            output +=  (str(self.blockListW[0][0]) + " " + str(self.blockListW[0][1]))

        elif self.status() == 'LOCKED-R': 

            output += (str(len(self.blockListR)) + " " + str(max(self.blockListR, key= itemgetter(1))[1]) )
        
        # Se o recurso está bloqueado para a escrita:
        # R <num do recurso> LOCKED-W <vezes bloqueios de escrita> <id do cliente> <deadline do bloqueio de escrita>
        # Se o recurso está bloqueado para a leitura:
        # R <num do recurso> LOCKED-R <vezes bloqueios de escrita> <num bloqueios de leitura atuais> <último deadline dos bloqueios de leitura>
        # Se o recurso está desbloqueado:
        # R <num do recurso> UNLOCKED
        # Se o recurso está inativo:
        # R <num do recurso> DISABLED

        return output

###############################################################################

class lock_pool:
    def __init__(self, N, K):
        """
        Define um array com um conjunto de resource_locks para N recursos. 
        Os locks podem ser manipulados pelos métodos desta classe. 
        Define K, o número máximo de bloqueios de escrita permitidos para cada 
        recurso. Ao atingir K bloqueios de escrita, o recurso fica desabilitado.
        """
        self.arrayResource_locks = list() # array de resource_lock
        
        for x in range(1,N+1): 
            self.arrayResource_locks.append(resource_lock(x))

        self.maxBlocks = K #numero maximo de bloqueios
        
    def clear_expired_locks(self):
        """
        Verifica se os recursos que estão bloqueados ainda estão dentro do tempo
        de concessão dos bloqueios. Remove os bloqueios para os quais o tempo de
        concessão tenha expirado.
        """
        current_time = t.time()
        
        for r in self.arrayResource_locks:

            for x in r.blockListW:

                if x[1] < current_time:

                    r.blockListW.remove(x)

                    if r.status() != 'DISABLED':

                        r.release()

            for x in r.blockListR:

                if x[1] < current_time: 

                    r.blockListR.remove(x)

                    if len(r.blockListR) == 0 and r.status() != 'DISABLED':

                        r.release()
                        
            if self.maxBlocks == r.stats():

                if len(r.blockListR)==0 and len(r.blockListW)==0:

                    r.disable()
            

    def lock(self, type, resource_id, client_id, time_limit):
        """
        Tenta bloquear (do tipo R ou W) o recurso resource_id pelo cliente client_id, 
        durante time_limit segundos. Retorna OK, NOK ou UNKNOWN RESOURCE.
        """
        resource_lock = None
        try:
            if resource_id > 0:
                self.arrayResource_locks[resource_id-1]
            else:
                return 'UNKNOWN RESOURCE'
        except:
            return 'UNKNOWN RESOURCE'

        if type == 'W':    
            writeBlocks = self.arrayResource_locks[resource_id-1].stats()

            if writeBlocks < self.maxBlocks:

                return self.arrayResource_locks[resource_id-1].lock(type,client_id,time_limit)

            return 'NOK'
            
        elif type == 'R':
            return self.arrayResource_locks[resource_id-1].lock(type,client_id,time_limit)


    def unlock(self, type, resource_id, client_id):
        """
        Liberta o bloqueio (do tipo R ou W) sobre o recurso resource_id pelo cliente 
        client_id. Retorna OK, NOK ou UNKNOWN RESOURCE.
        """

        resource_lock = None
        try:
            if resource_id > 0:
                resource_lock = self.arrayResource_locks[resource_id-1]
            else:
                return 'UNKNOWN RESOURCE'
        except:
            return 'UNKNOWN RESOURCE'
        
        return resource_lock.unlock(type,client_id)
        

    def status(self, resource_id):
        """
        Obtém o estado de um recurso. Retorna LOCKED, UNLOCKED,
        DISABLED ou UNKNOWN RESOURCE.
        """
        resource_lock = None
        
        try:
            if resource_id > 0:
                resource_lock = self.arrayResource_locks[resource_id-1]
            else:
                return 'UNKNOWN RESOURCE'
        except:
            return 'UNKNOWN RESOURCE'

        return resource_lock.status()

    def counter(self,state):
        counter = 0
        for resource in self.arrayResource_locks:
            if resource.status() == state:
                counter += 1
        return counter

    def stats(self, option, resource_id):
        """
        Obtém o estado do serviço de gestão de bloqueios. Se option for K, retorna <número de 
        bloqueios feitos no recurso resource_id> ou UNKNOWN RESOURCE. Se option for N, retorna 
        <número de recursos bloqueados atualmente>. Se option for D, retorna 
        <número de recursos desabilitados>
        """
        if option == 'K':
            try:
                if resource_id > 0:
                    resource_lock = self.arrayResource_locks[resource_id-1]
                else:
                    return 'UNKNOWN RESOURCE'
            except:
                return 'UNKNOWN RESOURCE'
            
            return resource_lock.stats()
            
        elif option == 'N':

            return self.counter('UNLOCKED')
        
        elif option == 'D':

            return self.counter('DISABLED')

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print ou str.
        """
        output = ""
        
        for r in self.arrayResource_locks:

            output += str(r) + '\n' 
        #
        # Acrescentar no output uma linha por cada recurso
        #
        return output