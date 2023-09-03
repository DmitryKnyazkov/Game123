from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QFont
from random import randint
import time
import json


class MyParentWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.list_matches = []
        self.queue = []

        self.lives = 5

        self.screen_ = 0

        self.start_count = "60"

        self.visit_in_change_button = 0

        self.dict_color = {"1": "white", "2": "green", "3": "orange", "4": "red", "5": "blue", "6": "violet",
                           "7": "yellow"}

        self.child_window_GameOver = ChildWindowGameOver()

        self.initUI_initSignal()
        self.InitThreads()
        self.answer()

    def initUI_initSignal(self) -> None:
        self.resize(290, 290)
        self.setWindowTitle("Игра 123")
        # self.setStyleSheet("background-color: purple")
        self.setStyleSheet("background-color: #00ff7f")
        self.gridlayout = QtWidgets.QGridLayout()
        self.hBoxLayout1 = QtWidgets.QHBoxLayout()
        self.hBoxLayout2 = QtWidgets.QHBoxLayout()
        self.hBoxLayout3 = QtWidgets.QHBoxLayout()
        self.hBoxLayout4 = QtWidgets.QHBoxLayout()

        self.vBoxLayout = QtWidgets.QVBoxLayout()

        self.lable11 = QtWidgets.QLabel("Количество жизней: ")
        self.lable12 = QtWidgets.QLabel(str(self.lives))

        self.lable21 = QtWidgets.QLabel("Время до конца игры: ")
        self.lable22 = QtWidgets.QLabel(self.start_count)

        self.lable31 = QtWidgets.QLabel("Счет: ")
        self.lable32 = QtWidgets.QLabel("0")

        self.hBoxLayout1.addWidget(self.lable11)
        self.hBoxLayout1.addWidget(self.lable12)

        self.hBoxLayout2.addWidget(self.lable21)
        self.hBoxLayout2.addWidget(self.lable22)

        self.hBoxLayout3.addWidget(self.lable31)
        self.hBoxLayout3.addWidget(self.lable32)

        self.hBoxLayout4.addLayout(self.gridlayout)

        self.vBoxLayout.addLayout(self.hBoxLayout1)
        self.vBoxLayout.addLayout(self.hBoxLayout2)
        self.vBoxLayout.addLayout(self.hBoxLayout3)
        self.vBoxLayout.addLayout(self.hBoxLayout4)

        for i in range(5):
            for j in range(5):
                self.pushbutton = QtWidgets.QPushButton(str(randint(1, 7)))
                self.pushbutton.setMaximumSize(100, 100)
                self.pushbutton.setMinimumSize(50, 50)
                numer_butten = self.pushbutton.text()
                eval(f'self.pushbutton.setStyleSheet("background-color: {self.dict_color[numer_butten]}")')

                self.gridlayout.addWidget(self.pushbutton, i, j)
                self.pushbutton.clicked.connect(self.click_counter)

                self.pushbutton.setObjectName(f'pushbutton{i}{j}')

        self.setLayout(self.vBoxLayout)

    def click_counter(self):
        widget_click = self.sender()

        self.runLongTimer()
        self.thread.progress.connect(self.reportProgress)
        self.thread.finished.connect(self.thread.quit)

        value = int(widget_click.text())
        if value < 7:
            widget_click.setText(str(value + 1))

        self.numer_butten = widget_click.text()
        eval(f'widget_click.setStyleSheet("background-color: {self.dict_color[self.numer_butten]}")')
        self.position_widgets_at_gridlayout(widget_click)
        if self.visit_in_change_button == 1:
            self.miss_counter(+1)
        else:
            self.miss_counter(-1)
        self.visit_in_change_button = 0

    def position_widgets_at_gridlayout(self, widget_click):
        for i in range(self.gridlayout.rowCount()):
            for j in range(self.gridlayout.columnCount()):
                if widget_click == self.gridlayout.itemAtPosition(i, j).widget():
                    self.check_widgets(i, j)
                    break

    def check_widgets(self, i, j):
        max_col = self.gridlayout.columnCount()
        max_row = self.gridlayout.rowCount()
        cur_w = self.gridlayout.itemAtPosition(i, j).widget().text()

        if self.gridlayout.itemAtPosition(i, j).widget() not in self.list_matches:
            self.list_matches.append(self.gridlayout.itemAtPosition(i, j).widget())
        # Проверяем соседа справа
        if j < max_col - 1:
            neighbour = self.gridlayout.itemAtPosition(i, j + 1).widget()
            if neighbour not in self.list_matches:
                if cur_w == neighbour.text():
                    self.queue.append(neighbour)
        # Проверяем соседа слева
        if 0 < j:
            neighbour = self.gridlayout.itemAtPosition(i, j - 1).widget()
            if neighbour not in self.list_matches:
                if cur_w == neighbour.text():
                    self.queue.append(neighbour)
        # Проверяем соседа сверху
        if 0 < i:
            neighbour = self.gridlayout.itemAtPosition(i - 1, j).widget()
            if neighbour not in self.list_matches:
                if cur_w == neighbour.text():
                    self.queue.append(neighbour)
        # Проверяем соседа снизу
        if i < max_row - 1:
            neighbour = self.gridlayout.itemAtPosition(i + 1, j).widget()
            if neighbour not in self.list_matches:
                if cur_w == neighbour.text():
                    self.queue.append(neighbour)


        if len(self.queue) != 0:
            self.position_widgets_at_gridlayout(self.queue.pop())

        if len(self.list_matches) > 2:
            self.change_button()

        self.list_matches = []

    def miss_counter(self, summand_):
        self.lives += summand_
        if self.lives > 5:
            self.lives = 5
        if self.lives < 1:
            self.game_over()

        self.lable12.setText(str(self.lives))

    def change_button(self):
        self.button_switch(False)
        self.screen_ += len(self.list_matches)
        for button in self.list_matches:
            button.setText("*")
            button.setStyleSheet('background-color: #ff0c39}')
            QtWidgets.QApplication.processEvents()
            time.sleep(0.05)
        time.sleep(0.5)
        for button in self.list_matches:
            button.setStyleSheet('QPushButton {background-color: #ff6589}')
            QtWidgets.QApplication.processEvents()
            time.sleep(0.05)
        time.sleep(0.05)
        for button in self.list_matches:
            button.setText(str(randint(1, 7)))
            self.numer_butten_ = button.text()
            eval(f'button.setStyleSheet("background-color: {self.dict_color[self.numer_butten_]}")')
            QtWidgets.QApplication.processEvents()
            time.sleep(0.05)

        self.lable32.setText(str(self.screen_))
        self.list_matches = []
        self.visit_in_change_button = 1
        self.button_switch(True)
        if int(self.lable22.text()) < 1:
            self.game_over()

    def button_switch(self, value):
        for i in range(self.gridlayout.rowCount()):
            for j in range(self.gridlayout.columnCount()):
                self.gridlayout.itemAtPosition(i, j).widget().setEnabled(value)

    def game_over(self):
        self.button_switch(False)

        self.child_window_GameOver.show()

        self.thread.stopThraid(False)

        # self.child_window_GameOver.screen_signal.emit(self.lable32.text())
        self.child_window_GameOver.set_text(self.screen_)

    def InitThreads(self):
        self.thread = Worker()

    def runLongTimer(self):
        self.thread.set_count(self.start_count)
        self.thread.start()
        # self.thread.stop_thread.emit(True)

    def reportProgress(self, progress) -> None:
        """
        Приём данных из потока и обработка их в основном цикле приложения

        :param progress: прогресс выполнения функции в потоке
        :return: None
        """
        if progress == 0:
            self.game_over()

        self.lable22.setText(str(progress))

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        Действия при закрытии программы

        :param event: QtGui.QCloseEvent
        :return: None
        """

        self.child_window_GameOver.close()

    def answer(self):
        self.child_window_GameOver.answer.connect(self.answer_processing)

    def answer_processing(self, answer):
        if answer == "yes":
            self.child_window_GameOver.close()
            self.button_switch(True)
            self.new_field()
        if answer == "no":
            self.child_window_GameOver.close()
            self.close()

    def new_field(self):
        self.screen_ = 0
        self.lives = 5
        self.lable32.setText(str(self.screen_))
        self.lable12.setText(str(self.lives))
        self.lable22.setText(self.start_count)
        self.thread.stopThraid(True)

        for i in range(self.gridlayout.rowCount()):
            for j in range(self.gridlayout.columnCount()):
                self.gridlayout.itemAtPosition(i, j).widget().setText(str(randint(1, 7)))
                numer_butten = self.gridlayout.itemAtPosition(i, j).widget().text()
                # eval(self.gridlayout.itemAtPosition(i, j).widget().setStyleSheet((f"background-color: {self.dict_color[numer_butten]}")))
                self.gridlayout.itemAtPosition(i, j).widget().setStyleSheet(
                    (f"background-color: {self.dict_color[numer_butten]}"))


class Worker(QtCore.QThread):
    progress = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.stop_thread = True
        self.count = ""

    def set_count(self, value):
        self.count = value

    def stopThraid(self, value):
        self.stop_thread = value

    def run(self) -> None:

        for i in reversed(range(int(self.count))):
            time.sleep(1)
            if self.stop_thread is True:
                self.progress.emit(i)
            else:
                break


class ChildWindowGameOver(QtWidgets.QDialog):
    answer = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()
        self.initSignal()

    def initUI(self):
        self.setWindowTitle("Вопрос игры 123")
        self.resize(270, 150)
        self.setStyleSheet("background-color: #00ff7f")
        # self.setStyleSheet("background-color: #ffff00")

        self.lable1 = QtWidgets.QLabel()
        self.lable1.setText("ИГРА ЗАКОНЧЕНА!!!")

        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        self.lable1.setFont(font)

        self.lable1.setStyleSheet(f"color: red")

        self.lable2 = QtWidgets.QLabel()
        self.lable3 = QtWidgets.QLabel()
        self.lable4 = QtWidgets.QLabel("Хотите еще сыграть?")
        self.button51 = QtWidgets.QPushButton("ДА")
        self.button52 = QtWidgets.QPushButton("НЕТ")
        self.qhboxLayout = QtWidgets.QHBoxLayout()

        self.qhboxLayout.addWidget(self.button51)
        self.qhboxLayout.addWidget(self.button52)

        self.qvboxLayout = QtWidgets.QVBoxLayout()
        self.qvboxLayout.addWidget(self.lable1)
        self.qvboxLayout.addWidget(self.lable2)
        self.qvboxLayout.addWidget(self.lable3)
        self.qvboxLayout.addWidget(self.lable4)
        self.qvboxLayout.addLayout(self.qhboxLayout)

        self.setLayout(self.qvboxLayout)

    def initSignal(self):

        self.button51.clicked.connect(lambda: self.answer.emit('yes'))
        self.button52.clicked.connect(lambda: self.answer.emit('no'))

    def set_text(self, text):
        self.lable2.setText(f"Набронных очков: {text}")
        self.save_screen(text)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        Действия при закрытии программы

        :param event: QtGui.QCloseEvent
        :return: None
        """

        self.answer.emit('yes')

    def save_screen(self, value):
        filename = "SCREEN.json"

        with open(filename, "r", encoding="utf-8") as f:
            current_record = json.load(f)

        if value > current_record:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(value, f)
                self.lable3.setText(f"Рекорд игры: {value}")

        else:
            self.lable3.setText(f"Рекорд игры: {current_record}")


if __name__ == "__main__":
    app = QtWidgets.QApplication()  # Создаем  объект приложения

    My_Parent_Window = MyParentWindow()  # Создаём объект окна
    My_Parent_Window.show()  # Показываем окно

    app.exec()
