class DateFormatter:

    MONTHS_DICTIONARY = {
        '01': 'January',
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'August',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December',
    }

    def __init__(self):
        pass

    def get_str_month(self, number):
        return self.MONTHS_DICTIONARY[str(number)]
