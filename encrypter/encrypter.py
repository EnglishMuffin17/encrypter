try:
    from encrypter.pkg_utils.encrypt_config import Config
    from encrypter.Bases import Bases
    from encrypter.Chars import Chars
    from encrypter.pkg_utils.encrypt_logger import Logger
except ModuleNotFoundError:
    from pkg_utils.encrypt_config import Config
    from Bases import Bases
    from Chars import Chars
    from pkg_utils.encrypt_logger import Logger
finally:
    #Builtins
    pass

class EncryptLogger(Logger):
    def start(self):
        return super().start()
    
    def configureLogger(self,*args,**kwargs):
        return super().configureLogger(*args,**kwargs)

class BaseConverter(Bases):
    @Logger.submitEvent
    def __init__(self,base):
        return super().__init__(base)
    
    @Logger.submitEvent
    def baseConverter(self,*args,**kwargs):
        return super().baseConverter(*args,**kwargs)
    
    @Logger.submitEvent
    def testLength(self,*args,**kwargs):
        return super().testLength(*args,**kwargs)
    
    @Logger.submitEvent
    def getMaxLength(self):
        return self.max_length

class CharGenerator(Chars):
    @Logger.submitEvent
    def __init__(self,run_check=True):
        return super().__init__(run_check)
    
    @Logger.submitEvent
    def merge(self,knit_list_id):
        return super().merge(knit_list_id)

    @Logger.submitEvent
    def mergeAll(self):
        return super().mergeAll()

    @Logger.submitEvent
    def setAllValues(self,*args,**kwargs):
        return super().setAllValues(*args,**kwargs)
    
    @Logger.submitEvent
    def setValue(self,*args,**kwargs):
        return super().setValue(*args,**kwargs)
    
    def getMergedDict(self):
        
        @Logger.submitEvent
        def returnDict():
            return self.merged_dict

        @Logger.submitEvent(log_level='warn')
        def returnDictWarning():
            print(f"[WARN] {self.__class__} merged_dict has not been made ready")
            print("returning None")

        if len(self.merge_dict) > 0:
            return returnDict()
        else:
            return returnDictWarning()

if __name__ == "__main__":
    print("Running from encrypter.py as <__main__>")

else:
    if Config.show_run_test:
        print(f"{__name__} Running...")
    
    if Config.use_config_logger:
        EncryptLogger.configureLogger(
            Config.config_log_path,
            Config.config_log_title,
            Config.config_log_format,
            Config.config_log_enabled,
            Config.config_log_level
            )