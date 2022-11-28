from PyQt5 import QtCore, QtWidgets, QtGui, uic
import time
import random
import sys


from main import CWW


class Progress(QtCore.QThread):
    my_signal = QtCore.pyqtSignal(list)

    def run(self):
        time.sleep(0.5)
        for i in range(0, 102):
            self.my_signal.emit(['progress_increment', i])
            time.sleep(0.04)


class Data(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('UI/loading.ui', self)

        self.handler = Progress()
        self.handler.my_signal.connect(self.signal_handler)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.progressBar.setValue(0)
        self.handler.start()

        self.movie = QtGui.QMovie('gif/logo.gif')
        self.movie.setScaledSize(QtCore.QSize(500, 600))
        self.giflabel.move(40, 35)
        self.giflabel.setMovie(self.movie)
        self.movie.start()

    def signal_handler(self, value):
        data = ['Загружаю информацию о погоде', 'Проверяю базы данных', 'Настраиваю интерфейс',
                'Создаю активную сессию']

        if value[1] == 101:
            time.sleep(0.2)
            self.new_window = CWW()
            self.movie.stop()
            self.hide()
            self.new_window.show()
        elif value[1] == 100:
            self.label.setText('Процесс успешно завершён')

            return
        elif value[0] == 'progress_increment':
            current_value = self.progressBar.value()
            self.progressBar.setValue(current_value + 1)

            if value[1] % 25 == 0:
                data1 = random.choice(data)
                self.label.setText(data1)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Data()
    ex.show()
    sys.exit(app.exec_())
