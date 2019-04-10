import cpu
import random
import process
import escalonator

escalonator_type = "RR"
c = cpu.CPU(escalonator_type, True)
for i in range(5):
    p = process.Process(i, random.randint(1, 5), c)
    c.queue(p)

while len(c.ready_queue) > 0:
    c.execute()
