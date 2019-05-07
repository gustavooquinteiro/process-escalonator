import time
import process
import threading

class Escalonator():
    """ Classe responsável pela  gerência da fila de prontos """
    def __init__(self, typeof="FCFS", override = .015, cpu=None):
        """ Método de inicialização de um escalonador.
        Args:
            typeof (str): tipo de algoritmo de escalonamento que será utilizado
            override (int): tempo necessário para a troca de contexto de processos
            cpu (CPU): objeto da cpu responsável pela execução dos processos
        
        """
        self.ready_queue = []
        self.algorithm = typeof
        self.override = override         
        self.cpu = cpu
        self.mutex = threading.Lock()

        
    def queue(self):
        """ Ordena a fila de prontos de acordo com o algoritmo escolhido e inicia a execução na CPU """
        if self.algorithm == "FCFS" or self.algorithm == "RR":
            self.ready_queue.sort(key=lambda x: x.start)
        if self.algorithm == "SJF":
            self.ready_queue.sort(key=lambda x: (x.start, x.execution_time))
        if self.algorithm == "EDF":
            self.ready_queue.sort(key=lambda x: (x.start, x.deadline))
        self.cpu.cpuWorking.set()

    def updateDeadline(self):
        for process in self.ready_queue:     
            if process.start < self.cpu.cpu_execution:
                process.deadline -= self.cpu.processing_time
            print ("Processo {} agr com deadline de {}" .format(process.id, process.deadline))        
        
    def remove(self, process):
        """ Remove o processo da fila de prontos, se ele já estiver finalizado, e coloca o próximo da fila na frente.
            Args:
                process (Process): processo a ser removido da fila
        """
        if self.cpu.preemptiveness:
            if process.finished():
                self.ready_queue.remove(process)
            else:
                self.updateDeadline()
                self.next_process()
                time.sleep(self.override)
                if process.needIO:
                    self.ready_queue.remove(process)                    
                self.cpu.cpu_execution += self.override
                
            
            if process.outOfTime(self.cpu.cpu_execution) and self.algorithm == "EDF":
                print("Processo {} está fora do prazo" .format(process.id))
        else:
            self.ready_queue.remove(process)

    def next_process(self):
        """ Atualiza a fila de prontos colocando o primeiro da fila no final da fila ou reoordenando-a caso seja o algoritmo de escalonamento EDF  """
        if self.algorithm == "EDF":
            self.ready_queue.sort(key=lambda x: (x.start, x.deadline))  
        elif len(self.ready_queue) > 1:
            self.ready_queue = self.ready_queue[1:]+[self.ready_queue[0]]        
