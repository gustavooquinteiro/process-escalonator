from ioqueue import IO
import cpu
import random
import process
import escalonator

quantum = int(input("Quantum: "))
override = int(input("Sobrecarga: "))
escalonator = escalonator.Escalonator("SJF", quantum, override)
c = cpu.CPU(escalonator)
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
    p = process.Process(id, start, execution_time, deadline, io)
    processes.append(p)
    
for i in range(n):
    print("Chegou o processo {}" .format(processes[i].id))
    escalonator.ready_queue.append(processes[i])
    
escalonator.queue()
    
