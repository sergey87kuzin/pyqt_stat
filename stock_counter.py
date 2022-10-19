import logging
from tkinter import (
    Button, Tk, W, LabelFrame, messagebox
)
from pages import (
    add_loads, month_stats, year_stats, add_income,
    create_stock, graphic, total
)
from src.helper import resource_path, start_sql
from src.global_enums.literals import (
    Titles, InfoTexts, ButtonTexts, ButtonNames
)

# настройка логирования
logging.basicConfig(
    level=logging.INFO,
    filename=resource_path('main.log'),
    filemode='w',
    format=('%(asctime)s, %(levelname)s, %(name)s, %(message)s,' +
            '%(funcName)s, %(lineno)d')
)

start_sql()
logging.info('таблицы в БД в наличии')


class StockCounter():
    def __init__(self):
        self.root = Tk()
        self.root.title(Titles.ROOT_TITLE.value)
        self.second_screen = Tk()
        self.second_screen.title(Titles.RESULT_TITLE.value)
        self.second_screen.eval('tk::PlaceWindow . center')
        self.frame = LabelFrame(
            self.second_screen, text=Titles.FRAME_TITLE.value,
            padx=5, pady=5
        )

    def on_closing(self):
        if messagebox.askokcancel(
            Titles.QUIT_TITLE.value, InfoTexts.QUIT_TEXT.value
                ):
            self.second_screen.quit()
            self.root.quit()

    def start(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.second_screen.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.frame.pack()

        add_loads_button = Button(
            self.root, text=ButtonTexts.ADD_LOADS.value,
            command=lambda: add_loads.add_loads(self.frame), width=25,
            name=ButtonNames.ADD_LOADS.value
        )
        month_stats_button = Button(
            self.root, text=ButtonTexts.MONTH_STATS.value, width=25,
            command=lambda: month_stats.month_stats(self.frame),
            name=ButtonNames.MONTH.value
        )
        year_stats_button = Button(
            self.root, text=ButtonTexts.YEAR_STATS.value, width=25,
            command=lambda: year_stats.year_stats(self.frame),
            name=ButtonNames.YEAR.value
        )
        add_income_button = Button(
            self.root, text=ButtonTexts.ADD_INCOME.value, width=25,
            command=lambda: add_income.add_income(self.frame),
            name=ButtonNames.ADD_INCOME.value
        )
        create_stock_button = Button(
            self.root, text=ButtonTexts.CREATE_STOCK.value, width=25,
            command=lambda: create_stock.create_stock(self.frame),
            name=ButtonNames.STOCK.value
        )
        graphic_button = Button(
            self.root, text=ButtonTexts.GRAPHIC.value, width=25,
            command=lambda: graphic.graphic(self.frame),
            name=ButtonNames.GRAPHIC.value
        )
        total_button = Button(
            self.root, text=ButtonTexts.TOTAL.value, width=25,
            command=lambda: total.total(self.frame),
            name=ButtonNames.TOTAL.value
        )
        buttons = [add_loads_button, month_stats_button, year_stats_button,
                   add_income_button, create_stock_button, graphic_button,
                   total_button]
        for ind, button in enumerate(buttons):
            button.grid(row=ind, column=0, sticky=W)


if __name__ == '__main__':
    stock = StockCounter()
    stock.start()
    stock.root.mainloop()
