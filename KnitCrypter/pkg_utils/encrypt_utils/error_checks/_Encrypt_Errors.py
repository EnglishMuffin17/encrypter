def _extract_type(o:object):
    return str(o.__class__).strip(" <clas>")

class SequenceError(Exception):

    _error_reasons = {
        0:lambda array:f"{array} has one or more equivalent values"
    }

    def __init__(self,array,reason=0):
        array = _extract_type(array)
        self._reason = self._error_reasons[reason](array)
        super().__init__()

    def __str__(self):
        return self._reason