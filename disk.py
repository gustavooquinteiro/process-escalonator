class Page():
    def __init__(self, proc_id, allocated=False):
        self.proc_id = proc_id
        self.isAllocated = allocated

class Disk():
    def __init__(self):
        self.memory = []

    def putProcess(self, id, qnt):
        for i in range(qnt):
            page = Page(id, allocated=True)
            self.memory.append(page)

    def remProcess(self, process, qnt):
        for index in range(len(self.memory)):
            if qnt == 0:
                break
            
            if self.memory[index].proc_id == process.id:
                self.memory[index].isAllocated = False
                qnt -= 1