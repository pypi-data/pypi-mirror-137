from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *

import sys

app = QApplication(sys.argv)
wind = QWidget()

names = {}
lsprite_base = {}

class oilwin():
    def __init__(self, res_x, res_y, title, resiz, icon) -> None:
        self.res_x = res_x
        self.res_y = res_y
        self.title = title
        self.resize = resiz
        self.icon = icon
        
        if self.icon != None:
            wind.setWindowIcon(QIcon(self.icon))

        if self.title != '':
            wind.setWindowTitle(self.title)
        elif self.title == '':
            wind.setWindowTitle('oilukla window')

        if self.resize == True:
            wind.setFixedSize(self.res_x, self.res_y)

        wind.resize(self.res_x, self.res_y)

    def resize_win(self, nres_x, nres_y):
        global wind
        if self.resize == False:
            wind.resize(nres_x, nres_y)
        elif self.resize == True:
            wind.setFixedSize(nres_x, nres_y)

    def rename_win(self, ntitle):
        global wind
        wind.setWindowTitle(ntitle)

    def ena_window(self):
        sys.exit(app.exec())

    def draw_obj(self):
        wind.show()


class oilentity(): #, img_way, res_x, res_y, phys, add_script
    def __init__(self, sprite, res_x, res_y) -> None:
        self.sprite = sprite
        self.res_x = res_x
        self.res_y = res_y

        self.x = 0
        self.y = 0
        self.gravity = -9.81
        self.llabel = QLabel(wind)

    def add_object(self):
        tsprite = QPixmap(self.sprite)

        self.llabel.setPixmap(tsprite)
        self.llabel.move(self.x, self.y)
        self.llabel.resize(self.res_x, self.res_y)

        print(self.llabel)
        print(tsprite)

    def transform(self):
        self.llabel.move(self.x, self.y)
