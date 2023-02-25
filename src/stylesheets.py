STYLESHEET = '''
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
QPushButton:pressed {{background-color: {button_color};}}
QLabel {{
    padding-bottom: 0px;
    padding-top: 0px;
    margin-top: 0px;
    margin-bottom: 0px;
}}
'''

MENUBUTTONSTYLE = '''QPushButton {{
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

ICONBUTTONSTYLE = '''QPushButton {background-color: transparent;
                    color: black;
                    font: bold italic 10pt 'Comic Sans MS';
                    max-width: 30px ;
                    height: 30px;
                    border: none;
                    text-align: center;
                    border-radius: 5px;
                }'''
