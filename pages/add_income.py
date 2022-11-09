import sqlite3
import sys
from PyQt5.QtWidgets import (
    QPushButton, QLabel, QMessageBox, QComboBox, QCalendarWidget
)
from src.helper import (
    resource_path, clean_layout, create_sales_month_data, field_insert
)
from src.validators import month_year_validate, int_validate, float_validate
from src.global_enums.literals import (
    Titles, InfoTexts, LabelTexts, ButtonTexts,  # ButtonNames, LabelNames
)
from configure import DB_NAME


def add_income(layout):
    ''' внести данные по продажам '''
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            stocks = cursor.execute('SELECT stock FROM stocks').fetchall()
            if not stocks:
                error = QMessageBox()
                error.setWindowTitle(Titles.WARN_TITLE.value)
                error.setText(InfoTexts.WARN_STOCK_TEXT.value)
                error.setIcon(QMessageBox.Warning)
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()
                return
    except Exception as e:
        error = QMessageBox()
        error.setWindowTitle(Titles.WARN_TITLE.value)
        error.setText(str(e))
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
        return

    clean_layout(layout)
    stocks = [stock[0] for stock in stocks]
    QLabel(LabelTexts.SALES.value)
    layout.addRow(QLabel(LabelTexts.SALES.value))
    ent_date = QCalendarWidget()
    layout.addRow('выберите дату', ent_date)
    lst_stock = QComboBox()
    lst_stock.addItems(stocks)
    layout.addRow(QLabel(LabelTexts.STOCK.value), lst_stock)
    ent_photo = field_insert(layout, 7, '0', LabelTexts.PHOTO.value)
    ent_video = field_insert(layout, 7, '0', LabelTexts.VIDEO.value)
    ent_income = field_insert(layout, 7, '0', LabelTexts.INCOME.value)
    btn_add = QPushButton(ButtonTexts.ADD.value)
    btn_add.clicked.connect(lambda: update_income(
        ent_date.monthShown(), ent_date.yearShown(), ent_photo.text(),
        ent_video.text(), ent_income.text(), lst_stock.currentText()
    ))
    layout.addRow(btn_add)


def update_income(
    month, year, photo, video, income, stock
):
    ''' Вносит доходы в БД '''
    if month_year_validate(month, year):
        return
    if (int_validate(photo) or int_validate(video)
       or float_validate(income)):
        return
    if not stock:
        error = QMessageBox()
        error.setWindowTitle(Titles.WARN_TITLE.value)
        error.setText(InfoTexts.WARN_NO_STOCK.value)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
        return
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            record = cursor.execute(
                '''SELECT stock FROM sales WHERE month=:month
                AND year=:year AND stock=:stock''',
                {
                    'month': month, 'year': year, 'stock': stock
                }
            ).fetchone()
            if not record:
                create_sales_month_data(month, year, stock)
            current_line = cursor.execute(
                ''' SELECT month, year, photo_sold, video_sold, amount_sold,
                stock FROM sales WHERE month=:month AND year=:year AND
                stock=:stock ''',
                {
                    'month': month, 'year': year, 'stock': stock
                }
            ).fetchone()
            cursor.execute(
                ''' UPDATE sales SET photo_sold=:photo, video_sold=:video,
                amount_sold=:income WHERE month=:month AND
                year=:year AND stock=:stock ''',
                {
                    'month': month, 'year': year,
                    'photo': int(photo) + int(current_line[2]),
                    'video': int(video) + int(current_line[3]),
                    'income': float(income) + float(current_line[4]),
                    'stock': stock
                })
            new_values = [(month, 'month'), (year, 'year')]
            cursor.executemany(
                'UPDATE dates SET value=? WHERE period=?', new_values
            )
            conn.commit()
    except Exception:
        error = QMessageBox()
        error.setWindowTitle(Titles.WARN_TITLE.value)
        error.setText(InfoTexts.ERROR_TEXT.value)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
        return
    if 'pytest' not in sys.modules:
        error = QMessageBox()
        error.setWindowTitle(Titles.SUCCESS_TITLE.value)
        error.setText(InfoTexts.SUCCESS_TEXT.value)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
