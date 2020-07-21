try:
    from _Console import _Console
except ModuleNotFoundError:
    from ._Console import _Console
finally:
    import json,os

class _ConfigReader:
    
    """
    Reads the config file, encrypt_config.json, and sets
    the data as object attributes.
    """

    _path:str = "KnitCrypter\\pkg_utils\\encrypt_config.json"

    def __init__(self):
        self._read_config()

    def __getitem__(self,attr):
        try:
            return self.__dict__[attr]
        except KeyError as err:
            _Console(
                f"{err} not found. Was {attr} defined?")._submit()
    
    def _read_config(self):
        """Reads json file then assigns contents as class attrs"""
        if _ConfigReader._verify_path_exists(self._path):
            with open(self._path,"r") as jFile:
                contents = json.load(jFile)
        
            for key in contents:
                setattr(self,key,contents[key])
        
            del(contents)
    
    @staticmethod
    def _verify_path_exists(path:str):
        return os.path.exists(path)