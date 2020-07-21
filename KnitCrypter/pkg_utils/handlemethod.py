try:
    from development_utils._Cache import _Cache
    from development_utils._Logger import _Logger
    from development_utils._Debug import _Debug
    from development_utils._Console import _Console
except ModuleNotFoundError:
    from .development_utils._Cache import _Cache
    from .development_utils._Logger import _Logger
    from .development_utils._Debug import _Debug
    from .development_utils._Console import _Console

class handlemethod:

    _cache_handler = _Cache()
    _logging_handler = _Logger()

    def __init__(self,log_level:str='debug',debug_flags:[str]=('module')):
        self._log_level = log_level
        self._debug_enabled = _Debug()._check_flags(*debug_flags)

    def __call__(self,func):

        def _handle(*args,**kwargs):
            func_call = func(*args,**kwargs)

            self._cache_handler._insert(func,*args,**kwargs)
            self._logging_handler._submit_entry(
                        self._log_level,
                        func,
                        func_call,
                        *args,
                        **kwargs
                    )

            if self._debug_enabled:
                _Console(
                    f"'{func.__qualname__}' handled with output '{func_call}'"
                )._submit()
            return func_call

        return _handle

handlemethod()