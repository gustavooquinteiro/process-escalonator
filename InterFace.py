import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QIcon
from pescalonator.process import Process
from WProcess import Window_Process


class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.idProcess = 1
        self.process = None
        self.listProcess = []

        self.setGeometry(300, 300, 900, 400)
        self.setWindowTitle('SO SIMULATOR')
        self.show()

        self.statusBar()

        openFile = QAction(QIcon('openThing.png'), '&Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open File')
        openFile.triggered.connect(self.file_open)

        saveFile = QAction(QIcon('saveThing.png'), '&Save', self)
        saveFile.setShortcut("Ctrl+S")
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.file_save)

        addProcess = QAction(QIcon('newThing.png'),'&NewProcess', self)
        addProcess.setShortcut('Ctrl+N')
        addProcess.setStatusTip('New Process')
        addProcess.triggered.connect(self.new_Process)

        comboCPU = QComboBox()
        comboCPU.addItem("FCFS")
        comboCPU.addItem("SJF")
        comboCPU.addItem("ROUND ROBIN")
        comboCPU.addItem("EDF")

        comboMem = QComboBox()
        comboMem.addItem("FIFO")
        comboMem.addItem("MRU")

        linhaCPU = QLabel()
        linhaCPU.setText("Algoritm Scalonitro")

        linhaMem = QLabel()
        linhaMem.setText("Pagination Algortim")

        layoutC = QGridLayout()
        layoutC.addWidget(linhaCPU)
        layoutC.addWidget(comboCPU)

        layoutM = QGridLayout()
        layoutM.addWidget(linhaMem)
        layoutM.addWidget(comboMem)

        quantum_sp = QSpinBox()
        quantum_sp.setMinimum(1)

        override_sp = QSpinBox()

        quantum_label = QLabel()
        quantum_label.setText("Quantum Time")

        override_label = QLabel()
        override_label.setText("Override Time")

        QuantumLayout = QGridLayout()
        QuantumLayout.addWidget(quantum_label)
        QuantumLayout.addWidget(override_sp)

        OverrideLayout = QGridLayout()
        OverrideLayout.addWidget(override_label)
        OverrideLayout.addWidget(quantum_sp)

        selectC = QWidget()
        selectC.setLayout(layoutC)

        selectM = QWidget()
        selectM.setLayout(layoutM)

        Quantum = QWidget()
        Quantum.setLayout(QuantumLayout)

        Override = QWidget()
        Override.setLayout(OverrideLayout)

        self.toolbar = self.addToolBar('Process')
        self.toolbar.addAction(addProcess)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(selectC)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(selectM)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(Quantum)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(Override)



        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)




    def file_save(self):
        name = QFileDialog.getSaveFileName(self, 'Save File')
        if name[0]:

            # def __init__(self, id, start, execution_time, deadline = 0, io=None, need_io=False, priority=0):
            file = open(name[0], 'w')
            with file:
                for i in self.listProcess:
                    file.write(str(i.id) + ' ' + str(i.start) + ' ' + str(i.execution_time) + ' ' + str(i.deadline) + ' ' +
                               "None" + ' ' + str(i.need_io) + ' ' + str(i.priority) + '\n')



    def file_open(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if fname[0]:
            f = open(fname[0], 'r')
            with f:
                data = f.read().split('\n')
                index = 0 # def __init__(self, id, start, execution_time, deadline = 0, io=None, need_io=False, priority=0):
                for a in data:
                    if a == '':
                        break
                    i = a.split(' ')
                    print(i)
                    processo = Process(int(i[0]), int(i[1]), int(i[2]), int(i[3]))
                    if i[5] == "True":
                        processo.need_io = True
                    else:
                        processo.need_io = False
                    processo.priority = int(i[6])
                    self.listProcess.append(processo)
            self.printProcesses()




    def new_Process(self):
        self.processAux = Window_Process(self.idProcess, self.process)
        self.processAux.exec_()
        self.process = self.processAux.process
        if self.process:
            self.listProcess.append(self.process)
            self.idProcess+= 1
        self.printProcesses()

    def editProcess(self):
        sender = self.sender()
        index = int(sender.text().split(' ')[1])
        self.processAux = Window_Process(index, self.process)
        self.processAux.exec_()
        process = self.processAux.process
        if process:
            self.listProcess[index - 1] = process
            self.printProcesses()

    def removeProcess(self):
        sender = self.sender()
        index = int(sender.text().split(' ')[1])
        reply = QMessageBox.question(self, 'Remove',
                                     "Are you sure to remove ? ", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            self.listProcess.pop(index - 1)
            if not self.listProcess:
                self.idProcess = 1
            self.printProcesses()

    def printProcesses(self):
        self.lista = QTabWidget()
        self.numberTab = 1
        for i in self.listProcess:
            self.janela = QWidget()
            self.lista.addTab(self.janela, "Processo " + str(i.id))
            self.janelaUi(i)
            self.numberTab += 1


        self.setCentralWidget(self.lista)


    def janelaUi(self, processo):
        layout = QFormLayout()
        linhaStart = QLabel()
        linhaStart.setText(str(processo.start))
        layout.addRow("StartTime" , linhaStart)

        linhaExec = QLabel()
        linhaExec.setText(str(processo.execution_time))
        layout.addRow("Execution Time", linhaExec)

        linhaDeadLine = QLabel()
        linhaDeadLine.setText(str(processo.deadline))
        layout.addRow("DeadLine Time", linhaDeadLine)

        linhaPriority = QLabel()
        linhaPriority.setText(str(processo.priority))
        layout.addRow("Priority", linhaPriority)

        btnEdit = QPushButton('Edit ' + str(self.numberTab) + ' ' + '° Process', self.janela)
        btnRemove = QPushButton('Remove ' + str(self.numberTab) + ' ' + '° Process', self.janela)

        btnEdit.clicked.connect(self.editProcess)
        btnRemove.clicked.connect(self.removeProcess)

        layout.addRow(btnEdit)
        layout.addRow(btnRemove)

        self.lista.setTabText(self.numberTab, "Process " + str(processo.id))
        self.janela.setLayout(layout)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_Window()
    sys.exit(app.exec_())