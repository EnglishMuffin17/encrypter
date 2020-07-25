try:
    from _Utility import _Utility
    from _Debug import _check_flags
    from _Console import _Console
    from _Container import _Container
except ModuleNotFoundError:
    from ._Utility import _Utility
    from ._Debug import _check_flags
    from ._Console import _Console
    from ._Container import _Container
finally:
    from os import path
    import sqlite3

class _Cache(_Utility):
    
    """
    Handles caching function calls during execution using the 
    '_insert' method. Items (_Struct objects) are created, inserted
    into the global container, then older items are removed if 
    necessary.
    """

    _BASE_UNIT  = 1000 #Base unit of measuring data
    _DATA_SIZE_CLASSES = { 
        "BT":_BASE_UNIT**0, #Bytes unit of measuring data
        "KB":_BASE_UNIT**1, #Kilobytes unit of measuring data
        "MB":_BASE_UNIT**2, #Megabytes unit of measuring data
        "GB":_BASE_UNIT**3, #Gigabytes unit of measuring data
        "TB":_BASE_UNIT**4, #Terabytes unit of measuring data
    }

    _cache_container = None #Placeholder for a _Container object in the 
                        # event cache is enabled

    def __init__(self):
        super().__init__("Cache_Options")
        self._debug_enabled = _check_flags("cache")

        if self.use_cache and self._cache_container == None:
            _get_mod = self._config_info["CACHE_SIZE_MOD"]
            self._cache_container = _Container(self.cache_size,_get_mod)

            if self._debug_enabled:
                _Console("Cache instantiated...")._submit()

    def __del__(self):
        return self._freeze()

    @property
    def _size(self):

        _s_mod = "BT"
        for mod in self._DATA_SIZE_CLASSES:
            if self._cache_container._size > self._DATA_SIZE_CLASSES[mod]:
                _size_mod_assignment = mod
                continue
        _c_s = self._cache_container._size // self._DATA_SIZE_CLASSES[_s_mod]

        return f"{_c_s} {_s_mod}"
        
    def _insert(self,func,*args,**kwargs):
        if self.use_cache:
            self._cache_container._add_struct(func,args,kwargs)

            if self._debug_enabled:
                _Console(f"Added {func} to local cache")._submit()

            if self.auto_cleanup and self._cache_container._check_cache:
                self._cache_container._cleanup()

                if self._debug_enabled:
                    _Console(
                        "Performed cleanup for local cache"
                        )._submit()
    
    def _clear(self):      
        if self.use_cache:
            self._cache_container._clear()

            if self._debug_enabled:
                _Console(
                    "Local cache cleared successfully"
                    )._submit()
    
    def _freeze(self):
        if path.exists(str(self.cache_path)) and self.use_cache:

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

            for i in self._cache_container:
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