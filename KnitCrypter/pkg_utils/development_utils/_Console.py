from datetime import datetime

_print_count = -1

class _Console:

    """
    Handles the format console messages utilize
    """

    def __init__(self,message="Default message",delimiter="|"):
        self._message = message
        self._delimiter = delimiter

    def __repr__(self):
        return f"[{self._count}] {self._time} {self._delimiter} {self._message}"

    @property
    def _datetime(self):
        date_time = datetime.now()
        return date_time

    @property
    def _ctime(self):
        return self._datetime.ctime()

    @property
    def _date(self):
        return self._datetime.date()

    @property
    def _time(self):
        return self._datetime.time()

    @property
    def _count(self):
        global _print_count
        _print_count += 1
        return _print_count

    @staticmethod
    def _print_count():
        global _print_count
        return _print_count
    
    def _submit(self):
        print(self)