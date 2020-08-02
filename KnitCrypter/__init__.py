from KnitCrypter.pkg_utils._Assignment_Handler import _Assignment_Handler
from KnitCrypter.pkg_utils._Context_Manager import _Context_Manager
from KnitCrypter.pkg_utils.encrypt_utils.error_checks import _Encrypt_Errors
from KnitCrypter.pkg_utils import algorithm_utils as Algorithms

__version__ = [2, 0, 8]
__all__ = ["_Encrypt_Errors", "Algorithms", "knitpattern", "knitcrypt"]


class knitpattern(_Assignment_Handler):

    def __init__(self, string, base, func=Algorithms.default, *args, **kwargs):
        super().__init__(string, base, func, *args, **kwargs)


class knitcrypt(_Context_Manager):

    def __init__(self, path, pattern: knitpattern, **kwargs):
        super().__init__(path, pattern, **kwargs)
