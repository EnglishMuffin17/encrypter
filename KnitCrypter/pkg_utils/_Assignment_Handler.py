try:
    from encrypt_utils._Number_Struct import _Number_Struct
    from encrypt_utils._Character_Struct import _Character_Struct
    from encrypt_utils.error_checks._Encrypt_Cases import _verify_sequence_pattern
except ModuleNotFoundError:
    from .encrypt_utils._Number_Struct import _Number_Struct
    from .encrypt_utils._Character_Struct import _Character_Struct
    from .encrypt_utils.error_checks._Encrypt_Cases import _verify_sequence_pattern

def _generate_values(string,base,func,*args,**kwargs):
    for step in range(len(string)):
        yield string[step], _Number_Struct(func(step,*args,**kwargs),base)

def _assign_values(generator):
    return_values = {}
    for i in generator:
        return_values[i[0]] = i[1]
    _verify_sequence_pattern(return_values)
    return return_values

def _extract_from_index(pattern:dict,index):
    return f"{list(pattern.keys())[index]}:{list(pattern.values())[index]}"


class _Assignment_Handler:

    def __init__(self,string:str,base:any,func,*args,**kwargs):
        generator = _generate_values(string,base,func,*args,**kwargs)
        self.__pattern = _assign_values(generator)
        self.__first = _extract_from_index(self.__pattern,0)
        self.__last = _extract_from_index(self.__pattern,-1)
    
    def __repr__(self):
        return f"({self.__first},...,{self.__last})"
    
    def __len__(self):
        return len(self.__pattern)
    
    def __iter__(self):
        return iter(self.__pattern)

    def __getitem__(self,key):
        return self.__pattern[key]

    def __reversed__(self):
        return sorted(self.__pattern,reverse=True)

    def __contains__(self,char):
        return self.__pattern.__contains__(char)