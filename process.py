import threading

class Process(threading.Thread):

    def __init__(self, id, execution_time, cpu, priority = 0, deadline = 0):
        super().__init__()
        self.id = id
        self.priority = priority
        self.deadline = deadline
        self.execution_time = execution_time
        self.cpu = cpu
        self.finished = False
        
    def run(self):
        while not self.finished:
            self.cpu.queue(self)
        
 
