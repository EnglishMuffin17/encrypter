try:
    from error_checks._Encrypt_Cases import _Test_Cases
except ModuleNotFoundError:
    from .error_checks._Encrypt_Cases import _Test_Cases

class _Character_Struct:

    """
    Represents a single character

    e.g. 'h' not 'ha'
    """

    def __init__(self,char:str):
        self._char = char
    
    def __repr__(self):
        return f"{self._char}"

    @property
    def _char(self):
        return self.__char

    @_char.setter
    def _char(self,char:str):
        _Test_Cases._verify_attribute_set(self,'__char')
        _Test_Cases._verify_char_value(char)
        self.__char = char