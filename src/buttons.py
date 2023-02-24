import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout
from configure import DB_NAME


class MenuButton(QPushButton):
    def __init__(self, text):
        super().__init__()
        self.make_style()
        self.set_word_wrap(text)

    def make_style(self):
        background, color = self.get_menu_buttons_colours()

        self.setStyleSheet(
            f'''QPushButton {{
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 {background}, stop:0.5 white, stop:1 {background});
                color: {color};
                font: bold italic 10pt 'Comic Sans MS';
                white-space: pre-wrap;
                width: 75px ;
                height: 50px;
                border: none;
                text-align: center;
                border-radius: 8px;
                }}
                QPushButton:pressed {{
                background-color: {background}
                }}
                QLabel {{
                background-color: rgba(255, 255, 255, 10);
                color: {color};
                font: bold italic 10pt 'Comic Sans MS';
                border: none;
                white-space: pre-wrap;
                text-align: center;
                }}
            '''
        )

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
        # label.setStyleSheet("background-color: rgba(255, 255, 255, 10);")
        layout = QHBoxLayout(self)
        layout.addWidget(label)


class IconButton(QPushButton):
    def __init__(self, icon):
        super().__init__(icon, '')

        self.setStyleSheet(
            '''QPushButton {background-color: transparent;
                color: black;
                font: bold italic 10pt 'Comic Sans MS';
                max-width: 30px ;
                height: 30px;
                border: none;
                text-align: center;
                border-radius: 5px;
            }'''
        )
