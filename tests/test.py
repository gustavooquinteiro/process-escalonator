from PyQt5.QtWidgets import QApplication
import unittest
import sys
sys.path.append("sample")
from InterFace import Main_Window
from process import Process


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.interface = Main_Window()
        self.testfile = self.interface.test_folder / "test0.txt"
        with open(self.testfile, 'r') as target:
            lines = target.read().split('\n')
            for line in lines:
                if line == '':
                    break
                params = line.split(' ')
                processo = Process(int(params[0]), int(params[1]),
                                   int(params[2]), int(params[3]),
                                   int(params[4]), int(params[5]))
                self.interface.listProcess.append(processo)
        self.interface.quantum_sp.setValue(2)
        self.interface.override_sp.setValue(1)

    def test_RR_FIFO(self):
        self.interface.comboCPU.setCurrentText("RR")
        self.interface.comboMem.setCurrentText("FIFO")
        self.interface.run()
        self.interface.gantt.hide()
        self.interface.gantt.AutoTickQuant.setValue(1)
        self.interface.gantt.checkAutoTick.setChecked(True)
        result = round(self.interface.gantt.info["TURNAROUND"], 0)
        self.assertEqual(result, 33.0)

    def test_FCFS_FIFO(self):
        self.interface.comboCPU.setCurrentText("FCFS")
        self.interface.comboMem.setCurrentText("FIFO")
        self.interface.run()
        self.interface.gantt.hide()
        self.interface.gantt.AutoTickQuant.setValue(1)
        self.interface.gantt.checkAutoTick.setChecked(True)
        result = round(self.interface.gantt.info["TURNAROUND"], 0)
        self.assertEqual(result, 19.0)

    def test_SJF_FIFO(self):
        self.interface.comboCPU.setCurrentText("SJF")
        self.interface.comboMem.setCurrentText("FIFO")
        self.interface.run()
        self.interface.gantt.hide()
        self.interface.gantt.AutoTickQuant.setValue(1)
        self.interface.gantt.checkAutoTick.setChecked(True)
        result = round(self.interface.gantt.info["TURNAROUND"], 0)
        self.assertEqual(result, 19.0)

    def test_SPN_FIFO(self):
        self.interface.comboCPU.setCurrentText("SPN")
        self.interface.comboMem.setCurrentText("FIFO")
        self.interface.run()
        self.interface.gantt.hide()
        self.interface.gantt.AutoTickQuant.setValue(1)
        self.interface.gantt.checkAutoTick.setChecked(True)
        result = round(self.interface.gantt.info["TURNAROUND"], 0)
        self.assertEqual(result, 27.0)

    def test_EDF_FIFO(self):
        self.interface.comboCPU.setCurrentText("EDF")
        self.interface.comboMem.setCurrentText("FIFO")
        self.interface.run()
        self.interface.gantt.hide()
        self.interface.gantt.AutoTickQuant.setValue(1)
        self.interface.gantt.checkAutoTick.setChecked(True)
        result = round(self.interface.gantt.info["TURNAROUND"], 0)
        self.assertEqual(result, 33.0)

    def test_PRIO_FIFO(self):
        self.interface.comboCPU.setCurrentText("PRIO")
        self.interface.comboMem.setCurrentText("FIFO")
        self.interface.run()
        self.interface.gantt.hide()
        self.interface.gantt.AutoTickQuant.setValue(1)
        self.interface.gantt.checkAutoTick.setChecked(True)
        result = round(self.interface.gantt.info["TURNAROUND"], 0)
        self.assertEqual(result, 27.0)

    def test_MLF_FIFO(self):
        self.interface.comboCPU.setCurrentText("MLF")
        self.interface.comboMem.setCurrentText("FIFO")
        self.interface.run()
        self.interface.gantt.hide()
        self.interface.gantt.AutoTickQuant.setValue(1)
        self.interface.gantt.checkAutoTick.setChecked(True)
        result = round(self.interface.gantt.info["TURNAROUND"], 0)
        self.assertEqual(result, 33.0)

    def test_RR_LRU(self):
        self.interface.comboCPU.setCurrentText("RR")
        self.interface.comboMem.setCurrentText("LRU")
        self.interface.run()
        self.interface.gantt.hide()
        self.interface.gantt.AutoTickQuant.setValue(1)
        self.interface.gantt.checkAutoTick.setChecked(True)
        result = round(self.interface.gantt.info["TURNAROUND"], 0)
        self.assertEqual(result, 33.0)

    def test_FCFS_LRU(self):
        self.interface.comboCPU.setCurrentText("FCFS")
        self.interface.comboMem.setCurrentText("LRU")
        self.interface.run()
        self.interface.gantt.hide()
        self.interface.gantt.AutoTickQuant.setValue(1)
        self.interface.gantt.checkAutoTick.setChecked(True)
        result = round(self.interface.gantt.info["TURNAROUND"], 0)
        self.assertEqual(result, 19.0)

    def test_SJF_LRU(self):
        self.interface.comboCPU.setCurrentText("SJF")
        self.interface.comboMem.setCurrentText("LRU")
        self.interface.run()
        self.interface.gantt.hide()
        self.interface.gantt.AutoTickQuant.setValue(1)
        self.interface.gantt.checkAutoTick.setChecked(True)
        result = round(self.interface.gantt.info["TURNAROUND"], 0)
        self.assertEqual(result, 19.0)

    def test_SPN_LRU(self):
        self.interface.comboCPU.setCurrentText("SPN")
        self.interface.comboMem.setCurrentText("LRU")
        self.interface.run()
        self.interface.gantt.hide()
        self.interface.gantt.AutoTickQuant.setValue(1)
        self.interface.gantt.checkAutoTick.setChecked(True)
        result = round(self.interface.gantt.info["TURNAROUND"], 0)
        self.assertEqual(result, 27.0)

    def test_EDF_LRU(self):
        self.interface.comboCPU.setCurrentText("EDF")
        self.interface.comboMem.setCurrentText("LRU")
        self.interface.run()
        self.interface.gantt.hide()
        self.interface.gantt.AutoTickQuant.setValue(1)
        self.interface.gantt.checkAutoTick.setChecked(True)
        result = round(self.interface.gantt.info["TURNAROUND"], 0)
        self.assertEqual(result, 33.0)

    def test_PRIO_LRU(self):
        self.interface.comboCPU.setCurrentText("PRIO")
        self.interface.comboMem.setCurrentText("LRU")
        self.interface.run()
        self.interface.gantt.hide()
        self.interface.gantt.AutoTickQuant.setValue(1)
        self.interface.gantt.checkAutoTick.setChecked(True)
        result = round(self.interface.gantt.info["TURNAROUND"], 0)
        self.assertEqual(result, 27.0)

    def test_MLF_LRU(self):
        self.interface.comboCPU.setCurrentText("MLF")
        self.interface.comboMem.setCurrentText("LRU")
        self.interface.run()
        self.interface.gantt.hide()
        self.interface.gantt.AutoTickQuant.setValue(1)
        self.interface.gantt.checkAutoTick.setChecked(True)
        result = round(self.interface.gantt.info["TURNAROUND"], 0)
        self.assertEqual(result, 33.0)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(
        unittest.TestLoader().loadTestsFromTestCase(TestApp))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=3).run(suite())
