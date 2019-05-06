from escalonator import Escalonator
from process import Process
from ioqueue import IO
from cpu import CPU
import random

quantum = int(input("Quantum: "))
override = int(input("Sobrecarga: "))
escalonator = Escalonator("RR", override)
c = CPU(escalonator, quantum)
escalonator.cpu = c
io = IO()
io.escalonator = escalonator
processes = []

n = int(input("Quantidade de processos: "))
for i in range(n):
    id = random.randint(1000, 3000)
    start = int(input("Tempo de chegada: "))
    execution_time = int(input("Tempo de execução: "))
    deadline = int(input("Deadline: "))    
    
    print("Criando o processo:\n\tID: {}\n\tTempo de inicio: {}\n\tTempo de execução: {}\n\tDeadline: {}\n" .format(id, start, execution_time, deadline                                                                                                                                                                                                                                                  ))
    p = Process(id, start, execution_time, deadline, io)
    escalonator.ready_queue.append(p)
    
escalonator.queue()
    
