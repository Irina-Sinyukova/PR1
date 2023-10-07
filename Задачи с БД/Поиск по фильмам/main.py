import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('widget.ui', self)
        self.params = {"Год выпуска": "year", "Название": "title", "Продолжительность": "duration"}
        self.comboBox.addItems(list(self.params.keys()))
        self.con = sqlite3.connect("films_db.sqlite")
        self.pushButton.clicked.connect(self.select)

    def select(self):
        try:
            req = "SELECT * FROM films WHERE {} = {}".format(self.params.get(self.comboBox.currentText()),
                                                             self.lineEdit.text())
            cur = self.con.cursor()
            result = cur.execute(req).fetchone()
            if not result:
                self.errorLabel.setText("Ничего не найдено")
                return
            self.idEdit.setText(str(result[0]))
            self.titleEdit.setText(result[1])
            self.yearEdit.setText(str(result[2]))
            req2 = "SELECT title FROM genres WHERE id = {}".format(str(result[3]))
            result2 = cur.execute(req2).fetchone()
            self.genreEdit.setText(result2[0])
            self.durationEdit.setText(str(result[4]))
        except sqlite3.OperationalError:
            self.errorLabel.setText("Неправильный запрос")


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
