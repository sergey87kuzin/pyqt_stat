import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFormLayout,
    QWidget,
    QAction,
    QMenuBar
)
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon
from pages import (
    add_loads, add_income, create_stock, month_stats,
    year_stats, graphic, total
)
from src.global_enums.literals import (
    Titles, ButtonTexts
)
from src.helper import start_sql
from src.stylesheets import StyleSheet


class StockWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(Titles.ROOT_TITLE.value)
        self.layout = QFormLayout()
        geometry = QRect(0, 0, 300, 300)
        self.setGeometry(geometry)

        self.create_menu()

        widget = QWidget()
        widget.setLayout(self.layout)

        self.setCentralWidget(widget)

    def create_menu(self):
        main_menu = QMenuBar(self)
        self.setMenuBar(main_menu)
        load_menu = main_menu.addMenu('Loads')
        sale_menu = main_menu.addMenu('Sales')

        items = [
            (ButtonTexts.ADD_LOADS.value, 'A',
             lambda: add_loads.add_loads(self.layout), load_menu),
            (ButtonTexts.MONTH_STATS.value, 'M',
             lambda: month_stats.month_stats(self.layout), load_menu),
            (ButtonTexts.YEAR_STATS.value, 'Y',
             lambda: year_stats.year_stats(self.layout), load_menu),
            (ButtonTexts.ADD_INCOME.value, 'I',
             lambda: add_income.add_income(self.layout), sale_menu),
            (ButtonTexts.CREATE_STOCK.value, 'C',
             lambda: create_stock.create_stock(self.layout), sale_menu),
            (ButtonTexts.GRAPHIC.value, 'G',
             lambda: graphic.graphic(self.layout), sale_menu),
            (ButtonTexts.TOTAL.value, 'T',
             lambda: total.total(self.layout), sale_menu)
        ]
        for item in items:
            self.add_menu_item(*item)

    def add_menu_item(self, text, shortcut, function, menu):
        menu_item = QAction(QIcon(''), text, self)
        menu_item.setShortcut(shortcut)
        menu_item.triggered.connect(function)
        menu.addAction(menu_item)


if __name__ == '__main__':
    start_sql()
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)
    window = StockWindow()
    window.show()

    app.exec()
