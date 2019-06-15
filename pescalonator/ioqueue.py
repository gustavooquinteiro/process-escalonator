import time 
import random
import threading
import process 
import escalonator 

class IO(): 
    def __init__(self, escalonator = None):
        self.queue = []
        self.mutex = threading.Condition()
        self.ioWorking = threading.Event()
        io = threading.Thread(target=self.run)
        self.escalonator = escalonator
        io.start()
        
    def run(self):
        while True:
            self.mutex.acquire()
            if len(self.queue) > 0:
                self.wait_for_resource()
                self.mutex.release()
                self.ioWorking.clear()
            else:
                self.mutex.release()
                self.ioWorking.wait()
                
            
    def enqueue(self, process):
        self.mutex.acquire()
        self.queue.append(process)
        self.mutex.release()
        self.ioWorking.set()
        
    def wait_for_resource(self):
        
        process = self.queue[0]
        print ("Processo {} na fila de Bloqueados " .format(process.id))
        time.sleep(random.randint(5, 10))
        process.nextState()
        if process.state == process.__class__.States[1]:
            self.escalonator.queue(process)
            print ("Processo {} na fila de Pronto " .format(process.id))
        del self.queue[0]
