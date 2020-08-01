try:
    from encrypt_utils._File_Struct import _File_Struct
    from encrypt_utils.error_checks._Encrypt_Cases import _verify_attribute_set
except ModuleNotFoundError:
    from .encrypt_utils._File_Struct import _File_Struct
    from .encrypt_utils.error_checks._Encrypt_Cases import _verify_attribute_set

class _Context_Manager:

    def __init__(self,path,pattern,encoding='UTF-8'):
        self.__file = _File_Struct(path,pattern,encoding)

    def __enter__(self):
        return self.__file

    def __exit__(self,exception_type,exception_value,trace):
        self.__file.close()