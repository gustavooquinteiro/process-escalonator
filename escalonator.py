import process

class Escalonator():
    def __init__(self):
        pass
        
    def sort(self, process_queue, typeof):
        if typeof == "SJF":
            process_queue.sort(key=self.shortest)
        elif typeof == "FCFS" or typeof == "RR":
            process_queue        
            
        
    def shortest(self, element):
        return element.execution_time

