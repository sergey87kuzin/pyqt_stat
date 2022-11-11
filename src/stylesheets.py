StyleSheet = '''
QWidget {
    background-color: white;
    color: black;
}
QPushButton {background-color: grey;
    font: bold italic 16pt 'Comic Sans MS';
    width: 75px ;
    height: 50px;
    border: none;
    text-align: center;
    border-radius: 8px;
}
QDateEdit {
    border: none;
}
QPushButton {color: black;}
# QPushButton:hover {background: #ff0000;}
# QPushButton:pressed {background-color: blue;}
QLabel {
    padding-bottom: 0px;
    padding-top: 0px;
    marging-top: 0px;
    marging-bottom: 0px;
}
'''

COLOR_PATTERNS = ((r'background-color: [#0-9a-zA-F]+',
                   'background-color: %s;'),
                  (r'QPushButton {background-color: [#0-9a-zA-F]+',
                   'QPushButton {background-color: %s'),
                  (r'QPushButton {color: [#0-9a-zA-F]+',
                   'QPushButton {color: %s'))
