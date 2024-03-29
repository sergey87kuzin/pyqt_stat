from enum import Enum


class Choices(Enum):
    GRAPHICS = ('Год суммарно', 'Месяц по стокам')
    MONTHS = (
        'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
        'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
    )


class Titles(Enum):
    ROOT_TITLE = 'Счетчик для стоков'
    RESULT_TITLE = 'Результат'
    FRAME_TITLE = 'Ваши данные'
    QUIT_TITLE = 'Выход'
    WARN_TITLE = 'Внимание'
    SUCCESS_TITLE = 'Ура'
    GRAPHIC_TITLE = 'Результат Вашей работы наглядно'


class InfoTexts(Enum):
    QUIT_TEXT = 'Хотите выйти?'
    WARN_STOCK_TEXT = '''Не указано ни одного стока, пожалуйста, задайте
                      сток в соответствующем разделе'''
    WARN_NO_STOCK = 'Выберите сток'
    ERROR_TEXT = 'что-то пошло не так('
    SUCCESS_TEXT = 'запись добавлена'
    NAME_STOCK = 'назовите сток'
    DUPLICATE = 'Такой сток уже существует'
    STOCK_CREATED = 'Сток создан'
    CHOOSE_GRAPH = 'выберите тип графика'
    NO_YEAR_DATA = 'вы не вносили данных по продажам этого года'
    NO_MONTH_DATA = 'вы не вносили данных по продажам этого месяца'
    WRONG_INPUT = 'некорректно внесено значение'
    WRONG_TYPE = 'нужно вносить цифры'


class ButtonTexts(Enum):
    ADD_LOADS = 'ОТЛОЖЕННЫЕ ЗАГРУЗКИ'
    MONTH_STATS = 'ЗАГРУЗКИ МЕСЯЦА'
    YEAR_STATS = 'ЗАГРУЗКИ ГОДА'
    ADD_INCOME = 'СТАТИСТИКА'
    CREATE_STOCK = 'ДОБАВИТЬ ФОТОБАНК'
    GRAPHIC = 'ГРАФИК ЗА ГОД'
    STOCK_GRAPHIC = 'ГРАФИК ПО СТОКАМ'
    TOTAL = 'ИТОГИ ГОДА'
    ADD = 'Внести'
    SAVE = 'Сохранить'
    CREATE = 'Создать'
    PLOT = 'Построить'
    SHOW = 'Показать'
    SHOW_STATS = 'Показать статистику'
    PREV = 'Предыдущий месяц'
    NEXT = 'Следующий месяц'
    PREV_YEAR = 'Предыдущий год'
    NEXT_YEAR = 'Следующий год'
    BACK_COLOR = 'Цвет фона'
    BUTTON_COLOR = 'Цвет кнопки'
    MENU_BUTTON_COLOR = 'Цвет кнопки меню'
    MENU_TEXT_COLOR = 'Цвет текста меню'
    FONT_COLOR = 'Цвет текста'
    PHOTO_COLOR = 'Цвет иконки фото'
    VIDEO_COLOR = 'Цвет иконки видео'


class ButtonNames(Enum):
    ADD_LOADS = 'add_loads_button'
    MONTH = 'month_stats_button'
    YEAR = 'year_stats_button'
    ADD_INCOME = 'add_income_button'
    STOCK = 'create_stock_button'
    GRAPHIC = 'graphic_button'
    TOTAL = 'total_button'


class LabelTexts(Enum):
    SALES = 'Продажи'
    LOADS = 'Загрузки'
    PHOTO = 'Фотографии'
    VIDEO = 'Видео'
    INCOME = 'Доход'
    STOCK = 'Фотобанк'
    DATE = 'Выберите дату'
    MONTH = 'Месяц'
    YEAR = 'Год'
    CREATE_STOCK = 'Создайте сток'
    GRAPHIC_TYPE = 'Вид графика'
    MONTH_STATS = 'Статистика месяца'
    YEAR_STATS = 'Статистика года'
    GRAPHIC_TOP = 'Построение графика'
    TOTAL_TOP = 'Итоговая таблица'


class LabelNames(Enum):
    LOADS_DAY = 'add_loads_day_in'
    LOADS_MONTH = 'add_loads_month_in'
    LOADS_YEAR = 'add_loads_year_in'
    LOADS_PHOTO = 'add_loads_photo_in'
    LOADS_VIDEO = 'add_loads_video_in'
    PHOTO_CIRCLE = 'photo_circle'
    VIDEO_CIRCLE = 'video_circle'
    MONTH_MONTH = 'month_stats_month_in'
    MONTH_YEAR = 'month_stats_year_in'
    YEAR_YEAR = 'year_stats_year_in'
    INCOME_MONTH = 'add_income_month_in'
    INCOME_YEAR = 'add_income_year_in'
    INCOME_PHOTO = 'add_income_photo_in'
    INCOME_VIDEO = 'add_income_video_in'
    INCOME_INCOME = 'add_income_income_in'
    INCOME_STOCK = 'add_income_stock_in'
    STOCK = 'stock_stock_in'
    TOTAL_MONTH = 'total_month_in'
    TOTAL_YEAR = 'total_year_in'


class Menus(Enum):
    LOAD_MENU = 'Загрузки'
    SALES_MENU = 'Продажи'
    COLOR_MENU = 'Цвета'


class ErrorMessages(Enum):
    WRONG_BUTTON_COUNT = 'Неверное число кнопок'
    WRONG_BUTTON_NAME = 'Неверное название кнопки'
    WRONG_DATE_INPUT = 'Неверно сохраняется дата'
    WRONG_MONTH_INPUT = 'Неверно сохраняется месяц'
    WRONG_YEAR_INPUT = 'Неверно сохраняется год'
    WRONG_VIDEO_INPUT = 'Неверно сохраняется количество видео'
    WRONG_PHOTO_INPUT = 'Неверно сохраняется количество фото'
    WRONG_PHOTO_SHOW = 'Неверно отображается фото'
    WRONG_INCOME_INPUT = 'Неверно сохраняется сумма продаж'
    WRONG_STOCK_INPUT = 'Неверно сохраняется сток'
    WRONG_SALES_SHOW = 'Неверно отображаются продажи'
