import time
import random
import ioqueue

class Process():
    States = ["Bloqueado", "Pronto", "Executando"]
    
    def __init__(self, id, start, execution_time, deadline = 0, io=None, needIO=False, priority=0):
        super().__init__()
        self.id = id
        self.priority = priority
        self.deadline = deadline
        self.execution_time = execution_time
        self.state = self.__class__.States[1]
        self.needIO = needIO
        self.io = io
        self.start = start
    
    def nextState(self):
        actual_index = self.__class__.States.index(self.state)
        index = (actual_index +1) % len(self.__class__.States)
        self.state = self.__class__.States[index]
        if self.state == self.__class__.States[0]:
            self.io.enqueue(self)                  
     
    def prevState(self):
        actual_index = self.__class__.States.index(self.state)
        index = (actual_index - 1) % len(self.__class__.States)
        self.state = self.__class__.States[index]
        
       
    def finished(self):
        if self.execution_time == 0:
            return True
        else:
            if self.state == self.__class__.States[2] and self.needIO:
                self.nextState()
            else:
                self.prevState()
            print("Processo {} em estado de {}" .format(self.id, self.state))
            return False
     
    def execute(self, cpu):
        self.nextState()
        print("Processo {} em estado de {}" .format(self.id ,self.state))
        if cpu.cpu_time > self.execution_time:
            cpu.processing_time = cpu.cpu_time - self.execution_time  
        else:
            cpu.processing_time = cpu.cpu_time
        time.sleep(cpu.processing_time)    
        print ("CPU executou {} que precisa de {}s por {}s" .format(self.id, self.execution_time, cpu.processing_time))
        self.execution_time -= cpu.processing_time
        cpu.cpu_execution += cpu.processing_time
        
    def outOfTime(self):
        if self.deadline <= 0:
            return True
        return False
        
    def __repr__(self):
        return ("Processo {} com deadline de: {}; e tempo de execução de: {}" .format(self.id, self.deadline, self.execution_time))
