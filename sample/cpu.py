from process import Process
from escalonator import Escalonator


class CPU():
    """ Classe responsável pela execução dos processos """
    State = ['Ocioso', 'Executando', 'Pronto',
             'Sobrecarga', 'PosSobrecarga', 'PreSobrecarga']

    def __init__(self, escalonator, mmu, ioqueue, quantum=0, process=None, disk=None):
        """ Inicialização com as caracteristicas de uma CPU
        Args:
            escalonator (Escalonator): tipo de escalonador utilizado na CPU
            quantum (int): quantidade de tempo destinado a execução do processo
            process (Process): processo a ser executado na CPU

        """

        self.clock = 0              # Tempo que a CPU permaneceu ligada
        self.quantum = quantum
        self.escalonator = escalonator
        self.process = process
        self.processing_time = 0
        self.concluded_process_time = []
        self.mmu = mmu
        self.ioqueue = ioqueue
        self.override_time = 0
        self.state = CPU.State[0]
        self.disk = disk
        # Verificação de preemptividade
        if escalonator.algorithm in escalonator.NON_PREEMPTIVE_ALGORITHMS:
            self.preemptiveness = False
        else:
            self.preemptiveness = True

    def runClock(self):
        """ Método para execução de um clock da CPU """

        if self.state == CPU.State[5]:
            self.state = CPU.State[3]

        if self.state == CPU.State[2] or self.state == CPU.State[4]:
            self.override_time = 0
            self.state = CPU.State[0]

        while self.state == CPU.State[0]:
            if self.escalonator.ready_queue:
                self.state = CPU.State[1]
                self.process = self.escalonator.ready_queue.pop(0)
            else:
                return
            allocated = self.mmu.isAllocated(self.process)
            self.process.next_state()

            if not allocated:
                self.ioqueue.enqueue(self.process)
                self.state = CPU.State[0]
            else:
                self.processing_time = 0
                self.mmu.referentiate(self.process)

        if self.preemptiveness:

            if self.state != CPU.State[3]:
                self.execute()
                if self.quantum - self.processing_time == 0:
                    self.state = CPU.State[5]

            if self.process.is_finished(self.mmu):
                self.mmu.deallocate(self.process)
                self.concluded_process_time.append(
                    (self.clock+1) - self.process.start)
                self.state = CPU.State[2]

            elif self.quantum - self.processing_time == 0:
                if self.escalonator.override == 0:
                    self.state = CPU.State[2]
                    self.escalonator.update_attributes()
                    self.escalonator.ready_queue.append(self.process)
                    self.override_time = 0

                elif self.escalonator.override - self.override_time == 0:
                    self.state = CPU.State[4]
                    self.escalonator.update_attributes()
                    self.escalonator.ready_queue.append(self.process)
                    self.override_time = 0
                else:
                    self.override_time += 1
                    return
        else:
            self.execute()
            if self.process.is_finished(self.mmu):
                self.mmu.deallocate(self.process)
                self.concluded_process_time.append(
                    (self.clock+1) - self.process.start)
                self.state = CPU.State[2]

    def execute(self):
        """ Método para executar um processo """
        self.process.next_state()
        self.processing_time += 1
        self.process.execution_time -= 1
