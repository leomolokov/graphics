from PyQt5.QtWidgets import QApplication

from mainwin.mainwin import MainWindow
from data.mydata import MyData

import sys

def main():
    data = MyData()
    data.read('scene.txt')
    app = QApplication(sys.argv)
    main = MainWindow(data)
    main.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()