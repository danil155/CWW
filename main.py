from PyQt5 import uic, QtGui, Qt, QtCore
from PyQt5.QtCore import Qt, QTime, QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
from PIL import Image

import own1
import base_main
import base_append


form_2, base_2 = uic.loadUiType('UI/db_append.ui')


class CWW(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.city_id = 511196
        self.initUI()

    def initUI(self):
        uic.loadUi('UI/main.ui', self)
        self.setFixedSize(1196, 702)
        self.precipitation()

        self.temp.setFont(QtGui.QFont("Bahnschrift SemiBold SemiConden", 72))
        self.temp.setText(str(own1.temp_now(self.city_id)))

        self.btn_append.clicked.connect(self.append)
        self.btn_selection.clicked.connect(self.selection)
        self.btn_exit.clicked.connect(self.exit)

        self.gifs()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.time)
        self.timer.start(1000)

    # Окно с подобранной одеждой
    def selection(self):
        self.timer.stop()
        uic.loadUi('UI/main_2.ui', self)
        self.show()

        self.btn_home.setIcon(QtGui.QIcon('icon/home.png'))
        self.btn_home.setIconSize(QtCore.QSize(40, 40))
        self.btn_home.clicked.connect(self.initUI)
        self.text_weather.setText(str(own1.temp_now(self.city_id)))
        self.text_weather.setFont(QtGui.QFont("Bahnschrift SemiBold SemiConden", 16))
        self.btn_append.clicked.connect(self.append)
        self.btn_selection.clicked.connect(self.selection)
        self.btn_exit.clicked.connect(self.exit)
        self.models()

        self.gifs()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.time)
        self.timer.start(1000)

        if self.path1 != '':
            img = Image.open(self.path1)
            img.thumbnail(size=(50, 50))
            img.save('icon2/precipitation.png')
            self.qpixmap2 = QtGui.QPixmap('icon2/precipitation.png')
            self.imglabel.setPixmap(self.qpixmap2)

        self.line_warning1.setText(own1.warning(self.city_id)[0])
        self.line_warning2.setText(own1.warning(self.city_id)[1])
        own1.protection(self.city_id)

        data = base_main.main(self.city_id)
        self.lineEdit1.setText(data[0])
        self.lineEdit2.setText(data[1])
        self.lineEdit2_2.setText(data[2])
        self.lineEdit2_3.setText(data[3])
        self.lineEdit3.setText(data[4])
        self.lineEdit3_2.setText(data[5])

    # Вывод значка осадков
    def precipitation(self):
        a = own1.precipitation_now(self.city_id)
        if 'небольшой дождь' in a:
            self.path1 = 'icon/little_rain.png'
            self.imglabel.setToolTip('Небольшой дождь')
        elif 'пасмурно' in a:
            self.path1 = 'icon/cloudy.png'
            self.imglabel.setToolTip('Пасмурно')
        elif 'небольшой снег' in a:
            self.path1 = 'icon/little_snow.png'
            self.imglabel.setToolTip('Небольшой снег')
        elif 'снег' in a:
            self.path1 = 'icon/snow.png'
            self.imglabel.setToolTip('Снег')
        elif 'облачно с прояснениями' in a:
            self.path1 = 'icon/cloudy.png'
            self.imglabel.setToolTip('Облачно с прояснениями')
        elif 'ясно' in a:
            self.path1 = 'icon/clear.png'
            self.imglabel.setToolTip('Ясно')
        elif 'небольшая облачность' in a:
            self.path1 = 'icon/partly_cloudy.png'
            self.imglabel.setToolTip('Небольшая облачность')
        elif 'переменная облачность' in a:
            self.path1 = 'icon/partly_cloudy.png'
            self.imglabel.setToolTip('Переменная облачность')
        else:
            self.path1 = ''
            self.imglabel.setToolTip('Хз чё')

        self.qpixmap = QtGui.QPixmap(self.path1)
        self.imglabel.setPixmap(self.qpixmap)

    # Часы
    def time(self):
        time = QTime.currentTime()
        self.time_edit.setText(time.toString(Qt.DefaultLocaleLongDate))
        self.time_edit.setAlignment(Qt.AlignCenter)

    # Добавление гифки сезона
    def gifs(self):
        if own1.get_seasons() == 'winter' or own1.date_now()[5:7] == '11':
            self.movie = QtGui.QMovie('gif/snow_g.gif')
        elif own1.get_seasons() == 'spring':
            self.movie = QtGui.QMovie('gif/rain_g.gif')
        elif own1.get_seasons() == 'summer':
            self.movie = QtGui.QMovie('gif/summer_g.gif')
        else:
            self.movie = QtGui.QMovie('gif/autumn_g.gif')

        self.giflabel.setMovie(self.movie)
        self.movie.start()

    # Вывод значков для одежды
    def models(self):
        self.imglabel_1.setPixmap(QtGui.QPixmap('icon/head.png'))
        self.imglabel_2.setPixmap(QtGui.QPixmap('icon/body.png'))
        self.imglabel_3.setPixmap(QtGui.QPixmap('icon/legs.png'))

    # Открытие окна с добавлением вещей
    def append(self):
        self.v = DbAppend()
        self.v.show()

    # Кнопка выход
    def exit(self):
        self.close()


class DbAppend(base_2, form_2):
    def __init__(self):
        super(base_2, self).__init__()
        uic.loadUi('UI/db_append.ui', self)
        self.initUI()
        self.setFixedSize(810, 613)

    def initUI(self):
        self.combobox_1.currentTextChanged.connect(self.list_update)
        self.btn_append.clicked.connect(self.append)

    def append(self):
        data = [self.lineEdit_1.text(), self.combobox_2.currentText(), self.combobox_1.currentText(), self.lineEdit_2.text()]
        inf = base_append.validation(data)
        if not inf[0]:
            self.lineEdit_war.setStyleSheet('''
            QLineEdit {
            border: 2px solid rgb(85, 98, 173);
            border-radius: 20px;
            border-radius: 20px;
            color: #FFF;
            padding-left: 20px;
            padding-right: 20px;
            background-color: rgb(85, 98, 173);
            color: rgb(200, 20, 20);
            }
            QLineEdit:hover {
            border: 2px solid rgb(96, 112, 197);
            }
            ''')
            self.lineEdit_war.setText(inf[1])
        else:
            base_append.append(data)
            self.close()

    def list_update(self):
        inf = base_append.update(self.combobox_1.currentText())
        self.combobox_2.clear()
        self.combobox_2.addItems(inf)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CWW()
    ex.show()

    sys.exit(app.exec_())
