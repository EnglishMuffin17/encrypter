try:
    from error_checks._Encrypt_Cases import _Test_Cases
except ModuleNotFoundError:
    from .error_checks._Encrypt_Cases import _Test_Cases
finally:
    from re import findall

class _Number_Struct:

    """
    Converts a number into the desired format
    
    supported formats:
        - hex     '0x'
        - oct     '0o'
        - int     '00'
        - 2-10    '0b'
    """

    def __init__(self,initial_value,base_value):
        super().__init__()
        self._base_value = base_value
        self._value = initial_value

    def __repr__(self):
        return str(self._value)

    def __str__(self):
        return str(self._value)
    
    @property
    def _base_value(self):
        return self.__base_value

    @property
    def _value(self):
        return self.__value

    @_base_value.setter
    def _base_value(self,new_base:int or hex or oct):
        _Test_Cases._verify_attribute_set(self,"__base_value")
        if _Test_Cases._base_is_integer_value(new_base):
            self.__base_value = _Test_Cases._verify_and_set_base(new_base)
        else:
            self.__base_value = new_base

    @_value.setter
    def _value(self,new_value:int):
        _Test_Cases._verify_attribute_set(self,"__value")
        self.__value = self._convert_value(new_value)

    def _convert_value(self,value):
        value = _Convert._into[int](value)
        try:
            return _Convert._into[self._base_value](value)
        except KeyError:
            return self._into_base(value,self._base_value)

    @staticmethod
    def _into_hex(init_value:int):
        return hex(init_value)

    @staticmethod
    def _into_oct(init_value:int):
        return oct(init_value)

    @staticmethod
    def _into_int(init_value:int):
        _extracted_id = _Number_Struct._extract_base_id(init_value)
        return _Convert._from[_extracted_id](init_value)

    @staticmethod
    def _into_base(init_value:int,base:int):
        new_value = "".join(_Number_Struct._get_new_digits(init_value,base))
        return f"{base}b{new_value}"

    @staticmethod
    def _from_hex(value:hex):
        return int(value,base=16)

    @staticmethod
    def _from_oct(value:oct):
        return int(value,base=8)

    @staticmethod
    def _from_int(value:int):
        return value

    @staticmethod
    def _from_base(value:str):
        return int( _Number_Struct._extract_value(value),
                    base=_Number_Struct._extract_base_value(value))

    @staticmethod
    def _extract_base_id(value):
        try:
            return '0'+findall(r"[xob]",value)[0]
        except TypeError:
            return '00'

    @staticmethod
    def _extract_base_value(value):
        return int(findall(r"(\d+)b",value)[0])
    
    @staticmethod
    def _extract_value(value):
        return findall(r"b(\d+)",value)[0]

    @staticmethod
    def _get_new_digits(value:int,base:int):
        remainder_stack = _Test_Cases._verify_value_gt_zero(value)
        while value > 0:
            remainder_stack.insert(0,_Number_Struct._get_remainder(value,base))
            value //= base
        return remainder_stack

    @staticmethod
    def _get_remainder(value:int,modulo:int):
        return str(value % modulo)

class _Convert:

    _into = {
        int:_Number_Struct._into_int,
        hex:_Number_Struct._into_hex,
        oct:_Number_Struct._into_oct
    }

    _from = {
        "0x":_Number_Struct._from_hex,
        "0o":_Number_Struct._from_oct,
        "0b":_Number_Struct._from_base,
        "00":_Number_Struct._from_int
    }