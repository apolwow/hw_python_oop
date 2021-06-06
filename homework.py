import datetime as dt


class Record:
    '''Класс Record данные о денежной сумме или количестве
    килокалорий, дате создания записи и поясняющих комментариях.
    '''

    def __init__(self, amount, comment, date=None):
        '''Метод __init__ инициализирует атрибуты.'''
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    '''Класс Calculator содержит данные о дневном лимите трат/калорий,
    которые задал пользователь. Пустой список для хранения записей.
    '''
    def __init__(self, limit):
        '''Метод __init__ инициализирует атрибуты.'''
        self.limit = limit
        self.records = []
        self.today = dt.date.today()
        self.week_later = self.today - dt.timedelta(days=7)

    def add_record(self, record):
        '''Метода add_record принимает объект класса Record и добавляет
        его в конец списка records.
        '''
        self.records.append(record)

    def get_today_stats(self):
        '''Метод get_today_stats считает сколько каллорий
        съедено/сколько денег потрачено за текущий день.
        '''
        return sum(
            record.amount for record in self.records
            if record.date == self.today)

    def get_week_stats(self):
        '''Метод get_week_stats считает количество полученных
        каллорий/потраченых денег за последние 7 дней.
        '''
        return sum(
            record.amount for record in self.records
            if self.week_later <= record.date <= self.today)

    def get_remaining_limit(self):
        '''Метод get_remaining_limit считает оставшиеся
        каллории/денеги.
        '''
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    '''Подкласс CaloriesCalculator для расчета каллорий.
    Содержит данные надкласса.
    '''
    def get_calories_remained(self):
        '''Метод get_calories_remained проверяет сколько каллорий
        получено и возвращает соответсвующие рекоммендации.
        '''
        calories_remained = self.get_remaining_limit()
        if calories_remained > 0:
            return (
                'Сегодня можно съесть что-нибудь ещё, но '
                f'с общей калорийностью не более {calories_remained} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    '''Подкласс CashCalculator для учета финансов.
    Содержит данные надкласса.
    '''
    # Константы для соответсвующей валюты
    RUB_RATE = 1.0
    USD_RATE = 60.0
    EURO_RATE = 70.0

    def get_today_cash_remained(self, currency):
        '''Метод get_today_cash_remained денежного калькулятора
        принимает на вход код валюты и возвращает дневной баланс.
        '''
        currencies = {
            'rub': ('руб', self.RUB_RATE),
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE)
        }
        cash_remained = self.get_remaining_limit()
        if currency not in currencies:
            return f'Указана неправильная валюта - {currency}'
        if cash_remained == 0:
            return 'Денег нет, держись'
        cur_name, rate = currencies.get(currency)
        cash_remained = round(cash_remained / rate, 2)
        if cash_remained > 0:
            return f'На сегодня осталось {cash_remained} {cur_name}'
        cash_remained = abs(cash_remained)
        return f'Денег нет, держись: твой долг - {cash_remained} {cur_name}'
