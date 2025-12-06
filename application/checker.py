from datetime import datetime


class Checker:
    @staticmethod
    def check_date(date_str : str):
        if date_str is None:
            return False
        try:
            dt = datetime.strptime(date_str, "%d.%m.%y %H:%M")
            now = datetime.now()
            return dt >= now
        except ValueError:
            return False