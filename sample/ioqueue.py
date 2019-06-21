class IO():
    """ Classe responsável pela fila de Bloqueados """
    def __init__(self, mmu, disk, escalonator=None):
        """ Inicialização da fila de bloqueados.
        Args:
            mmu (MMU): objeto gerenciador de memória
            disk (Disk): objeto onde as páginas dos processos estão armazenadas
            escalonator (Escalonator): objeto gerenciador pela fila de prontos
        """
        self.queue = []
        self.mmu = mmu
        self.escalonator = escalonator
        self.disk = disk

    def enqueue(self, process):
        """ Insere o processo na lista de bloqueados
        Args:
            process (Proces): processo a ser inserido na fila de bloqueados
        """
        self.queue.append(process)

    def is_on_queue(self, process):
        """ Verifica se um processo está na lista de bloqueados
        Args:
            process (Process): processo a ser averiguado
        """
        return process in self.queue

    def wait_for_resource(self, cpu):
        """ Aloca as páginas que o processo precisa
        Args:
            cpu (CPU): objeto que contem o processo que está sendo executado
        """
        if self.queue:
            process = self.queue[0]
            if process.numpages - len(process.pages) > 0:
                for __ in range(min(2, process.numpages - len(process.pages))):
                    process.add_pages(self.mmu.allocate_page(
                        process, cpu_process=cpu.process))
            else:
                vm = self.mmu.vm
                non_allocated_pages = list(filter(
                    lambda ref: not vm.is_page_allocated(process, ref),
                    process.pages))
                for __ in range(min(2, len(non_allocated_pages))):
                    process.add_pages(self.mmu.allocate_page(
                        process, cpu_process=cpu.process))

            if self.mmu.is_allocated(process):
                process.next_state()
                self.escalonator.ready_queue.append(process)
                del self.queue[0]
