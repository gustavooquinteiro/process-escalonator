import time
import random
import ioqueue

class Process():
    """ Classe responsável pela instanciação dos processos """
    States = ["Bloqueado", "Pronto", "Executando"]  # Estados de um processo
    
    def __init__(self, id, start, execution_time,
                 numpages, deadline = 0, io=None, need_io=False, priority=0):
        """ Inicialização de um processo.
        Args:
            id (int): indentificador do processo
            start (int): tempo de inicio do processo
            execution_time (int): tempo necessário para o processo ser concluido
            deadline (int): tempo limite máximo que o processo deve ser executado
            io (IO): Objeto responsável pela fila de IO
            need_io (bool): necessidade de IO 
            priority (int): prioridade do processo
        """        
        self.id = id
        self.priority = priority
        self.deadline = deadline
        self.execution_time = execution_time
        self.state = self.States[2]
        self.need_io = need_io
        self.io = io
        self.start = start
        self.numpages = numpages
        self.pages = []
        self.laxity = 0

    def get_pages(self):
        return self.pages

    def set_pages(self, list_pages):
        self.pages = list_pages
        
    def add_pages(self, list_pages):
        for data in list_pages:
            self.pages.append(data)
    
    def get_num_pages(self):
        return self.numpages
    
    def next_state(self, mmu):
        """ Próximo estado do processo """
        actual_index = self.States.index(self.state)
        index = (actual_index +1) % len(self.States)
        self.state = self.States[index]
     
    def previous_state(self):
        """ Estado prévio do processo """
        actual_index = self.States.index(self.state)
        index = (actual_index - 1) % len(self.States)
        self.state = self.States[index]
        
       
    def is_finished(self, mmu):
        """ Verificação de conclusão do processo """
        if self.execution_time == 0:
            return True
        else:
            if self.state == self.States[2]:
                # Se estava no estado de Executando e precisa de IO então vá para o estado de Bloqueado
                self.next_state(mmu)
            else: 
                self.previous_state()
            return False
        
    def is_out_deadline(self):
        """ Verificação do tempo limite máximo """
        return self.deadline < 0
    
    def is_arrived(self, clock):
        """ Verificação se um processo está apto a entrar na CPU  """
        return clock == self.start
    
    def __repr__(self):
        """ Representação do processo. Útil em print() """
        return ("Processo {}\n\tStart: {}\n\tDeadline: {}\n\tTempo de execução: {}" .format(self.id, self.start, self.deadline, self.execution_time))
