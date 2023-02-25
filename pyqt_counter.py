import logging
import shutil
import sqlite3
import sys
from pathlib import Path

from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtGui import QBrush, QIcon, QImage, QPalette
from PyQt5.QtWidgets import (QAction, QApplication, QColorDialog, QFileDialog,
                             QFormLayout, QFrame, QHBoxLayout, QMainWindow,
                             QMenuBar, QMessageBox, QVBoxLayout, QWidget)

from configure import DB_NAME
from pages import (add_income, add_loads, create_stock, graphic, month_stats,
                   total, year_stats)
from src.buttons import IconButton, MenuButton
from src.global_enums.literals import ButtonTexts, InfoTexts, Menus, Titles
from src.helper import clean_frame, resource_path, start_sql


class StockWindow(QMainWindow):
    window_height = 600
    window_width = 600

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
        self.setGeometry(
            QRect(100, 100, self.window_height, self.window_width)
        )
        self.set_style()

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

    def set_style(self):
        try:
            with sqlite3.connect(resource_path(DB_NAME)) as conn:
                cursor = conn.cursor()
                init_style = cursor.execute(
                    '''SELECT widget, style FROM stylesheets WHERE
                    widget IN (:button, :text, :photo, :video)''',
                    {'button': 'button_color',
                     'text': 'button_text_color',
                     'photo': 'photo', 'video': 'video'}
                ).fetchall()
                button_color, button_text_color = '', ''
                for line in init_style:
                    if line[0] == 'video':
                        self.video = line[1]
                    elif line[0] == 'photo':
                        self.photo = line[1]
                    elif line[0] == 'button_text_color':
                        button_text_color = line[1]
                    elif line[0] == 'button_color':
                        button_color = line[1]
                    self.setStyleSheet(f'''
                        MainWindow {{
                            background-image: url(fon.jpg);
                            background-repeat: no-repeat;
                            background-position: center;
                        }}
                        .QPushButton {{
                            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {button_color}, stop:0.5 white, stop:1 {button_color});
                            color: {button_text_color};
                            font: bold italic 16pt 'Comic Sans MS';
                            width: 75px ;
                            height: 50px;
                            border: none;
                            text-align: center;
                            border-radius: 8px;
                        }}
                        QDateEdit {{
                            border: none;
                        }}
                        QPushButton:hover {{background: #ff0000;}}
                        QPushButton:pressed {{background-color: {button_color};}}
                        QLabel {{
                            padding-bottom: 0px;
                            padding-top: 0px;
                            marging-top: 0px;
                            marging-bottom: 0px;
                        }}
                        ''')
        except Exception as e:
            logging.warning(str(e))
            QMessageBox.warning(
                self, Titles.WARN_TITLE.value,
                InfoTexts.ERROR_TEXT.value
            )
            return

        oImage = QImage("src/images/fon.jpg")
        sImage = oImage.scaled(QSize(self.window_height, self.window_width))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

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
             self.change_background, self.color_menu),
            # (ButtonTexts.BUTTON_COLOR.value, 'P',
            #  lambda: self.change_color(*COLOR_PATTERNS[1]), self.color_menu),
            # (ButtonTexts.FONT_COLOR.value, 'Ctrl+F',
            #  lambda: self.change_color(*COLOR_PATTERNS[2]), self.color_menu),
            (ButtonTexts.BUTTON_COLOR.value, 'P',
             lambda: self.change_icon_color('button_color'), self.color_menu),
            (ButtonTexts.FONT_COLOR.value, 'Ctrl+F',
             lambda: self.change_icon_color('button_text_color'),
             self.color_menu),
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
            elif indicator in ['button_color', 'button_text_color']:
                self.set_style()
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

    def change_background(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File",
            "~",
            "Images (*.png *.jpg)"
        )
        if filename:
            path = Path(filename)
            shutil.copyfile(path, 'src/images/fon.jpg')
            self.set_style()


if __name__ == '__main__':
    start_sql()
    app = QApplication(sys.argv)
    window = StockWindow()
    window.show()

    sys.exit(app.exec())
