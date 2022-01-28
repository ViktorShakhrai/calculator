import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QFontDatabase
from typing import Union, Optional
from operator import add, sub, mul, truediv

from calculator import Ui_MainWindow

operations = {
    '+': add,
    '−': sub,
    '×': mul,
    '/': truediv
}


class Calculator(QMainWindow):
    def __init__(self):
        super(Calculator, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        QFontDatabase.addApplicationFont("fonts/Rubik-Regular.ttf")

        # digits
        self.ui.btn_0.clicked.connect(self.add_digit)
        self.ui.btn_1.clicked.connect(self.add_digit)
        self.ui.btn_2.clicked.connect(self.add_digit)
        self.ui.btn_3.clicked.connect(self.add_digit)
        self.ui.btn_4.clicked.connect(self.add_digit)
        self.ui.btn_5.clicked.connect(self.add_digit)
        self.ui.btn_6.clicked.connect(self.add_digit)
        self.ui.btn_7.clicked.connect(self.add_digit)
        self.ui.btn_8.clicked.connect(self.add_digit)
        self.ui.btn_9.clicked.connect(self.add_digit)

        # actions
        self.ui.btn_clear.clicked.connect(self.clear_all)
        self.ui.btn_ce.clicked.connect(self.clear_entry)
        self.ui.btn_point.clicked.connect(self.add_point)
        # math
        self.ui.btn_calc.clicked.connect(self.calculate)
        self.ui.btn_add.clicked.connect(self.math_operation)
        self.ui.btn_.clicked.connect(self.math_operation)
        self.ui.btn_mul.clicked.connect(self.math_operation)
        self.ui.btn_div.clicked.connect(self.math_operation)

    def add_digit(self):
        # Метод sender() возвращает Qt объект, который посылает сигнал.
        btn = self.sender()

        # Создадим кортеж с именами кнопок-цифр.
        digit_buttons = ('btn_0', 'btn_1', 'btn_2', 'btn_3',
                         'btn_4', 'btn_5', 'btn_6', 'btn_7',
                         'btn_8', 'btn_9',)

        # По дефолту в поле всегда стоит 0. В этом случае,
        # если нажимается кнопка с цифрой, текст поля заменяется на эту цифру.
        # Получается, что при нажатии на 0 ничего не будет происходить.

        if btn.objectName() in digit_buttons:
            if self.ui.le_entry.text() == '0':
                self.ui.le_entry.setText(btn.text())
            else:
                # Если же в поле не 0, то просто добавляем текст нажатой цифры в строку поля.
                self.ui.le_entry.setText(self.ui.le_entry.text() + btn.text())

    def clear_all(self) -> None:
        self.ui.le_entry.setText('0')
        self.ui.lbl_temp.clear()

    def clear_entry(self) -> None:
        self.ui.le_entry.setText('0')

    def add_point(self) -> None:
        # Логика проста. Если точки нет в поле, значит добавляем.
        if '.' not in self.ui.le_entry.text():
            self.ui.le_entry.setText(self.ui.le_entry.text() + '.')

    def add_temp(self) -> None:
        btn = self.sender()
        entry = self.remove_trailing_zeros(self.ui.le_entry.text())
        # Для начала нам нужно убедиться, что в лейбле нет текста. Затем ставим во временное выражение число из поля ввода + текст кнопки btn.
        if not self.ui.lbl_temp.text() or self.get_math_sign() == '=':
            self.ui.lbl_temp.setText(self.ui.le_entry.text() + f"{btn.text()}")
            # Еще нужно очистить поле ввода.
            self.ui.le_entry.setText('0')

    @staticmethod
    def remove_trailing_zeros(num: str) -> str:
        # Введем переменную n, которая приводит аргумент сначала к типу float, потом к string
        n = str(float(num))
        # Приведение к float обрезает нули, но не все. В конце остается .0.
        # Мы будем возвращать срез строки без двух последних символов, если они равны .0, иначе будем возвращать просто n.
        return n[:-2] if n[-2:] == '.0' else n

    def get_entry_num(self) -> Union[int, float]:
        # Запишем в переменную текст поля, уберем потенциальную точку с помощью strip().
        entry = self.ui.le_entry.text().strip('.')
        # Возвращаем float, если точка есть в переменной, иначе возвращаем int
        return float(entry) if '.' in entry else int(entry)

    def get_temp_num(self) -> Union[int, float, None]:
        '''Получаем число из Label'''
        # Если в лейбле есть текст, получаем его, разделяем по пробелам и берем первый элемент, то есть число.
        if self.ui.lbl_temp.text():
            temp = self.ui.lbl_temp.text().strip(".").split()[0]
            return float(temp) if '.' in temp else int(temp)

    def get_math_sign(self) -> Optional[str]:
        '''Получаем знак из Label'''
        if self.ui.lbl_temp.text():
            return self.ui.lbl_temp.text().strip('.').split()[-1]

    def calculate(self) -> Optional[str]:
        entry = self.ui.le_entry.text()
        temp = self.ui.lbl_temp.text()
        if temp:
            result = self.remove_trailing_zeros(
                str(operations[self.get_math_sign()](self.get_temp_num(), self.get_entry_num())))
            self.ui.lbl_temp.setText(temp + self.remove_trailing_zeros(entry) + ' =')
            self.ui.le_entry.setText(result)
            return result

    def math_operation(self) -> None:
        temp = self.ui.lbl_temp.text()
        btn = self.sender()

        if not temp:
            self.add_temp()
        else:
            if self.get_math_sign() != btn.text():
                if self.get_math_sign() == '=':
                    self.add_temp()
                else:
                    self.ui.lbl_temp.setText(temp[:-2] + f'{btn.text()} ')
            else:
                self.ui.lbl_temp.setText(self.calculate() + f' {btn.text()}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Calculator()

    window.show()
    sys.exit(app.exec())
