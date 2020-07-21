try:
    from _Struct import _Struct
except ModuleNotFoundError:
    from ._Struct import _Struct

class _Container:

    """
    Cache container class which holds a number of items
    no greater than the defined container size. _Container size
    is measured in bytes.
    """

    _BASE_UNIT  = 1000 #Base unit of measuring data
    _DATA_SIZE_CLASSES = { 
        "BT":_BASE_UNIT**0, #Bytes unit of measuring data
        "KB":_BASE_UNIT**1, #Kilobytes unit of measuring data
        "MB":_BASE_UNIT**2, #Megabytes unit of measuring data
        "GB":_BASE_UNIT**3, #Gigabytes unit of measuring data
        "TB":_BASE_UNIT**4, #Terabytes unit of measuring data
    }

    def __init__(self,max_size:int,size_mod:str):
        self.__container = []
        self.__struct_id = -1
        self.__init_size = self._container.__sizeof__()
        self.__max_size = max_size
        self.__size_mod = self._DATA_SIZE_CLASSES[size_mod]

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