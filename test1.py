import os
import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.l = 'map'
        self.z = 1
        self.ll = [37.530887, 55.70311]
        self.initUI()
        self.getImage(self.z, self.ll, self.l)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)

    def getImage(self, z, ll, l):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={ll[0]},{ll[1]}&l={l}&z={z}"
        response = requests.get(map_request)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
        os.remove('map.png')

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def keyPressEvent(self, e):
        if e.key() == 16777238:
            if self.z < 17:
                self.z += 1
                self.getImage(self.z, self.ll, self.l)
        elif e.key() == 16777239:
            if self.z > 1:
                self.z -= 1
                self.getImage(self.z, self.ll, self.l)
        elif e.key() == Qt.Key_Up:
            self.ll[1] += 0.5
            self.getImage(self.z, self.ll, self.l)
        elif e.key() == Qt.Key_Down:
            self.ll[1] -= 0.5
            self.getImage(self.z, self.ll, self.l)
        elif e.key() == Qt.Key_Left:
            self.ll[0] -= 0.5
            self.getImage(self.z, self.ll, self.l)
        elif e.key() == Qt.Key_Right:
            self.ll[0] += 0.5
            self.getImage(self.z, self.ll, self.l)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
# https://github.com/tofu18/YandexMapsApi
