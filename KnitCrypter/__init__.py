try:
    from pkg_utils.handlemethod import handlemethod,pull_handler_log
    from pkg_utils._Assignment_Handler import _Assignment_Handler as __AH
    from pkg_utils._Context_Manager import _Context_Manager as __CM
    from pkg_utils.encrypt_utils.error_checks import _Encrypt_Errors as KCE
except ModuleNotFoundError:
    from KnitCrypter.pkg_utils.handlemethod import handlemethod,pull_handler_log
    from KnitCrypter.pkg_utils._Assignment_Handler import _Assignment_Handler as __AH
    from KnitCrypter.pkg_utils._Context_Manager import _Context_Manager as __CM
    from KnitCrypter.pkg_utils.encrypt_utils.error_checks import _Encrypt_Errors as KCE

__version__ = [3,0,0]
__all__ = ["KCE","knitpattern","knitcrypt"]

def default(a):
    return a

def equals(a,b):
    if a % b == 0:
        return a
    return a * -1

def notequals(a,b):
    if a % b != 0:
        return a
    return a * -1

class knitpattern(__AH):

    def __init__(self,string,base,func=default,*args,**kwargs):
        super().__init__(string,base,func,*args,**kwargs)

class knitcrypt(__CM):

    def __init__(self,path,pattern:knitpattern,**kwargs):
        super().__init__(path,pattern,**kwargs)