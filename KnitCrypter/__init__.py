try:
    from pkg_utils.handlemethod import handlemethod,pull_handler_log
    from pkg_utils._Assignment_Handler import _Assignment_Handler
except ModuleNotFoundError:
    from KnitCrypter.pkg_utils.handlemethod import handlemethod,pull_handler_log
    from KnitCrypter.pkg_utils._Assignment_Handler import _Assignment_Handler

__version__ = [3,0,0]
__all__ = ["knitpattern","equals","notequals"]

@handlemethod('debug')
def default(a):
    return a

@handlemethod('debug')
def equals(a,b):
    if a % b == 0:
        return a
    return a * -1

@handlemethod('debug')
def notequals(a,b):
    if a % b != 0:
        return a
    return a * -1

@handlemethod('debug')
def knitpattern(string,base,func=default,*args,**kwargs):
    return _Assignment_Handler(string,base,func,*args,**kwargs)