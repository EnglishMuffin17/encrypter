try:
    from encrypter.pkg_utils.encrypt_config import Config
    from encrypter.pkg_utils.encrypt_threader import Threader
    from encrypter.pkg_utils.encrypt_logger import Logger
except ModuleNotFoundError:
    from pkg_utils.encrypt_config import Config
    from pkg_utils.encrypt_threader import Threader
    from pkg_utils.encrypt_logger import Logger
finally:
    #Builtins
    import string
    import math

class Chars:

    CHARACTERS = {
            "UPPER_ALPHA":(string.ascii_uppercase),
            "LOWER_ALPHA":(string.ascii_lowercase),
            "PUNCTUATION":(string.punctuation),
            "DIGITS":(string.digits),
            "WHITESPACE":(" ")
        }
    
    def __init__(self):

        self.character_values = {}
        self.merged_dict = {}

        if Config.show_console:
            self.getCharacterCheck()

    @classmethod
    def getCharacterCheck(cls):
        init_character_count = 0

        print("Testing character count...")
        for i in cls.CHARACTERS:
            i_length = len(cls.CHARACTERS[i])
            init_character_count += i_length
            print(f"{i}: {cls.CHARACTERS[i]} --: {i_length} chars")
        
        print(f"Character count: {init_character_count} chars")
    
    @classmethod
    def getCharacters(cls,character_list=None):
        """
        Get a specific array, or all if None is specified
        """
        if character_list == None:
            return cls.CHARACTERS
        else:
            return cls.CHARACTERS[character_list]

    @Threader.addthread
    def merge(self,knit_list_id):
        """
        Merge CHARACTERS and character_values into a new dict, add to merged_dict
        """

        # Test to ensure knit_list_id exists inside of CHARACTERS and character_values
        # if not, raise KnitPatternNotSet 
        if not self.character_values.get(knit_list_id):
            raise KnitPatternNotSet(f"{knit_list_id} does not exist in character_values")
        
        elif not self.CHARACTERS.get(knit_list_id):
            raise KnitPatternNotSet(f"{knit_list_id} does not exist in CHARACTERS")
        
        char_keys = []
        char_vals = []
        new_dict = {}

        for i in self.CHARACTERS[knit_list_id]:
            char_keys.append(i)
        
        for i in self.character_values[knit_list_id]:
            char_vals.append(i)
        
        for i in char_keys:
            new_dict[i] = char_vals[char_keys.index(i)]
        
        self.merged_dict[knit_list_id] = new_dict

        return new_dict

    def mergeAll(self):
        for i in self.CHARACTERS:
            self.merge(i)            

    def setAllValues(self,knit_pattern,**kwargs):
        """
        Calculate and return the values attributed to the characters
        """

        # Grab any kwargs from method call
        # Ensure kwargs are valid for calling knit_patterns
        fields = {"STEP":1,"OFFSET":2,"ROTATION":0}
        for key in kwargs:
            if fields.__contains__(key):
                fields[key] = kwargs[key]

        # For each array in CHARACTERS get a new set of values to be merged later
        for i in self.CHARACTERS:
            next_value_array = self.knit_patterns(knit_pattern,i,
                    fields["STEP"],fields["OFFSET"],fields["ROTATION"])
            self.character_values[i] = next_value_array

        return self.character_values

    def setValue(self,knit_pattern,knit_list,**kwargs):
        """
        Calculate and return the values of a specified array
        """

        # Grab any kwargs from method call
        # Ensure kwargs are valid for calling knit_patterns
        fields = {"STEP":1,"OFFSET":2,"ROTATION":0}
        for key in kwargs:
            if fields.__contains__(key):
                fields[key] = kwargs[key]

        # Call knit_pattern method with kwargs
        # Assign knit_pattern to character_values dict
        knit_pattern = self.knit_patterns(knit_pattern,knit_list,
                fields["STEP"],fields["OFFSET"],fields["ROTATION"])
        self.character_values[knit_list] = knit_pattern
        
        return knit_pattern
    
    @Threader.addthread
    def knit_patterns(self,knit_pattern,knit_list,
                        STEP=1,OFFSET=2,ROTATION=0):
        """
        Returns a set of values based on the length of a specified array.\n
        knit_pattern --> method of operation that dictates change.\n
        knit_list --> list or dictionary item to be iterated through.\n
        STEP --> determines the increments per iteration.\n
        OFFSET --> test value for certain knit_patterns (POW, EQUALS, and NOTEQUALS);
        in POW, OFFSET dictates the power n is multiplied to
        """

        # Try to grab an existing array from CHARACTERS dict
        # If none exists, grab a knit_list_id
        try:
            knit_list_id = knit_list
            knit_list = self.CHARACTERS[knit_list]
        except TypeError:
            knit_list_id = knit_list.__class__

        init_step = 0
        list_length = len(knit_list)
        knit_values = []

        # Alternates a given value between itself and it's opposite
        # if the given integer % the given OFFSET equals 0 or not
        def EQUALS(integer):
            if integer % OFFSET == 0:
                return integer
            else:
                return integer*-1

        # Inverse of EQUALS
        def NOTEQUALS(integer):
            if integer % OFFSET != 0:
                return integer
            else:
                return integer*-1

        knit_patterns = {
            "HEX":lambda integer: hex(integer),
            "OCT":lambda integer: oct(integer),
            "SIN":lambda integer: math.ceil(math.sin(integer)*OFFSET),
            "COS":lambda integer: math.ceil(math.cos(integer)*OFFSET),
            "POW":lambda integer: integer**OFFSET,
            "INVERSE":lambda integer: math.ceil((integer*-1)*OFFSET),
            "EQUALS":EQUALS,
            "NOTEQUALS":NOTEQUALS
        }
        
        # Create a list of values using the defined args and kwargs defined abouve
        if Config.show_console:
            print(f"Attempting to {knit_pattern}ify values for {knit_list_id}")
            print(f"{knit_list_id} <list> length: {list_length}")
        for i in range(list_length):
            next_value = init_step
            init_step += STEP
            knit_values.append(knit_patterns[knit_pattern](next_value))

        # If ROTATION is not equal to zero, rotate the list accordingly
        if ROTATION < 0:
            ROTATION = len(knit_values) - abs(ROTATION)

        for i in range(ROTATION):
            temporary_value = knit_values[0]
            knit_values.pop(0)
            knit_values.append(temporary_value)

        knit_values = list(dict.fromkeys(knit_values))

        if Config.show_console:
            print(f"{knit_list_id} <values> length: {len(knit_values)}")

        if list_length != len(knit_values):
            raise KnitValueError(f"{knit_list_id} <list> and <values> are not the same length")

        return knit_values

class KnitPatternNotSet(Exception):
    @Logger.submitEvent
    def __init__(self):
        super().__init__()
    """Raised when a merge occurs but there is no knit_pattern set"""

class KnitValueError(Exception):
    @Logger.submitEvent
    def __init__(self):
        super().__init__()
    """Raised when knit_pattern method call has invalid output"""

if __name__ == "__main__":
    print("Running from Chars.py as <__main__>")
    char_test = Chars()

    alpha_upper = Chars().setValue("SIN","UPPER_ALPHA",STEP=1,ROTATION=0,OFFSET=10000)
    alpha_lower = Chars().setValue("COS","LOWER_ALPHA",STEP=1,ROTATION=0,OFFSET=10000)

    print(alpha_upper)
    print(alpha_lower)

    char_test.setValue("HEX","UPPER_ALPHA")
    char_test.merge("UPPER_ALPHA")

elif Config.show_run_test:
    print(f"{__name__} Running...")