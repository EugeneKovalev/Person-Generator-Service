#!/usr/bin/env python
# -*- coding: utf-8 -*-

class DateFormatter:

    MONTHS_DICTIONARY = {
        '01': {'en': 'January', 'ru': 'января'},
        '02': {'en': 'February', 'ru': 'февраля'},
        '03': {'en': 'March', 'ru': 'марта'},
        '04': {'en': 'April', 'ru': 'апреля'},
        '05': {'en': 'May', 'ru': 'мая'},
        '06': {'en': 'June', 'ru': 'июня'},
        '07': {'en': 'July', 'ru': 'июля'},
        '08': {'en': 'August', 'ru': 'августа'},
        '09': {'en': 'September', 'ru': 'сентября'},
        '10': {'en': 'October', 'ru': 'октября'},
        '11': {'en': 'November', 'ru': 'ноября'},
        '12': {'en': 'December', 'ru': 'декабря'}
    }

    def __init__(self):
        pass

    def get_str_month(self, number, lang):
        return self.MONTHS_DICTIONARY[str(number)][lang]
