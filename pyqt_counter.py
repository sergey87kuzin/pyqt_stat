import logging
import re
import sqlite3
import sys

from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QColorDialog, QFormLayout,
                             QHBoxLayout, QMainWindow, QMenuBar, QMessageBox,
                             QVBoxLayout, QWidget, QFrame)

from configure import DB_NAME
from pages import (add_income, add_loads, create_stock, graphic, month_stats,
                   total, year_stats)
from src.global_enums.literals import ButtonTexts, InfoTexts, Menus, Titles
from src.helper import resource_path, start_sql, clean_frame
from src.stylesheets import COLOR_PATTERNS
from src.buttons import MenuButton, IconButton


class StockWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.set_log_config()

        self.setWindowTitle(Titles.ROOT_TITLE.value)
        self.main_layout = QHBoxLayout()
        self.left_frame = QFrame()
        self.left_layout = QVBoxLayout()
        self.center_layout = QVBoxLayout()
        self.left_frame.setLayout(self.left_layout)
        self.layout = QFormLayout()
        self.main_layout.addWidget(self.left_frame)
        self.main_layout.setStretch(0, 5)
        self.main_layout.addLayout(self.center_layout)
        self.main_layout.setStretch(1, 1)
        self.main_layout.addLayout(self.layout)
        self.main_layout.setStretch(2, 10)
        self.setGeometry(QRect(0, 0, 500, 300))
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
        except Exception as e:
            logging.warning(str(e))
            QMessageBox.warning(
                self, Titles.WARN_TITLE.value,
                InfoTexts.ERROR_TEXT.value
            )
            return

        self.create_menu()
        self.create_left_menu()
        self.create_center_buttons()

        widget = QWidget()
        widget.setLayout(self.main_layout)

        self.setCentralWidget(widget)

    def set_log_config(self):
        # настройка логирования
        logging.basicConfig(
            level=logging.INFO,
            filename=resource_path('main.log'),
            filemode='w',
            format=(''' %(asctime)s, %(levelname)s, %(name)s, %(message)s,
                    %(funcName)s, %(lineno)d''')
        )

    def create_menu(self):
        ''' создание верхнего меню '''
        self.main_menu = QMenuBar(self)
        self.setMenuBar(self.main_menu)
        self.load_menu = self.main_menu.addMenu(Menus.LOAD_MENU.value)
        self.sale_menu = self.main_menu.addMenu(Menus.SALES_MENU.value)
        self.color_menu = self.main_menu.addMenu(Menus.COLOR_MENU.value)

        self.items = [
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
             lambda: self.change_icon_color('video'), self.color_menu),
            (ButtonTexts.MENU_TEXT_COLOR.value, 'Ctrl+T',
             lambda: self.change_icon_color('text'), self.color_menu),
            (ButtonTexts.MENU_BUTTON_COLOR.value, 'Ctrl+M',
             lambda: self.change_icon_color('menu'), self.color_menu),
        ]

        for item in self.items:
            self.add_menu_item(*item)

    def add_menu_item(self, text, shortcut, function, menu):
        '''  '''
        menu_item = QAction(QIcon(''), text, menu)
        menu_item.setShortcut(shortcut)
        menu_item.triggered.connect(function)
        menu.addAction(menu_item)

    def create_left_menu(self):
        '''  '''
        for item in self.items[:7]:
            self.add_left_menu_item(*item)

    def add_left_menu_item(self, name, shortcut, function, menu):
        '''  '''
        button = MenuButton(name)
        button.setFlat(False)
        button.clicked.connect(function)
        self.left_layout.addWidget(button)

    def create_center_buttons(self):
        '''  '''
        right_button = IconButton(QIcon('src/icons/arrow_right.png'))
        left_button = IconButton(QIcon('src/icons/arrow_left.png'))
        right_button.clicked.connect(
            lambda: self.show_menu(right_button, left_button)
        )
        left_button.clicked.connect(
            lambda: self.hide_menu(right_button, left_button)
        )
        right_button.hide()
        self.center_layout.setAlignment(Qt.AlignTop)
        self.center_layout.addWidget(right_button)
        self.center_layout.addWidget(left_button)

    def change_color(self, pattern, repl):
        '''  '''
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
        except Exception as e:
            logging.warning(str(e))
            QMessageBox.warning(
                self, Titles.WARN_TITLE.value,
                InfoTexts.ERROR_TEXT.value
            )
            return

    def change_icon_color(self, indicator):
        '''  '''
        color = QColorDialog.getColor()
        if not color.isValid():
            return
        if indicator == 'photo':
            self.photo = color
        elif indicator == 'video':
            self.video = color
        try:
            with sqlite3.connect(resource_path(DB_NAME)) as conn:
                cursor = conn.cursor()
                cursor.execute('''UPDATE stylesheets SET style=:style
                               WHERE widget=:widget''',
                               {'style': color.name(), 'widget': indicator})
            if indicator in ['text', 'menu']:
                clean_frame(self.left_frame)
                self.create_left_menu()
        except Exception as e:
            logging.warning(str(e))
            QMessageBox.warning(
                self, Titles.WARN_TITLE.value,
                InfoTexts.ERROR_TEXT.value
            )
            return

    def hide_menu(self, right_button, left_button):
        '''  '''
        self.left_frame.hide()
        right_button.show()
        left_button.hide()

    def show_menu(self, right_button, left_button):
        '''  '''
        self.left_frame.show()
        right_button.hide()
        left_button.show()


if __name__ == '__main__':
    start_sql()
    app = QApplication(sys.argv)
    window = StockWindow()
    window.show()

    sys.exit(app.exec())
