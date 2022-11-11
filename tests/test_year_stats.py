from datetime import datetime

from pages import year_stats


def test_texts(app, clear_db, db_month_insert, insert_colors):
    year_stats.year_stats(app.layout, app.photo, app.video)
    new_window = app.children()[2].children()[1]
    label = new_window.children()[1].text()
    month = new_window.children()[2].text()
    assert label == str(datetime.now().year)
    assert month == 'Январь'
    assert len(new_window.children()) >= 459
