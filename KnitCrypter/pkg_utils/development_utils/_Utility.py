try:
    from _ConfigReader import _ConfigReader
except ModuleNotFoundError:
    from ._ConfigReader import _ConfigReader

class _Utility:

    """
    Base encrypter_util class
    
    Looks for the appropriate section of encrypt_config.json
    to distribute attributes of the child class.

    Child classes are listed below:

        - _Debug
        - _Cache
        - _Threader
        - _Logger

    """

    def __init__(self,config:str):
        _open_config = _ConfigReader()[config]
        try:
            for key in _open_config:
                setattr(self,key,_open_config[key])
        except TypeError:
            print(_open_config)
        
        del(_open_config)

    def __getattr__(self,attr):
        try:
            return self.__dict__[attr]
        except KeyError:
            pass

    @property
    def _config_info(self) -> dict:
        return _ConfigReader()["File_Information"]