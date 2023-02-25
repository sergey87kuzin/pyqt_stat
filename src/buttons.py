import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout
from configure import DB_NAME
from src.stylesheets import MENUBUTTONSTYLE, ICONBUTTONSTYLE


class MenuButton(QPushButton):
    def __init__(self, text):
        super().__init__()
        self.make_style()
        self.set_word_wrap(text)

    def make_style(self):
        background, color = self.get_menu_buttons_colours()

        self.setStyleSheet(MENUBUTTONSTYLE.format(
            background=background, color=color
        ))

    def get_menu_buttons_colours(self):
        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                result = cursor.execute(
                    ''' SELECT style FROM stylesheets WHERE widget IN
                     (?, ?)''', ['menu', 'text']
                ).fetchall()
                return [line[0] for line in result]
        except Exception as e:
            print(str(e))

    def set_word_wrap(self, text):
        label = QLabel(text)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter)
        layout = QHBoxLayout(self)
        layout.addWidget(label)


class IconButton(QPushButton):
    def __init__(self, icon):
        super().__init__(icon, '')

        self.setStyleSheet(ICONBUTTONSTYLE)
