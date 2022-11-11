from datetime import date

from src.global_enums.literals import LabelTexts, ButtonTexts
from pages import add_loads


def test_texts(app, qtbot):
    add_loads.add_loads(app.layout)
    # qtbot.mouseClick(app.load_menu, QtCore.Qt.LeftButton)
    # app.load_menu.aboutToShow().connect()
    # item = app.load_menu.actions()[0]
    # item.aboutToShow().emit(QtCore.pyqtSlot())
    # action_rect = app.main_menu.actionGeometry(
    #     app.load_menu.menuAction()
    # )
    # print(action_rect.top())
    # qtbot.wait(1000)
    # qtbot.mouseMove(app.main_menu, action_rect.center())
    # qtbot.wait(1000)
    # qtbot.mouseClick(
    #     app.main_menu, QtCore.Qt.LeftButton, pos=action_rect.center()
    # )
    # qtbot.wait(1000)
    # load_rect = app.load_menu.actionGeometry(app.loads_button)
    # print(load_rect.top())
    # qtbot.mouseMove(app.load_menu, load_rect.center())
    # qtbot.wait(1000)
    # qtbot.mouseClick(
    #     app.load_menu, QtCore.Qt.LeftButton, pos=load_rect.center()
    # )
    label = app.layout.takeRow(0).fieldItem.widget().text()
    assert label == LabelTexts.LOADS.value

    rows = ((LabelTexts.DATE.value, date.today().strftime("%d.%m.%Y")),
            (LabelTexts.PHOTO.value, '0'),
            (LabelTexts.VIDEO.value, '0'))
    for row in rows:
        layout_row = app.layout.takeRow(0)
        label = layout_row.labelItem.widget().text()
        value = layout_row.fieldItem.widget().text()
        assert label == row[0]
        assert value == row[1]


def test_button_texts(app):
    add_loads.add_loads(app.layout)
    button = app.layout.takeRow(4).fieldItem.widget().text()
    assert button == ButtonTexts.SAVE.value
