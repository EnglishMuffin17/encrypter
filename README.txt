README file for encrypter.py

encrypter.py version no. 1.0

to start, import encrypter.py as follows:
"from encrypter import encrypter"

Dependancies:

    - #Builtins
        encrypter uses a small number of dependencies
        for utilities and debugging purposes:

        1. threading
        2. queue
        3. string
        4. math
        5. os

    - pkg_utils
        encrypter defines three dependencies as utiliy functions:

        1. encrypt_threader
        2. encrypt_logger
        3. encrypt_config

    - classes
        enrypter defines the following classes to handle 'under the hood'
        functions that the main encrypt file (encrypt.py) uses:

        1. Chars
        2. Bases

    - encrypter.py classes
        Utilizing the dependencies, encrypter defines three classes for user purposes:

        1. EncryptLogger
        2. baseConverter
        3. CharGenerator

EncryptLogger - class
    EncryptLogger utilizes encrypt_logger.py to handle logging events.
    If log_enabled set to True, any methods/functions with the
    '@Logger.submitEvent' decorator will submit event calls to the defined
    log.

    @Logger.submitEvent can accept one additional keyword argument, 'log_level'
    log_level, by default is "info" but can be changed as follows.

    '@Logger.submitEvent("debug")'

    For further information, look into the logger module documentation on how to
    configure EncryptLogger properly.

    methods:

        1. start
            Initiates EncryptLogger to setup logger

            arguments:
                takes no arguments.

        2. configureLogger
            configures the logger to make ready for submit requests.

            arguments:
                path - set the path logs will be instatiated
                title - set the name of the log
                format_ - set the format logs will be displayed
                log_enabled - True by default. set whether or not a log
                will be instatiated
                log_level - "info" by default. set what level submit requests
                will be accepted

BaseConverter - class
    BaseConvert utilizes the Bases class in Bases.py to handle base conversion.
    Instatiation of BaseConverter requires a base value in it's constructor.

    methods:

        1. baseConverter
            Using the base value in the constructor, baseConverter takes an integer
            value then returns a new integer counting from the base value. The new
            value is then returned as a string object with filler and negative
            replacement characters.

            arguments:
                integer - any integer value between inf and (-inf)
                fill_char - '?' by default. a single character value to replace 0s 
                in the stack
                neg_char - 'x' by default. a single character value to represent 
                a negative value
        
        2. testLength
            Tests the length of a stack (integer string value sliced in an array)
            comparing it to the current max_length. If inserts is equal to False,
            testLength only tests the length of the stack versus max_length. If inserts
            is equal to True, testLength fills the diffence (empty space) between the
            length of max_length and the stack.

            arguments:
                stack - array of integer string values
                max_length - integer value to compare the length of stack
                char - replacement character for if inserts is equal to True 
                inserts - False by default. Determines whether or not testLength will
                only test the length of a stack or fill the stack with replacement chars.

        3. getMaxLength
            Returns the current maximum length for the BaseConverter object.

            arguments:
                takes no arguments.        
            
CharGenerator - class
    CharGenerator utilizes the Chars class in Chars.py to handle key/value assignment.

    CHARACTERS - dictionary
        The CHARACTERS dictionary holds string arrays, as make ready for encryption.
        The arrays are as follows:

            "UPPER_ALPHA" - a string of upper case letters
            "LOWER_ALPHA" - a string of lower case letters
            "PUNCTUATION" - a string of punctuation and syntax characters
            "DIGITS" - a string of digits 0-9
            "WHITESPACE" - a single character of " " as the place holder

    methods:

        1. getCharacters
            Returns either all string arrays from CHARACTERS or just the specified string.

            arguments:
                characters_list - None by default. If None, return all; else returns specific
                string

        2. strand
            Returns a new dictionary of key/value pairs where the keys are the chars from
            the CHARACTERS specified array, and the values are the integers from the
            character_values specified array.

            argurments:
                knit_list_id - shared key_name in CHARACTERS and character_values
                to be merged

        3. strandAll
            Utilizes merge method to merge CHARACTERS arrays to thier respective values
            from character_values.

            arguments:
                takes no arguments.

        4. setAllStitches
            Generates values for all CHARACTERS arrays using the same knit_pattern.

            {NOTICE} each CHARACTERS array will start from 0 and increment using the
            same pattern. Recommended to use BaseConverter().baseConverter() for each array
            with either different fill and neg chars, or different base counting values.

            arguments:
                knit_pattern - determines how internal method 'knit_pattern' handles
                value generation
                **kwargs - Refer to setValue for further documentation

        5. setStitch
            Returns a set of values based on the length of a specific array. Each value
            is generated based on a defined pattern.

            arguments:
                knit_pattern - method of operation that dictates change
                knit_list - list or dictionary to be iterated through
                STEP - increment value for each iteration
                OFFSET - change value for certain knit_paterns (SIN,COS,POW,INVERSE,EQUALS,NOTEQUALS)
                ROTATION - integer that dictates if the list is rotated before
                returned for assignment

            knit_patterns:
                HEX - returns a hexidecimal value of an integer
                OCT - returns an octodecimal value of an integer
                SIN - returns the ceiling sin value of an integer, multiplied by the given OFFSET
                COS - returns the ceiling cos value of an integer, multiplied by the given OFFSET
                POW - returns a given integer multiplied to the power of the given OFFSET 
                INVERSE - returns the ceiling inverse value of an integer, multiplied by the given OFFSET
                EQUALS - alternates a given value between itself and it's opposite if the 
                given integer % the given OFFSET equals 0
                NOTEQUALS - inverse of EQUALS

        6. getStrandedDict
                Returns stranded_dict if the dictionary has been merged sucessfully.

                arguments:
                    takes no arguments.
