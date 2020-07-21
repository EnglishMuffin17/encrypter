class FlagError(Exception):

    _error_reasons = {
        0:lambda flag:f"{flag} is not a legal flag"
    }

    def __init__(self,flag,reason=0):
        self._reason = self._error_reasons[reason](flag)
        super().__init__()

    def __str__(self):
        return self._reason