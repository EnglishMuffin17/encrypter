try:
    try:
        from pkg_utils.encrypt_config import Config
    except ModuleNotFoundError:
        from KnitCrypter.pkg_utils.encrypt_config import Config
except ModuleNotFoundError:
    from encrypt_config import Config
finally:
    #Builtins
    import threading
    import queue

"""
Using threading, wrap functions in new threads to run concurrently.
"""
class Threader:

    @staticmethod
    def addthread(func):
        """
        Decorator.\n
        When applied to a function, on function call, @addthread creates a new thread
        executing the function.
        """
        def wrapped_func(que,*args,**kwargs):
            next_func = func(*args,**kwargs)
            que.put(next_func)

        def wrapper(*args,**kwargs):
            que = queue.Queue()

            next_thread = threading.Thread(target=wrapped_func,args=(que,)+args,kwargs=kwargs)
            
            if Config.show_thread_test:
                print(f"Running <{func.__name__}> in --> [{next_thread.getName()}]")

            next_thread.start()
            next_thread.result_queue = que

            return next_thread.result_queue.get()
        return wrapper

if __name__ == "__main__":
    print("Running Threader.py as <__main__>")

elif Config.show_run_test:
    print(f"{__name__} Running...")