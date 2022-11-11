import re
import sqlite3
import sys

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QColorDialog, QFormLayout,
                             QMainWindow, QMenuBar, QMessageBox, QWidget)

from configure import DB_NAME
from pages import (add_income, add_loads, create_stock, graphic, month_stats,
                   total, year_stats)
from src.global_enums.literals import ButtonTexts, InfoTexts, Menus, Titles
from src.helper import resource_path, start_sql
from src.stylesheets import COLOR_PATTERNS


class StockWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(Titles.ROOT_TITLE.value)
        self.layout = QFormLayout()
        self.setGeometry(QRect(0, 0, 400, 300))
        try:
            with sqlite3.connect(resource_path(DB_NAME)) as conn:
                cursor = conn.cursor()
                init_style = cursor.execute(
                    '''SELECT widget, style FROM stylesheets WHERE
                    widget IN (:main, :photo, :video)''',
                    {'main': 'main', 'photo': 'photo', 'video': 'video'}
                ).fetchall()
                for line in init_style:
                    if line[0] == 'main':
                        self.setStyleSheet(line[1])
                    elif line[0] == 'photo':
                        self.photo = line[1]
                    else:
                        self.video = line[1]
        except Exception:
            QMessageBox.warning(
                self, Titles.WARN_TITLE.value,
                InfoTexts.ERROR_TEXT.value
            )
            return

        self.create_menu()

        widget = QWidget()
        widget.setLayout(self.layout)

        self.setCentralWidget(widget)

    def create_menu(self):
        self.main_menu = QMenuBar(self)
        self.setMenuBar(self.main_menu)
        self.load_menu = self.main_menu.addMenu(Menus.LOAD_MENU.value)
        self.sale_menu = self.main_menu.addMenu(Menus.SALES_MENU.value)
        self.color_menu = self.main_menu.addMenu(Menus.COLOR_MENU.value)

        items = [
            (ButtonTexts.ADD_LOADS.value, 'A',
             lambda: add_loads.add_loads(self.layout), self.load_menu),
            (ButtonTexts.MONTH_STATS.value, 'M',
             lambda: month_stats.month_stats(
                 self.layout, self.photo, self.video
             ), self.load_menu),
            (ButtonTexts.YEAR_STATS.value, 'Y',
             lambda: year_stats.year_stats(
                 self.layout, self.photo, self.video
             ), self.load_menu),
            (ButtonTexts.ADD_INCOME.value, 'I',
             lambda: add_income.add_income(self.layout), self.sale_menu),
            (ButtonTexts.CREATE_STOCK.value, 'C',
             lambda: create_stock.create_stock(self.layout), self.sale_menu),
            (ButtonTexts.GRAPHIC.value, 'G',
             lambda: graphic.year_chart(self.layout), self.sale_menu),
            (ButtonTexts.STOCK_GRAPHIC.value, 'S',
             lambda: graphic.stock_chart(self.layout), self.sale_menu),
            (ButtonTexts.TOTAL.value, 'T',
             lambda: total.total(self.layout), self.sale_menu),
            (ButtonTexts.BACK_COLOR.value, 'B',
             lambda: self.change_color(*COLOR_PATTERNS[0]), self.color_menu),
            (ButtonTexts.BUTTON_COLOR.value, 'P',
             lambda: self.change_color(*COLOR_PATTERNS[1]), self.color_menu),
            (ButtonTexts.FONT_COLOR.value, 'Ctrl+F',
             lambda: self.change_color(*COLOR_PATTERNS[2]), self.color_menu),
            (ButtonTexts.PHOTO_COLOR.value, 'F',
             lambda: self.change_icon_color('photo'), self.color_menu),
            (ButtonTexts.VIDEO_COLOR.value, 'V',
             lambda: self.change_icon_color('video'), self.color_menu)
        ]
        for item in items:
            self.add_menu_item(*item)

    def add_menu_item(self, text, shortcut, function, menu):
        menu_item = QAction(QIcon(''), text, menu)
        menu_item.setShortcut(shortcut)
        menu_item.triggered.connect(function)
        menu.addAction(menu_item)

    def change_color(self, pattern, repl):
        try:
            with sqlite3.connect(resource_path(DB_NAME)) as conn:
                cursor = conn.cursor()
                init_style = cursor.execute(
                    ''' SELECT style FROM stylesheets
                    WHERE widget=:widget''', {'widget': 'main'}
                ).fetchone()[0]
                color = QColorDialog.getColor()
                if not color.isValid():
                    return
                replace = repl % color.name()
                style = re.sub(pattern, replace, init_style, 1)
                self.setStyleSheet(style)
                cursor.execute('''UPDATE stylesheets SET style=:style
                               WHERE widget=:widget''',
                               {'style': style, 'widget': 'main'})
        except Exception:
            QMessageBox.warning(
                self, Titles.WARN_TITLE.value,
                InfoTexts.ERROR_TEXT.value
            )
            return

    def change_icon_color(self, indicator):
        color = QColorDialog.getColor()
        if not color.isValid():
            return
        if indicator == 'photo':
            self.photo = color
        else:
            self.video = color
        try:
            with sqlite3.connect(resource_path(DB_NAME)) as conn:
                cursor = conn.cursor()
                cursor.execute('''UPDATE stylesheets SET style=:style
                               WHERE widget=:widget''',
                               {'style': color.name(), 'widget': indicator})
        except Exception:
            QMessageBox.warning(
                self, Titles.WARN_TITLE.value,
                InfoTexts.ERROR_TEXT.value
            )
            return


if __name__ == '__main__':
    start_sql()
    app = QApplication(sys.argv)
    window = StockWindow()
    window.show()

    sys.exit(app.exec())
