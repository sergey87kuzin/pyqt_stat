from datetime import datetime

from src.global_enums.literals import Choices
from pages import month_stats


def test_texts(app, clear_db, db_month_insert, insert_colors):
    month = datetime.now().month
    year = datetime.now().year
    month_stats.month_stats(
        app.layout, app.photo, app.video
    )
    label = app.layout.takeRow(0).fieldItem.widget().text()
    assert label == Choices.MONTHS.value[month - 1] + str(year)
