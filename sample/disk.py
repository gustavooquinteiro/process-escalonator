class Page():
    def __init__(self, proc_id, allocated=False):
        self.proc_id = proc_id
        self.is_allocated = allocated


class Disk():
    def __init__(self):
        self.memory = []

    def put_process(self, pid, qnt):
        count = qnt
        for index in range(len(self.memory)):
            if count == 0:
                break
            allocated = self.memory[index].is_allocated
            if self.memory[index].proc_id == pid and not allocated:
                self.memory[index].is_allocated = True
                count -= 1

    def insert_process(self, pid, qnt):
        count = qnt
        for __ in range(count):
            page = Page(pid, allocated=True)
            self.memory.append(page)

    def remove_process(self, process, qnt):
        count = qnt
        for index in range(len(self.memory)):
            if count == 0:
                break
            allocated = self.memory[index].is_allocated
            if self.memory[index].proc_id == process.pid and allocated:
                self.memory[index].is_allocated = False
                count -= 1
