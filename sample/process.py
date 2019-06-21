class Process():
    """ Classe responsável pela instanciação dos processos """
    States = ["Bloqueado", "Pronto", "Executando"]  # Estados de um processo

    def __init__(self, pid, start, execution_time,
                 numpages, deadline, priority):
        """ Inicialização de um processo.
        Args:
            id (int): indentificador do processo
            start (int): tempo de inicio do processo
            execution_time (int): tempo necessário para o processo ser concluido
            deadline (int): tempo limite máximo que o processo deve ser executado
            priority (int): prioridade do processo
        """
        self.pid = pid
        self.priority = priority
        self.deadline = deadline
        self.execution_time = execution_time
        self.state = self.States[2]
        self.start = start
        self.numpages = numpages
        self.pages = []
        self.laxity = 0

    def add_pages(self, list_pages):
        """" Insere páginas no processo """
        for data in list_pages:
            self.pages.append(data)

    def next_state(self):
        """ Próximo estado do processo """
        actual_index = self.States.index(self.state)
        index = (actual_index + 1) % len(self.States)
        self.state = self.States[index]

    def previous_state(self):
        """ Estado prévio do processo """
        actual_index = self.States.index(self.state)
        index = (actual_index - 1) % len(self.States)
        self.state = self.States[index]

    def is_finished(self):
        """ Verificação de conclusão do processo """
        if self.execution_time == 0:
            return True
        else:
            if self.state == self.States[2]:
                # Se estava no estado de Executando e precisa de IO então vá para o estado de Bloqueado
                self.next_state()
            else:
                self.previous_state()
            return False

    def is_out_deadline(self):
        """ Verificação do tempo limite máximo """
        return self.deadline < 0

    def is_out_laxity(self):
        """ Verificação do laxity máximo """
        return self.laxity < 0

    def is_arrived(self, clock):
        """ Verificação se um processo está apto a entrar na CPU
        Args:
            clock (int): clock atual da CPU
        """
        self.laxity = self.deadline - clock - self.execution_time
        return clock == self.start

    def __repr__(self):
        """ Representação do processo. Útil em print() """
        process_info = {
            "PID": self.pid,
            "Start time": self.start,
            "Execution time": self.execution_time,
            "Deadline": self.deadline
            }
        info_array = [""]
        for x, y in process_info.items():
            info_array.append("\t{}: {}\n" .format(x, y))
        return (''.join(info_array))
