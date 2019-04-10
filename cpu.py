import time
from escalonator import Escalonator

class CPU():
    def __init__(self, escalonator_type, preemptive=False, quantum =2, override = .015):   
        self.ready_queue = []
        self.escalonator = Escalonator()
        self.cpu_time = 0
        self.escalonator_type = escalonator_type
        self.preemptive = preemptive
        self.quantum = quantum
        self.override = override
        
    def execute(self):
        if not self.preemptive:
            process = self.ready_queue[0]
            del self.ready_queue[0]
            self.cpu_time = process.execution_time
            time.sleep(self.cpu_time)
            print ("CPU executou {} por {}s" .format(process.id, process.execution_time))
            process.execution_time -= self.cpu_time 
        else:
            self.cpu_time = self.quantum
            for process in self.ready_queue:
                
                if self.quantum > process.execution_time:
                    time.sleep(self.quantum - process.execution_time)    
                    print ("CPU executou {} que precisa de {}s por {}s" .format(process.id, process.execution_time, self.quantum-process.execution_time))
                    process.execution_time -= self.quantum - process.execution_time
                    
                else:
                    time.sleep(self.quantum)
                    print ("CPU executou {} que precisa de {}s por {}s" .format(process.id, process.execution_time, self.quantum))
                    process.execution_time -= self.quantum
                    
                if process.execution_time == 0:
                    process.finished = True
                    self.ready_queue.remove(process)
                    continue
                        
                if all(a.finished for a in  self.ready_queue):
                    break
                else:
                    self.ready_queue = self.ready_queue[1:]+[self.ready_queue[0]]
                    
                time.sleep(self.override)
                
            
            
    def queue(self, process):
        self.ready_queue.append(process)
        self.escalonator.sort(self.ready_queue, self.escalonator_type)
