from datetime import datetime

class _Console:

    """
    Handles the format console messages utilize
    """

    __print_count = -1

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
        _Console.__print_count += 1
        return _Console.__print_count
    
    def _submit(self):
        print(self)

def _print_count():
    return _Console.__print_count