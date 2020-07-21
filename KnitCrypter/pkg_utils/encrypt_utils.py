"""
Utility classes for KnitCrypter module.
contains:
    Config reader class - reads config file, distributes the
    requested section

    Debug class - Determines whether or not to print any 
    'debugging' statements to the console that come directly 
    from KnitCrypter.

    Cache class - Used to add desired function/method
    calls to the cache container at execution of module.

    Logging class

    Bases - converts numerical values from one base counting system
    into another

    Chars - defines characters for manipulation, reassignment, etc.
"""

import sqlite3,datetime
import os,json,string

_BASE_UNIT  = 1000 #Base unit of measuring data
_DATA_SIZE_CLASSES = { 
    "BT":_BASE_UNIT**0, #Bytes unit of measuring data
    "KB":_BASE_UNIT**1, #Kilobytes unit of measuring data
    "MB":_BASE_UNIT**2, #Megabytes unit of measuring data
    "GB":_BASE_UNIT**3, #Gigabytes unit of measuring data
    "TB":_BASE_UNIT**4, #Terabytes unit of measuring data
}

_LOG_LEVELS = { #Levels to evalutate debugging submissions
    "debug":0,
    "info":1,
    "warn":2,
    "error":3,
    "critical":4
}

_LOG_TAGS = {
    "debug":'[DEBUG]',
    "info":'[INFO]',
    "warn":'[WARN]',
    "error":'[ERROR]',
    "critical":'[CRITICAL]'
}

_cache_container = None #Placeholder for a _Container object in the 
                        # event cache is enabled

_print_count = -1 #Number of times a statement is printed to console

class _Console:

    """
    Handles the format console messages utilize
    """

    def __init__(self,message="Default message",delimiter="|"):
        self._message = message
        self._delimiter = delimiter

    def __repr__(self):
        return f"[{self._count}] {self._time} {self._delimiter} {self._message}"

    @property
    def _datetime(self):
        date_time = datetime.datetime.now()
        return date_time

    @property
    def _ctime(self):
        return self._datetime.ctime()

    @property
    def _date(self):
        return self._datetime.date()

    @property
    def _time(self):
        return self._datetime.time()

    @property
    def _count(self):
        global _print_count
        _print_count += 1
        return _print_count
    
    def _submit(self):
        print(self)

class _Struct:

    """
    _Struct defines a function or method call, after it
    has been called. Recording the function name, its args
    and kwargs as a temporary log that can be called back during
    program execution.
    """
    
    def __init__(self,_id:int,func,*args,**kwargs):
        self.__id = _id
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs

    def __repr__(self):
        return f"{hex(self._id)}||{self._func}"

    @property
    def _id(self):
        return self.__id

    @property
    def _func(self):
        return self.__func

    @property
    def _args(self):
        return self.__args

    @property
    def _kwargs(self):
        return self.__kwargs

    @_args.setter
    def _args(self,values:list):
        if self.__dict__.__contains__("__args"):
            raise AttributeError("arguments already set")

        _args_dict = {}

        for i in range(len(values)):
            key = _Struct._get_var_name(i)
            _args_dict[f"var_{key}"] = values[i]

    @staticmethod
    def _get_var_name(index:int):
        var_stack = []

        if index == 0:
            return string.ascii_lowercase[0]
        
        while index > 0:
            remainder = index % 26
            var_stack.insert(0,remainder)

            index = index // 26
        
        return "".join([string.ascii_lowercase[x] for x in var_stack])

class _Container:

    """
    Cache container class which holds a number of items
    no greater than the defined container size. _Container size
    is measured in bytes.
    """

    def __init__(self,max_size:int,size_mod:str):
        self.__container = []
        self.__struct_id = -1
        self.__init_size = self._container.__sizeof__()
        self.__max_size = max_size
        self.__size_mod = _DATA_SIZE_CLASSES[size_mod]

    def __repr__(self):
        return f"{self._container}"

    def __len__(self):
        return len(self._container)

    def __contains__(self,id_:int):
        
        _found_struct = self._search(id_)

        if _found_struct == None:
            return False

        if _found_struct._id == id_:
            return True
        return False

    def __iter__(self):
        return iter(self._container)
        
    def __getitem__(self,id_:int):
        return self._search(id_)

    @property
    def _container(self) -> list:
        return self.__container

    @property
    def _struct_id(self) -> int:
        self.__struct_id += 1
        return self.__struct_id

    @property
    def _init_size(self) -> int:
        return self.__init_size

    @property
    def _size(self) -> int:
        return self._container.__sizeof__() - self._init_size

    @property
    def _max_size(self) -> int:
        return self.__max_size

    @property
    def _check_cache(self):
        _max_size = self._max_size * self._size_mod
        
        if self._size > _max_size:
            return True
        return False

    @property
    def _size_mod(self) -> int:
        return self.__size_mod
    
    def _search(self,id_:int) -> _Struct:
        
        #Utilize a bit search algorithm to find the
        #desired _Struct object. Given the assignment
        #nature of _Container, a bit search is conducted
        #in reverse order

        def _bit_search(arr:list):
            pos = len(arr) // 2

            if arr[pos]._id != id_ and pos > 0:

                #If the selected object is greater than
                #the tarted id_, search from the first half
                if arr[pos]._id > id_:
                    return _bit_search(arr[pos:])
                    
                #If the selected object is less than the
                #targeted id_, search from the last half
                elif arr[pos]._id < id_:
                    return _bit_search(arr[:pos])
                
            elif arr[pos]._id == id_:
                return arr[pos]     
            else:
                return arr[-1]
                
        if len(self) > 0:
            return _bit_search(self._container)
    
    def _cleanup(self):
        while self._check_cache:
            self._remove_struct(-1)

    def _clear(self):
        while self._size > 0:
            self._remove_struct(-1)

    def _add_struct(self,func,*args,**kwargs):
        self._container.insert(0,
            _Struct(self._struct_id,func,*args,**kwargs))

    def _remove_struct(self,id_:int):
        if id_ == -1:
            self._container.pop(id_)
        elif id_ in self:
            _index = self._container.index(self._search(id_))
            self._container.pop(_index)

#Define Config reader class
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
        with open(self._path,"r") as jFile:
            contents = json.load(jFile)
        
        for key in contents:
            setattr(self,key,contents[key])
        
        del(contents)

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
        for key in _open_config:
            setattr(self,key,_open_config[key])
        
        del(_open_config)

    def __getattr__(self,attr):
        try:
            return self.__dict__[attr]
        except KeyError:
            pass

    @property
    def _config_info(self) -> dict:
        return _ConfigReader()["File_Information"]
        
#Define Debug class
class _Debug(_Utility):
    
    """
    Determines whether or not to print any 'debugging' statements
    to the console that come directly from KnitCrypter.

    For example, assuming debugging is enabled:

        - check to see what flags are declared inside of
        encrypt_config.json.

        - ensure declared flags are legal options, raise an error
        if there is an illegal or undefined flag.

        - return boolean value for whether or not any of the
        desired flags are declared in config.

    The following flags are to be considered 'legal':

        - *
        - bases
        - cache
        - chars
        - logging
        - threads

    Options to be aware of; Debugging_Options:

        - enable_debug_mode
        - debug_flags
    """

    def __init__(self):
        super().__init__("Debugging_Options")
        self.__flag_options = self._config_info["DEBUG_FLAG_OPTIONS"]

    @property
    def _flag_options(self) -> list:
        return self.__flag_options

    @staticmethod
    def _check_flags(*targets:str) -> bool:
        """
        Tests for whether or not the target flags are active.
        """

        #Test if debug_mode is set to True
        if not _Debug().enable_debug_mode:
            return False

        #Active flags defined in Debugging_Options
        _active_flags = _Debug().debug_flags

        #Available flags that can be made active
        _available_flags = _Debug()._flag_options

        #Total no. of active targets
        _active_targets = 0

        #Test if flags in _active_flags are valid
        for i in _active_flags:
            if not _available_flags.__contains__(i):
                raise AttributeError(f"{i} is not a legal flag")

        #Test _active_flags for none or all
        if len(_active_flags) < 1 and _print_count < 0:
            _Console("No flags declared")._submit()
            return False
        if _active_flags.__contains__("*"):
            return True
        
        #Test if target flags are active
        for i in targets:
            if not _available_flags.__contains__(i):
                raise AttributeError(f"{i} is not a legal flag")

            if _active_flags.__contains__(i):
                _active_targets += 1

        if _active_targets == 0:
            return False
        return True

#Define Cache class
class _Cache(_Utility):
    
    """
    Handles caching function calls during execution using the 
    '_insert' method. Items (_Struct objects) are created, inserted
    into the global container, then older items are removed if 
    necessary.
    """

    def __init__(self):
        super().__init__("Cache_Options")
        self._debug_enabled = _Debug()._check_flags("cache")

        global _cache_container
        if self.use_cache and _cache_container == None:
            _get_mod = self._config_info["CACHE_SIZE_MOD"]
            _cache_container = _Container(self.cache_size,_get_mod)

            if self._debug_enabled:
                _Console("Cache instantiated...")._submit()

    def __del__(self):
        return self._freeze()

    @property
    def _size(self):
        global _DATA_SIZE_CLASSES
        global _cache_container

        _s_mod = "BT"
        for mod in _DATA_SIZE_CLASSES:
            if _cache_container._size > _DATA_SIZE_CLASSES[mod]:
                _size_mod_assignment = mod
                continue
        _c_s = _cache_container._size // _DATA_SIZE_CLASSES[_s_mod]

        return f"{_c_s} {_s_mod}"
        
    def _insert(self,func,*args,**kwargs):
        if self.use_cache:
            global _cache_container
            _cache_container._add_struct(func,args,kwargs)

            if self._debug_enabled:
                _Console(f"Added {func} to local cache")._submit()

            if self.auto_cleanup and _cache_container._check_cache:
                _cache_container._cleanup()

                if self._debug_enabled:
                    _Console(
                        "Performed cleanup for local cache"
                        )._submit()
    
    def _clear(self):      
        if self.use_cache:
            global _cache_container
            _cache_container._clear()

            if self._debug_enabled:
                _Console(
                    "Local cache cleared successfully"
                    )._submit()
    
    def _freeze(self):
        if os.path.exists(self.cache_path) and self.use_cache:
            global _cache_container

            _title = _Console()._ctime
            _title = _title.replace(" ","_")
            _title = _title.replace(":","")

            cache_conn = sqlite3.connect(self.cache_path)
            cache_conn.execute(f"""
                                CREATE TABLE {_title}(
                                id_number INTEGER,
                                structure BLOB
                                ) 
                            """)

            for i in _cache_container:
                cache_conn.execute(f"""
                                INSERT INTO {_title} VALUES(
                                    {i._id},
                                    '{i}'
                                )
                                """)
            
            cache_conn.commit()
            cache_conn.close()

            if self._debug_enabled:
                _Console(
                    "Cache frozen to database sucessfully"
                )._submit()

#Define Logging class
class _Logger(_Utility):

    """
    If enabled, this utility handles logging of desired method
    or function calls, adding them to a designated table.
    """
    
    def __init__(self):
        super().__init__("Logging_Options")
        self._debug_enabled = _Debug()._check_flags("logging")

        if self.use_logger:
            if self._debug_enabled:
                _Console("Logger instantiated...")._submit()

            self._init_log()
    
    @property
    def _connection(self):
        return self.__connection

    @property
    def _connect(self):
        _connection_str = self.log_path+"log_data.db"
        if os.path.exists(_connection_str):
            self.__connection = sqlite3.connect(_connection_str)

    @property
    def _disconnect(self):
        if self.__dict__.__contains__("__connection"):
            self.__connection.close()
            del self.__connection

    @property
    def _log_table(self):
        return self.__log_table

    @_log_table.setter
    def _log_table(self,n:str):
        if not self.__dict__.__contains__("__log_table"):
            self.__log_table = n

    def _init_log(self):
        if self.use_logger:
            self._connect

            _title = _Console()._ctime
            _title = _title.replace(" ","_")
            _title = _title.replace(":","")

            self.__log_table = f"{_title}"
            
            #Create table to hold log submissions
            self._connection.execute(f"""
                                    CREATE TABLE {self._log_table}(
                                        entry_time DATETIME(50),
                                        method_id VARCHAR(150),
                                        arguments TEXT,
                                        keyword_arguments TEXT,
                                        return_values TEXT,
                                        entry_tag VARCHAR(10)
                                    )
                                    """)
            self._connection.commit()
            
            if self._debug_enabled:
                _Console(
                    f"Log {self._log_table} created sucessfully"
                    )._submit()
            self._disconnect

    def _submit_entry(self,level,func,r_value,*args,**kwargs):
        global _LOG_LEVELS
        global _LOG_TAGS

        if self.use_logger and (_LOG_LEVELS[level] >= 
            _LOG_LEVELS[self.log_level]):
            
            self._connect
            
            #submit a log entry to designated table
            self._connection.execute(f"""
                                    INSERT INTO '{self._log_table}'
                                    VALUES(
                                        '{_Console()._time}',
                                        '{func.__qualname__}',
                                        '{args}',
                                        '{kwargs}',
                                        '{r_value}',
                                        '{_LOG_TAGS[level]}'
                                    )
                                    """)
            self._connection.commit()

            if self._debug_enabled:
                _Console(
                    f"{func} call logged to table"
                )._submit()
            self._disconnect
    
    def _get_logs(self) -> list: 
        self._connect

        #pull the desired log table from log database
        _cursor = self._connection.execute(f"""
                                    SELECT name FROM sqlite_master
                                    WHERE type='table'
                                    """)
        _log_tables = [
            t[0] for t in _cursor.fetchall()
            if t[0] != "sqlite_sequence"
        ]

        if self._debug_enabled:
            _Console(
                "Pulled log tables from log database"
            )._submit()
        self._disconnect

        return _log_tables

    def _pull_log(self,log_table:str,to_file:bool=False): 
        if self._get_logs().__contains__(log_table):
            _pulled_log = self._extract_log(log_table)

            if to_file:
                self._init_file(log_table,_pulled_log)

        else:
            if self._debug_enabled:
                _Console(
                    "Could not find target log table"
                )._submit()
                return None
    
    def _extract_log(self,log_table:str) -> list:   
            self._connect

            _cursor = self._connection.execute(f"""
                                    SELECT * FROM {log_table}
                                    """)
            _pulled_log = [
                l for l in _cursor.fetchall()
            ]

            if self._debug_enabled:
                _Console(
                    f"Selected table {log_table} found"
                )._submit()
            self._disconnect

            return _pulled_log

    def _init_file(self,log_table_name:str,log_table_data:list):
        _file_path = self.log_file_path+log_table_name+".log"
        
        if os.path.exists(self.log_file_path):

            with open(_file_path,"w") as log_file:

                for e in log_table_data:
                    file_entry = f"{e[0]} {e[-1]} {e[1]}: args {e[2]}; kwargs {e[3]}; return {e[4]}"
                    log_file.write(file_entry+'\n')

            if self._debug_enabled:
                _Console(
                    "Created log file from table"
                )._submit()
        
#Define Bases class
class _Bases:
    
    def __init__(self):
        self._debug_enabled = _Debug()._check_flags("bases")

        if self._debug_enabled:
            _Console("Bases class instantiated...")._submit()

#Define Chars class
class _Characters:
    
    def __init__(self):
        self._debug_enabled = _Debug()._check_flags("chars")

        if self._debug_enabled:
            _Console("Characters class instantiated...")._submit()