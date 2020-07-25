try:
    from _Utility import _Utility
    from _Console import _Console
    from _Debug import _check_flags
except ModuleNotFoundError:
    from ._Utility import _Utility
    from ._Console import _Console
    from ._Debug import _check_flags
finally:
    from os import path
    import sqlite3

_entry = lambda e:f"{e[0]} {e[-1]} {e[1]}: args {e[2]}; kwargs {e[3]}; return {e[4]}"

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
    
    def __init__(self,create_log=True):
        super().__init__("Logging_Options")
        self._debug_enabled = _check_flags("logging")

        if self.use_logger and create_log:
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
                                        method_id TEXT,
                                        arguments TEXT,
                                        keyword_arguments TEXT,
                                        return_values TEXT,
                                        entry_tag TEXT
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
            
            try:
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
            except sqlite3.OperationalError:
                self._connection.execute(f"""
                                        INSERT INTO '{self._log_table}'
                                        VALUES(
                                            '{_Console()._time}',
                                            '{func.__qualname__}',
                                            '',
                                            '',
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
    
def _get_logs() -> list: 
    database_agent = _Logger(False)
    database_agent._connect

    _cursor = database_agent._connection.execute(f"""
                                SELECT name FROM sqlite_master
                                WHERE type='table'
                                """)
    _log_tables = [
        t[0] for t in _cursor.fetchall()
        if t[0] != "sqlite_sequence"
    ]

    if database_agent._debug_enabled:
        _Console("Pulled log tables from log database")._submit()
    database_agent._disconnect

    return _log_tables

def _pull_log(log_table:str,to_file:bool=False):
    database_agent = _Logger(False)
    found_table = _get_logs().__contains__(log_table)

    if found_table and to_file == True:
        return _init_file(log_table,_extract_log_data(log_table))    
    
    elif found_table and to_file == False:
        return _extract_log_data(log_table)
    
    elif database_agent._debug_enabled:
        _Console("Could not find target log table")._submit()

def _extract_log_data(log_table:str) -> list:  
    database_agent = _Logger(False)
    database_agent._connect

    _cursor = database_agent._connection.execute(f"SELECT * FROM {log_table}")
    _pulled_log = [l for l in _cursor.fetchall()]

    if database_agent._debug_enabled:
        _Console(f"Selected table {log_table} found")._submit()
    database_agent._disconnect

    return _pulled_log

def _init_file(log_table_name:str,log_table_data:list):
    database_agent = _Logger(False)
    _file_path = database_agent.log_file_path+log_table_name+".log"
        
    if path.exists(database_agent.log_file_path):
        with open(_file_path,"w") as log_file:
            for e in log_table_data:
                log_file.write(_entry(e)+'\n')

        if database_agent._debug_enabled:
            _Console("Created log file from table")._submit()