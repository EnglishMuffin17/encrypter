try:
    from error_checks._Dev_Cases import _verify_attribute_set
except ModuleNotFoundError:
    from .error_checks._Dev_Cases import _verify_attribute_set
finally:
    from string import ascii_lowercase

def _get_var_name(index:int):
    var_stack = []
    if index == 0:
        return ascii_lowercase[0]
    
    while index > 0:
        remainder = index % 26
        var_stack.insert(0,remainder)
        index = index // 26
    
    return "".join([ascii_lowercase[x] for x in var_stack])

class _Struct:

    """
    _Struct defines a function or method call, after it
    has been called. Recording the function name, its args
    and kwargs as a temporary log that can be called back during
    program execution.
    """
    
    def __init__(self,_id:int,func,*args,**kwargs):
        self.__id = _id
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs

    def __repr__(self):
        return f"{hex(self._id)}||{self._func}"

    @property
    def _id(self):
        return self.__id

    @property
    def _func(self):
        return self.__func

    @property
    def _args(self):
        return self.__args

    @property
    def _kwargs(self):
        return self.__kwargs

    @_args.setter
    def _args(self,values:list):
        _verify_attribute_set(self,"__args")
        _args_dict = {}
        
        for i in range(len(values)):
            key = _get_var_name(i)
            _args_dict[f"var_{key}"] = values[i]