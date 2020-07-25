try:
    from _Utility import _Utility
    from _Console import _Console
    from error_checks._Dev_Cases import _verify_flag
except ModuleNotFoundError:
    from ._Utility import _Utility
    from ._Console import _Console
    from .error_checks._Dev_Cases import _verify_flag

class _Debug(_Utility):
    
    """
    Determines whether or not to print any 'debugging' statements
    to the console that come directly from KnitCrypter.

    For example, assuming debugging is enabled:

        - check to see what flags are declared inside of
        encrypt_config.json.

        - ensure declared flags are legal options, raise an error
        if there is an illegal or undefined flag.

        - return boolean value for whether or not any of the
        desired flags are declared in config.

    The following flags are to be considered 'legal':

        - *
        - bases
        - cache
        - chars
        - logging
        - threads

    Options to be aware of; Debugging_Options:

        - enable_debug_mode
        - debug_flags
    """

    def __init__(self):
        super().__init__("Debugging_Options")
        self.__flag_options = self._config_info["DEBUG_FLAG_OPTIONS"]

    @property
    def _flag_options(self) -> list:
        return self.__flag_options

def _verify_flags(flag_array:list):
    _available_flags = _Debug()._flag_options
    for i in flag_array:
        _verify_flag(_available_flags,i)

def _check_for_all_or_none(flag_array:list) -> bool:
    if len(flag_array) < 1 and _Console._print_count() < 0:
        _Console("No flags declared")._submit()
        return False
    if flag_array.__contains__("*"):
        return True
    
def _compare_flags(flag_array:list,targets):
    _active_targets = 0
    for i in targets:
        if flag_array.__contains__(i):
            _active_targets += 1
    
    if _active_targets == 0:
        return False
    return True

def _check_flags(*targets:str) -> bool:
    if not _Debug().enable_debug_mode:
        return False
    
    _active_flags = _Debug().debug_flags
    _all_or_none = _check_for_all_or_none(_active_flags)
    
    if _all_or_none == None:
        _verify_flags(_active_flags)
        _verify_flags(targets)
        return _compare_flags(_active_flags,targets)
    
    return _all_or_none