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
    pass

class Bases:
    def __init__(self,base):
        self.base = base
        self.max_length = 0
    
    @Threader.addthread
    def convert(self,integer,fill_char='?',neg_char='x'):
        """
        Returns an integer as a base value.
        """

        if not type(integer) == int:
            raise ConversionError(
        "Invalid input for integer argument."+
        f" '{integer}' is either a string, float or already converted")

        remainder_stack = []
        integer = self.testNegative(integer)

        # If the integer value is a negative, insert neg_char into the remainder_stack
        if integer["negative"] == True:
            remainder_stack.insert(0,neg_char)
        integer = integer["integer"]

        # If the integer value is 0, replace insert fill_char into the remainder_stack;
        # Else if the integer is greater than 0, convert integer into the base and
        #   insert each value into the remainder_stack.
        if integer == 0:
            remainder_stack.insert(0,fill_char)
        elif integer > 0:
            while integer > 0:
                remainder = integer % self.base
                if remainder == 0:
                    remainder_stack.insert(0,fill_char)
                else:
                    remainder_stack.insert(0,str(remainder))
                integer = integer // self.base
        
        remainder_stack = self.testLength(remainder_stack,self.max_length,fill_char)
        
        # If the remainder_stack exceeds the max_length, set self.max_length to new max_length
        if remainder_stack["max_length"] > self.max_length:
            self.max_length = remainder_stack["max_length"]
        
        remainder_stack = remainder_stack["stack"]

        return "".join(remainder_stack)

    @staticmethod
    def testLength(stack,max_length=None,char='?',inserts=False):
        """
        Tests the length of the stack and returns a dict of the stack and the max_length.
        If the stack exceeds the max_length, a new max_length is returned.
        If the stack does not exceed the max_length, fill stack with additional characters.\n

        If inserts is True, ensure stack is equivalent to the max_length value by inserting
        chars to the stack.\n
        If inserts is False (default), test if stack exceeds max_length. 
        """
        return_values = {}
        return_values["stack"] = stack
        return_values["max_length"] = max_length

        if inserts == False:
            if len(stack) > max_length:
                return_values["max_length"] = len(stack)
                return return_values

        if inserts == True:
            while len(stack) < max_length:
                stack.insert(0,char)
            return_values["stack"] = stack
            
            return "".join(return_values["stack"])
        
        return return_values

    @staticmethod
    def testNegative(integer):
        """
        Tests if an integer value is negative and returns a dict of the integer and bool.
        If the integer is negative, it is returned at it's absolute value, boolean set to True.
        If the integer is positive, it is returned at it's absolute value, boolean set to False.
        """
        return_values = {"negative":False}
        return_values["integer"] = integer
        
        if integer < 0:
            integer_str = abs(integer)
            return_values["negative"] = True
            return_values["integer"] = integer_str

        return return_values

class ConversionError(Exception):
    """Raised if an integer string has already been converted"""

if __name__ == "__main__":
    print("Running Bases.py as <__main__>")
    from random import randint as rand

    numbers = []

    for i in range(5):
        base = rand(2,10)
        negative = rand(-1,1)
        integer = 42*negative

        next_number = Bases(base).baseConverter(integer)

        result = {"Base":base,"Integer":integer,"result":next_number}
        numbers.append(result)
    
    for i in numbers:
        print(i)
    
    for i in numbers:
        numbers.pop(numbers.index(i))

elif Config.show_run_test:
    print(f"{__name__} Running...")
