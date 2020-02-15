import os
import sys
import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel



class Example(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)
        self.image = QLabel(self)
        self.image.move(20, 0)
        self.image.resize(500, 400)
        self.lineEdit.setText('0')
        self.lineEdit_2.setText('0')

        self.z = 5
        self.showMap()
        self.pushButton.clicked.connect(self.showMap)

    def showMap(self):
        self.coords = self.lineEdit.text() + ',' + self.lineEdit_2.text()
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def getImage(self):
        map_request = f'http://static-maps.yandex.ru/1.x/?ll={self.coords}&z={self.z}&l=map&size=500,350'
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
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def keyPressEvent(self, e):
        key = e.key()
        if key == 16777238:
            if self.z <= 16:
                self.z += 1
                self.showMap()
        elif key == 16777239:
            if self.z >= 1:
                self.z -= 1
                self.showMap()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
