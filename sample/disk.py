class Page():
    def __init__(self, proc_id, allocated=False):
        self.proc_id = proc_id
        self.isAllocated = allocated


class Disk():
    def __init__(self):
        self.memory = []

    def putProcess(self, id, qnt):
        count = qnt
        for index in range(len(self.memory)):
            if count == 0:
                break
            allocated = self.memory[index].isAllocated
            if self.memory[index].proc_id == id and not allocated:
                self.memory[index].isAllocated = True
                count -= 1

    def insertProcess(self, id, qnt):
        count = qnt
        for __ in range(count):
            page = Page(id, allocated=True)
            self.memory.append(page)

    def remProcess(self, process, qnt):
        count = qnt
        for index in range(len(self.memory)):
            if count == 0:
                break
            allocated = self.memory[index].isAllocated
            if self.memory[index].proc_id == process.id and allocated:
                self.memory[index].isAllocated = False
                count -= 1
