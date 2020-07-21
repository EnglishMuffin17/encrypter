try:
    from _Encrypt_Errors import *
except ModuleNotFoundError:
    from ._Encrypt_Errors import *

def _extract_type(o:object):
    return str(o.__class__).strip(" <clas>")

class _Test_Cases:

    @staticmethod
    def _verify_value_gt_zero(value:int):
        if value > 0:
            return []
        return '0'

    @staticmethod
    def _base_is_integer_value(desired_base):
        return desired_base == int and type(desired_base) != type
    
    @staticmethod
    def _verify_and_set_base(base:int):
        if base in range(2,11):
            return base
        raise ValueError(f"Base '{base}' not within inclusive range 2-10")

    @staticmethod
    def _verify_char_value(char):
        type_name = _extract_type(char)
        if type(char) != str or len(char) > 1:
            raise TypeError(f"expected 'char' not '{type_name}'")
    
    @staticmethod
    def _verify_attribute_set(o:object,attribute):
        if o.__dict__.__contains__(attribute):
            attr_name = attribute.strip("_")
            raise AttributeError(f"attribute '{attr_name}' has already been set")
    
    @staticmethod
    def _verify_sequence_pattern(sequence:dict):
        sequence = list(sequence.values())
        for i in range(len(sequence)):
            for j in range(len(sequence)):
                if sequence[i] == sequence[j] and i != j:
                    raise SequenceError(sequence,reason=0)