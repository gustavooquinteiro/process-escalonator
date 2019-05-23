import time 
import random
import threading
import process 
import escalonator 

class IO(): 
    def __init__(self, mmu, escalonator = None):
        self.queue = []
        self.mmu = mmu
        self.mutex = threading.Condition()
        self.ioWorking = threading.Event()
        self.io = threading.Thread(target=self.run)
        self.escalonator = escalonator
        self.io.start()
        
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

    def isOnQueue(self, process):
        if process in self.queue:
            return True
        return False
        
    def wait_for_resource(self):
        process = self.queue[0]
        print ("Processo {} na fila de Bloqueados " .format(process.id))
        
        time = time.time()
        while time.time() - time < 5:
            continue

        if process.getPages() == []:
            process.setPages(self.mmu.giveMemAddr(process))
        elif process.execution_time != 0:
            self.mmu.reallocate(process)
            process.nextState(self.mmu)
            if process.state == process.__class__.States[1]:
                self.escalonator.ready_queue.append(process)
                # self.escalonator.queue()
                print ("Processo {} na fila de Pronto " .format(process.id))
        del self.queue[0]
