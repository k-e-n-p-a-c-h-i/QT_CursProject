import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtGui import QImage, QPalette, QBrush, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, \
    QDialog, QMessageBox
from PyQt5.QtCore import Qt, QCoreApplication


class PhoneException(Exception):
    pass


class TypeException(Exception):
    pass


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI_files/main.ui', self)
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.new_win)
        self.records_win = Records()
        self.setFixedSize(481, 391)
        fon(self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QCoreApplication.instance().quit()

    def new_win(self):
        self.records_win.show()
        self.hide()


class Records(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI_files/2wid.ui', self)
        self.initUI()

    def initUI(self):
        self.setFixedSize(450, 490)
        fon(self)
        self.pushButton.clicked.connect(self.breac)
        self.pushButton_2.clicked.connect(self.add_record)

        self.widget = QWidget(self)
        self.vbox = QVBoxLayout(self.widget)
        self.scroll.setWidget(self.widget)
        con = sqlite3.connect('records.db')
        cur = con.cursor()
        result = cur.execute(f"""SELECT name FROM records """).fetchall()
        for elem in result:
            a = QPushButton(f'{elem[0]}')
            a.setStyleSheet('background-color: rgba(192, 192, 192, 180)')
            a.setFixedHeight(33)
            a.clicked.connect(self.inf)
            self.vbox.addWidget(a)
        con.close()

    def inf(self):
        self.inf_win = InfoWin(self.sender())
        self.inf_win.show()

    def add_record(self):
        self.win = AddRecord(self)
        self.win.show()

    def breac(self):
        self.hide()
        global form
        form.show()


class AddRecord(QDialog):
    def __init__(self, parents):
        super().__init__()
        self.parents = parents
        self.setModal(True)
        uic.loadUi('UI_files/2add_win.ui', self)
        self.setFixedSize(491, 260)
        fon(self)
        self.initUI()

    def initUI(self):
        fon(self)
        self.pushButton.clicked.connect(self.add_record)

    def add_record(self):
        try:
            con = sqlite3.connect('records.db')
            cur = con.cursor()

            name = self.lineEdit.text()
            date_of_birth = self.dateEdit.dateTime().toString('dd-MM-yyyy')
            if self.lineEdit_3.text() == "" or self.lineEdit.text() == "":
                raise PhoneException
            if not all(char.isalpha() or char.isspace() for char in self.lineEdit.text()) or not self.lineEdit_3.text().isdigit():
                raise TypeException
            phone_number = self.comboBox.currentText() + self.lineEdit_3.text()
            specialization = self.comboBox_2.currentText()
            date_of_admission = self.dateTimeEdit.text()
            cur.execute("""INSERT INTO records (name, date_of_birth,
             phone_number, specialization, date_of_admission) VALUES (?, ?, ?, ?, ?)""",
                        (name, date_of_birth, phone_number, specialization, date_of_admission))
            con.commit()
            c = QPushButton(name)
            c.setStyleSheet('background-color: rgba(192, 192, 192, 180)')
            c.setFixedHeight(33)
            c.clicked.connect(self.inf)
            self.parents.vbox.addWidget(c)
            self.close()
        except PhoneException:
            QMessageBox.critical(self, "Ошибка", "Все поля должны быть заполнены", QMessageBox.Ok)
        except TypeException:
            QMessageBox.critical(self, "Ошибка", "Введены некорректные данные", QMessageBox.Ok)

    def inf(self):
        Records.inf(self)


class InfoWin(QDialog):
    def __init__(self, but):
        super().__init__()
        self.setModal(True)
        uic.loadUi('UI_files/2inf_win.ui', self)
        self.setFixedSize(491, 260)
        fon(self)
        self.but = but
        self.name = but.text()
        con = sqlite3.connect('records.db')
        cur = con.cursor()
        self.result = cur.execute(f"""SELECT * FROM records WHERE name = '{self.name}'""").fetchall()
        con.close()
        print(self.result)
        self.initUI()

    def initUI(self):
        self.lineEdit.setText(self.result[0][1])
        self.lineEdit_2.setText(self.result[0][2])
        self.lineEdit_3.setText('+' + str(self.result[0][3]))
        self.lineEdit_4.setText(self.result[0][4])
        self.lineEdit_5.setText(self.result[0][5])
        self.pushButton.clicked.connect(self.delete)

    def delete(self):
        a = 'Вы действительно хотите удалить эту запись?'
        if QMessageBox.question(self, ' ', a, QMessageBox.Yes,
                                QMessageBox.No) == QMessageBox.Yes:
            self.but.setParent(None)
            self.close()
            con = sqlite3.connect('records.db')
            cur = con.cursor()
            cur.execute(f"DELETE FROM records WHERE name = '{self.but.text()}'")
            con.commit()


def fon(self):  # делает фон
    o_image = QImage("Picture_files/fon.png")
    s_image = o_image.scaled(self.size())
    palette = QPalette()

    palette.setBrush(QPalette.Window, QBrush(s_image))
    self.setPalette(palette)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('Picture_files/kolba.ico'))
    form = MyWidget()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
