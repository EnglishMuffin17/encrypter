try:
    from _Dev_Errors import *
except ModuleNotFoundError:
    from ._Dev_Errors import *
finally:
    from os.path import exists

def _verify_flag(flag_array:list,flag):
    if not flag_array.__contains__(flag):
        raise FlagError(flag,reason=0)
    
def _verify_path_exists(path:str):
    if exists(path):
        return True
    raise FileNotFoundError(f"file path {path} could not be located")

def _verify_attribute_exists(o:object,attribute):
    if o.__dict__.__contains__(attribute):
        return True
    attr_name = attribute.strip("_")
    raise AttributeError(f"attribute '{attr_name}' has not been set")

def _verify_attribute_set(o:object,attribute):
    if o.__dict__.__contains__(attribute):
        attr_name = attribute.strip("_")
        raise AttributeError(f"attribute '{attr_name}' has already been set")