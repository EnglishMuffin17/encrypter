try:
    from _Utility import _Utility
    from _Console import _Console
    from _Debug import _Debug
except ModuleNotFoundError:
    from ._Utility import _Utility
    from ._Console import _Console
    from ._Debug import _Debug
finally:
    from os import path
    import sqlite3

class _Logger(_Utility):

    """
    If enabled, this utility handles logging of desired method
    or function calls, adding them to a designated table.
    """

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
        if path.exists(_connection_str):
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
    def _log_table(self,t:str):
        if not self.__dict__.__contains__("__log_table"):
            self.__log_table = t

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

        if self.use_logger and (self._LOG_LEVELS[level] >= 
            self._LOG_LEVELS[self.log_level]):
            
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
                                        '{self._LOG_TAGS[level]}'
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
        
        if path.exists(self.log_file_path):

            with open(_file_path,"w") as log_file:

                for e in log_table_data:
                    file_entry = f"{e[0]} {e[-1]} {e[1]}: args {e[2]}; kwargs {e[3]}; return {e[4]}"
                    log_file.write(file_entry+'\n')

            if self._debug_enabled:
                _Console(
                    "Created log file from table"
                )._submit()