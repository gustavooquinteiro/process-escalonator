from ioqueue import IO
import cpu
import random
import process
import escalonator

l = [True, False]
io = IO()
escalonator = escalonator.Escalonator("SJF")
c = cpu.CPU(escalonator)
escalonator.cpu = c
io.escalonator = escalonator
processes = []
start = 0
for i in range(3):
    id = random.randint(1000, 3000)
    start = random.randint(start, 10)
    execution_time =  random.randint(1, 5)
    priority = random.randint(1, 10)
    deadline = random.randint(1, 10)
    needIO = random.choice(l)
    
    print("Criando o processo:\n\tID: {}\n\tTempo de inicio: {}\n\tTempo de execução: {}\n\tPrioridade: {}\n\tDeadline: {}\n\tPrecisa de IO: {}\n" .format(id, start, execution_time, priority, deadline, needIO                                                                                                                                                                                                                                                                  ))
    
    
    p = process.Process(id, start, execution_time, priority, deadline, needIO, io)
    escalonator.queue(p)    
    processes.append(p)
