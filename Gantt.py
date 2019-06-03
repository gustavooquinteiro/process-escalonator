import sys
from PyQt5 import QtTest
from PyQt5.QtCore import Qt, QTime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QIcon, QBrush, QPalette
from escalonator import Escalonator
import time

class Window_Gantt(QWidget):
    def __init__(self, n, cpu, escalonator, io, processes, SOWindow):
        super().__init__()
        self.timer = QTime()
        self.SO = SOWindow
        self.tickClock = 0
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(processes))
        self.tableWidget.setColumnCount(1)
        self.tableMem = QTableWidget()
        self.tableMem.setRowCount(50)
        self.tableMem.setColumnCount(1)
        self.tableMem.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.dicionary = {}
        index = 0
        for i in processes:
            self.dicionary[i.id] = index
            index+=1
        self.setWindowTitle("Gantt Processes")
        self.layout = QVBoxLayout()
        self.tickRun = QPushButton( "Tick", self)
        self.tickRun.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout2 = QHBoxLayout()
        self.tickRun.clicked.connect(self.tick)
        self.ticksQuant = QSpinBox()
        self.ticksQuant.setMinimum(1)
        self.ticksQuant.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.AutoTickQuant = QSpinBox()
        self.AutoTickQuant.setMinimum(1)
        self.AutoTickQuant.setMaximum(2000)
        self.AutoTickQuant.setValue(1000)
        self.AutoTickQuant.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.checkAutoTick = QCheckBox("Auto Tick")
        self.checkAutoTick.setChecked(False)
        self.checkAutoTick.stateChanged.connect(self.autoTick)
        self.checkAutoTick.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.Info = QLabel("Algoritmo CPU: " + self.SO.type + "\n Algoritmo Mem: " + self.SO.typeMMU +  "\n Quantum: " + str(self.SO.quantum) + "\n Sobrecarga: "
                           + str(self.SO.override))
        self.Info.setStyleSheet("color: red;")
        self.Info.setAlignment(Qt.AlignCenter)

        self.layout3 = QVBoxLayout()
        labelCheck =  QLabel("Mark to Run Automatic")
        self.layout3.addWidget(labelCheck)
        self.layout3.addWidget(self.checkAutoTick)
        C = QWidget()
        C.setLayout(self.layout3)
        self.layout2.addWidget(C)

        self.layout3 = QVBoxLayout()
        labelCheck = QLabel("Time in MSec to AutoRun")
        self.layout3.addWidget(labelCheck)
        self.layout3.addWidget(self.AutoTickQuant)
        D = QWidget()
        D.setLayout(self.layout3)
        self.layout2.addWidget(D)

        self.layout3 = QVBoxLayout()
        self.labelCheck1 = QLabel("Click to Run " + str(self.ticksQuant.value()) + " ticks")
        self.layout3.addWidget(self.labelCheck1)
        self.layout3.addWidget(self.tickRun)
        E = QWidget()
        E.setLayout(self.layout3)
        self.layout2.addWidget(E)

        self.layout3 = QVBoxLayout()
        labelCheck = QLabel("Ticks to Run")
        self.layout3.addWidget(labelCheck)
        self.layout3.addWidget(self.ticksQuant)
        self.ticksQuant.valueChanged.connect(self.ticksQuantUpdate)
        F = QWidget()
        F.setLayout(self.layout3)
        self.layout2.addWidget(F)

        A = QWidget()
        A.setLayout(self.layout2)
        self.layout.addWidget(self.Info)
        self.layout.addWidget(A)
        layoutTables = QHBoxLayout()
        layoutTables.addWidget(self.tableWidget)
        layoutTables.addWidget(self.tableMem)
        B = QWidget()
        B.setLayout(layoutTables)
        self.layout.addWidget(B)
        self.LastLabel = QLabel("Running")
        self.layout.addWidget(self.LastLabel)
        self.setGeometry(300, 300, 1000, 600)
        self.setLayout(self.layout)
        self.setWindowIcon(QIcon('edit-image.png'))
        self.show()

        self.cpu = cpu
        self.escalonator = escalonator
        self.io = io
        self.n = n

    def ticksQuantUpdate(self):
        self.labelCheck1.setText("Click to Run " + str(self.ticksQuant.value()) + " ticks")



    def updategantt(self, tick, escalonator, io, cpu):
        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.setItem(i, tick, QTableWidgetItem())
            self.tableWidget.item(i, tick,).setBackground(Qt.gray)
            self.tableWidget.item(i, tick).setFlags(Qt.NoItemFlags)

        for i in escalonator.ready_queue:
            self.tableWidget.setItem(self.dicionary[i.id], tick, QTableWidgetItem())
            self.tableWidget.item(self.dicionary[i.id], tick).setBackground(Qt.yellow)
            self.tableWidget.item(self.dicionary[i.id], tick).setFlags(Qt.NoItemFlags)
        for i in io.queue:
            self.tableWidget.setItem(self.dicionary[i.id], tick, QTableWidgetItem())
            self.tableWidget.item(self.dicionary[i.id], tick).setBackground(Qt.red)
            self.tableWidget.item(self.dicionary[i.id], tick).setFlags(Qt.NoItemFlags)
        #print(cpu.state)
        if cpu.state == "Executando" or cpu.state == "PreSobrecarga" or cpu.state == "Pronto" :
            self.tableWidget.setItem(self.dicionary[cpu.process.id], tick, QTableWidgetItem())
            self.tableWidget.item(self.dicionary[cpu.process.id], tick).setBackground(Qt.green)
            self.tableWidget.item(self.dicionary[cpu.process.id], tick).setFlags(Qt.NoItemFlags)
        if cpu.state == "PosSobrecarga"  or cpu.state == "Sobrecarga":
            self.tableWidget.setItem(self.dicionary[cpu.process.id], tick, QTableWidgetItem())
            self.tableWidget.item(self.dicionary[cpu.process.id], tick).setBackground(QColor(255,165,0))
            self.tableWidget.item(self.dicionary[cpu.process.id], tick).setFlags(Qt.NoItemFlags)
        if self.n != len(self.cpu.concluded_process_time):
            self.tableWidget.setColumnCount(self.tableWidget.columnCount()+1)

    def updateMem(self):
        index = 0
        for i in self.cpu.mmu.vm.mem_ram.queue:
            if self.cpu.mmu.vm.mem_ram.isAllocated(i):
                self.tableMem.setItem(index, 0, QTableWidgetItem())
                self.tableMem.item(index, 0).setBackground(QColor(30,144,255))
                self.tableMem.item(index, 0).setForeground(Qt.yellow)
                self.tableMem.item(index, 0).setTextAlignment(Qt.AlignHCenter)
                self.tableMem.item(index, 0).setText(str(i.num))
                self.tableMem.item(index, 0).setFlags(Qt.NoItemFlags)
            else:
                self.tableMem.setItem(index, 0, QTableWidgetItem())
                self.tableMem.item(index, 0).setBackground(Qt.gray)
                self.tableMem.item(index, 0).setFlags(Qt.NoItemFlags)
            index+=1



    def tick(self):
        if self.n == len(self.cpu.concluded_process_time):
            if self.ticksQuant.value() > 1:
                self.ticksQuant.setValue(1)
            self.checkAutoTick.setChecked(False)
            turnaround = sum(self.cpu.concluded_process_time) / self.n
            self.LastLabel.setText("TURNAROUND: " + str(turnaround))
            text = " Algoritmo CPU: " + self.SO.type + "\n Algoritmo Mem: " + self.SO.typeMMU +  "\n Quantum: " + str(self.SO.quantum) + "\n Sobrecarga: " + str(self.SO.override) + "\n TURNAROUND: "+ str(turnaround)
            reply = QMessageBox.information(self, 'FINISHED', text, QMessageBox.Ok)
            #print("JA FOI")
            return
        self.escalonator.nextProcess()
        self.io.wait_for_resource(self.cpu)
        self.cpu.runClock()

        #print('Prontos: ', end='')
        #for proc in self.escalonator.ready_queue:
            #print(proc.id, end=' ')
        #print()
        #print('Bloqueados: ', end='')
        #for proc in self.io.queue:
            #print(proc.id, end=' ')
        #print()

        # print(cpu.state)
        self.updategantt(self.cpu.clock, self.escalonator, self.io, self.cpu)
        self.updateMem()
        self.cpu.clock += 1
        self.tickClock = self.cpu.clock

        if self.ticksQuant.value()>1:
            self.ticksQuant.setValue(self.ticksQuant.value()-1)
            self.tick()

    def autoTick(self):
        while self.checkAutoTick.isChecked():
            self.tick()
            QtTest.QTest.qWait(self.AutoTickQuant.value())


    def closeEvent(self, e):
        self.SO.file_open(True)
        self.SO.show()
        self.close()
