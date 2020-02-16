import os
import sys
import requests
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit
from PyQt5.QtCore import Qt


class Example(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)
        self.image = QLabel(self)
        self.image.move(20, 0)
        self.image.resize(500, 400)
        self.coords = [0, 0]
        self.lineEdit.setText('0')
        self.lineEdit_2.setText('0')
        self.z = 0
        self.l = 'map'
        self.modes = {'Спутник': 'sat', 'Карта': 'map', 'Гибрид': 'sat,skl'}
        self.world_size = 256
        self.showMap()
        self.pushButton.setFocusPolicy(
            QtCore.Qt.NoFocus)  # Выключает возможность выбора виджета с помощью клавиш, чтобы keypressevent видел нажатия стрелок

        self.pushButton.clicked.connect(self.showMap)
        self.comboBox.currentTextChanged.connect(self.changeMode)

    def showMap(self):
        if self.sender() == self.pushButton:
            self.coords = [float(self.lineEdit.text()), float(self.lineEdit_2.text())]
            self.lineEdit.clearFocus()  # Убирает выделение поля ввода

        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def changeMode(self):
        self.l = self.modes[self.comboBox.currentText()]
        self.comboBox.clearFocus()
        self.showMap()

    def getImage(self):
        map_request = f'http://static-maps.yandex.ru/1.x/?ll={self.coords[0]},{self.coords[1]}&z={self.z}&l={self.l}'
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def closeEvent(self, event):
        os.remove(self.map_file)

    def keyPressEvent(self, e):

        if e.key() == 16777238:
            if self.z <= 16:
                self.z += 1
                self.world_size *= 2
                self.showMap()
        elif e.key() == 16777239:
            if self.z >= 1:
                self.z -= 1
                self.world_size /= 2
                self.showMap()
        elif e.key() == Qt.Key_Up:
            if self.z != 0:
                if self.coords[1] + 180 / self.world_size * 256 < 90:
                    self.coords[1] += 180 / self.world_size * 256
                    self.showMap()
        elif e.key() == Qt.Key_Down:
            if self.z != 0:
                if self.coords[1] - 180 / self.world_size * 256 > -90:
                    self.coords[1] -= 180 / self.world_size * 256
                    print(1)
                    self.showMap()

        elif e.key() == Qt.Key_Left:
            if self.z != 0:
                if self.coords[0] - 360 / self.world_size * 256 > -180:
                    self.coords[0] -= 360 / self.world_size * 256
                    self.showMap()
        elif e.key() == Qt.Key_Right:
            if self.coords[0] + 360 / self.world_size * 256 < 180:
                self.coords[0] += 360 / self.world_size * 256
                self.showMap()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
