import time
import random
import ioqueue

class Process():
    """ Classe responsável pela instanciação dos processos """
    States = ["Bloqueado", "Pronto", "Executando"]  # Estados de um processo
    
    def __init__(self, id, start, execution_time, deadline = 0, io=None, needIO=False, priority=0):
        """ Inicialização de um processo.
        Args:
            id (int): indentificador do processo
            start (int): tempo de inicio do processo
            execution_time (int): tempo necessário para o processo ser concluido
            deadline (int): tempo limite máximo que o processo deve ser executado
            io (IO): Objeto responsável pela fila de IO
            needIO (bool): necessidade de IO 
            priority (int): prioridade do processo
        """        
        self.id = id
        self.priority = priority
        self.deadline = deadline
        self.execution_time = execution_time
        self.state = self.__class__.States[1]
        self.needIO = needIO
        self.io = io
        self.start = start
    
    def nextState(self):
        """ Próximo estado do processo """
        actual_index = self.__class__.States.index(self.state)
        index = (actual_index +1) % len(self.__class__.States)
        self.state = self.__class__.States[index]
        if self.state == self.__class__.States[0]:
            self.io.enqueue(self)                  
     
    def prevState(self):
        """ Estado prévio do processo """
        actual_index = self.__class__.States.index(self.state)
        index = (actual_index - 1) % len(self.__class__.States)
        self.state = self.__class__.States[index]
        
       
    def finished(self):
        """ Verificação de conclusão do processo """
        if self.execution_time == 0:
            return True
        else:
            if self.state == self.__class__.States[2] and self.needIO:
                # Se estava no estado de Executando e precisa de IO então vá para o estado de Bloqueado
                self.nextState()
            else: 
                self.prevState()
            return False
        
    def outOfTime(self, clock):
        """ Verificação do tempo limite máximo 
        Args:
            clock (int): tempo total de execução da CPU 
        """
        if clock > self.start + self.deadline:
            return True
        return False
    
    def isArrived(self, clock):
        """ Verificação se um processo está apto a entrar na CPU  """
        if clock >= self.start:
            return True
        return False
    
    def __repr__(self):
        """ Representação do processo. Útil em print() """
        return ("Processo {}\n\tStart: {}\n\tDeadline: {}\n\tTempo de execução: {}" .format(self.id, self.start, self.deadline, self.execution_time))
