import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QIcon, QBrush

class App(QWidget):
    def __init__(self):
        super().__init__()
        colG = Qt.black

        teste = QBrush(colG)
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(1)

        """self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setItem(0, 0, QTableWidgetItem())

        self.tableWidget.item(0, 0).setForeground(Qt.black)
        self.tableWidget.item(0, 0).setText("teste")
        self.tableWidget.item(0, 0).setFlags(Qt.NoItemFlags)
        self.tableWidget.setItem(0, 1, QTableWidgetItem(QIcon("saveThing.jpg"), ""))

        self.tableWidget.setItem(1, 1, QTableWidgetItem("Cell (2,2)"))
        self.tableWidget.setItem(2, 0, QTableWidgetItem("Cell (3,1)"))
        self.tableWidget.setItem(2, 1, QTableWidgetItem("Cell (3,2)"))
        self.tableWidget.setItem(3, 0, QTableWidgetItem("Cell (4,1)"))
        self.tableWidget.setItem(3, 1, QTableWidgetItem("Cell (4,2)"))
        self.tableWidget.move(0, 0)"""

        self.tableWidget.doubleClicked.connect(self.on_click)

        self.title = 'PyQt5 table - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        # Show widget
        self.show()

        for i in range(10):
            for j in range(10):
                self.tableWidget.setItem(j, i, QTableWidgetItem("fuck"))
                self.tableWidget.item(0, 0).setBackground(Qt.yellow)

    def on_click(self):
        print("\n")
        for currentQtableWidgetItem in self.tableWidget.selectedItems():
            print(currentQtableWidgetItem.row(), currentQtableWidgetItem.column(), currentQtableWidgetItem.text())

        self.tableWidget.setColumnCount(self.tableWidget.columnCount()+1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex1 = App()
    sys.exit(app.exec_())