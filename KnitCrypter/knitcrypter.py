try:
    from KnitCrypter.pkg_utils.encrypt_config import Config
    from KnitCrypter.Bases import Bases
    from KnitCrypter.Chars import Chars
    from KnitCrypter.pkg_utils.encrypt_logger import Logger
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
    """
    Handles base conversion using a base counter value in the constructor
    """
    @Logger.submitEvent
    def __init__(self,base):
        return super().__init__(base)
    
    @Logger.submitEvent
    def baseConverter(self,integer,**kwargs):
        """
        integer - any integer value\n
        fill_char - replacement char for 0s\n
        neg_char - replacement char for negative sign\n
        """
        return super().baseConverter(integer,**kwargs)
    
    @Logger.submitEvent
    def testLength(self,stack,max_length,*args,**kwargs):
        """
        stack - array of integer string values\n
        max_length - integer value to compare the lenght of stack\n
        char - replacement character for if inserts is True\n
        inserts - boolean. dictates whether or not to insert replacement chars\n
        """
        return super().testLength(stack,max_length,*args,**kwargs)
    
    @Logger.submitEvent
    def getMaxLength(self):
        return self.max_length

class CharGenerator(Chars):
    """
    Handles generating string/integer pairs for encryption keys
    """
    @Logger.submitEvent
    def __init__(self):
        return super().__init__()
    
    @Logger.submitEvent
    def getCharacters(self,characters_list=None):
        """
        characters_list - returns either all or the specified string
        from CHARACTERS
        """
        return super().getCharacters(characters_list)
    
    @Logger.submitEvent
    def strand(self,knit_list_id):
        """
        knit_list_id - shared key_name between CHARACTERS and character_values
        """
        return super().strand(knit_list_id)

    @Logger.submitEvent
    def strandAll(self):
        return super().mergeAll()

    @Logger.submitEvent
    def setAllStitches(self,*args,**kwargs):
        """
        knit_pattern - method of operation that dictates change\n
        knit_list - string iterable (list,dict,string)\n
        STEP - increment value for each iteration\n
        OFFSET - change value for certain knit_patterns (SIN,COS,POW,
        INVERS,EQUALS,NOTEQUALS)\n
        ROTATION - integer that dictates if the list is rotated before 
        assignment\n
        """
        return super().setAllValues(*args,**kwargs)
    
    @Logger.submitEvent
    def setStitch(self,*args,**kwargs):
        """
        knit_pattern - method of operation that dictates change\n
        knit_list - string iterable (list,dict,string)\n
        STEP - increment value for each iteration\n
        OFFSET - change value for certain knit_patterns (SIN,COS,POW,
        INVERS,EQUALS,NOTEQUALS)\n
        ROTATION - integer that dictates if the list is rotated before 
        assignment\n
        """
        return super().setStitch(*args,**kwargs)
    
    def getStrandedDict(self,knit_list_id=None):
        
        @Logger.submitEvent
        def returnDict():
            if knit_list_id == None:
                return self.stranded_dict
            return self.stranded_dict[knit_list_id]

        @Logger.submitEvent
        def returnDictWarning():
            print(f"[WARN] {self.__class__} merged_dict has not been made ready")
            print("returning None")

        if len(self.stranded_dict) > 0:
            return returnDict()
        else:
            return returnDictWarning()

if __name__ == "__main__":
    print("Running from KnitCrypter.py as <__main__>")

else:
    if Config.show_run_test:
        print(f"{__name__} Running...")
    
    if Config.use_config_logger:
        EncryptLogger().configureLogger(
            Config.config_log_path,
            Config.config_log_title,
            Config.config_log_format,
            Config.config_log_enabled,
            Config.config_log_level
            )
            
        EncryptLogger().start()
    
    CharGenerator().getCharacters()