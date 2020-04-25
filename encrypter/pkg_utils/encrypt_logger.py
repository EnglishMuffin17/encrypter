try:
    try:
        from pkg_utils.encrypt_config import Config
    except ModuleNotFoundError:
        from encrypter.pkg_utils.encrypt_config import Config
except ModuleNotFoundError:
    from encrypt_config import Config
finally:
    import logging,os,datetime

"""
Using logging, os and datetime, configure a logging module to use for debugging
"""

class Logger:
    log_enabled = False
    log_level = "info"

    log_path = ""
    log_title = ""
    log_format = ""

    log_time = datetime.datetime.today()
    log_time = log_time.strftime("%H:%M")

    log = logging.getLogger(__name__)
    
    @classmethod
    def start(cls):
        log_levels = {
            "debug":logging.DEBUG,
            "info":logging.INFO,
            "warn":logging.WARN,
            "error":logging.ERROR,
            "critical":logging.CRITICAL
        }
        
        if Config.show_log_test:
            print(f"{__name__} log_enabled set to {cls.log_enabled}")
        if cls.log_enabled:
            if Config.show_log_test:
                print("Staring log...")
                print(f"Logging events in {cls.log_title}")

            cls.log.setLevel(log_levels[cls.log_level])
            cls.log_formatter = logging.Formatter(cls.log_format)
            cls.log_handler = logging.FileHandler(cls.log_path+cls.log_title+".log")
            cls.log_handler.setFormatter(cls.log_formatter)
            cls.log.addHandler(cls.log_handler)

            cls.log.info(f"[{__name__}] {cls.log_title} initiated at [{cls.log_time}]")

    @classmethod
    def configureLogger(cls,path,title,format_,log_enabled=False,log_level="info"):
        cls.log_enabled = log_enabled
        cls.log_level = log_level

        cls.log_path = path
        cls.log_title = title
        cls.log_format = format_

        fill = 0
        new_title = cls.log_title
        while os.path.exists(cls.log_path+new_title+".log"):
            new_title = cls.log_title +"_"+ str(fill)
            fill += 1

        cls.log_title = new_title

        if Config.show_log_test:
            print(f"{__name__} Configured. Ready to log if enabled")

    @classmethod
    def submitEvent(cls,func,log_level="info"):
        """
        Decorator.\n
        When applied to a function, on a function call, @submitEvent submits a request
        to log events to the appropriate  log file
        """
        log_levels = {
            "debug":cls.log.debug,
            "info":cls.log.info,
            "warn":cls.log.warning,
            "error":cls.log.error,
            "critical":cls.log.critical
        }

        
        class_name = func.__qualname__
        name = f"{class_name}"
        
        def wrapper_enabled(*args,**kwargs):
            log_levels[log_level](f"[{log_level}] <{name}> called at [{cls.log_time}]")
            log_levels["debug"](f"[debug] <{name}> given ({args}) and ({kwargs}) as arguments at [{cls.log_time}]")
            return func(*args,**kwargs)

        def wrapper_disabled(*args,**kwargs):
            return func(*args,**kwargs)

        if cls.log_enabled:    
            return wrapper_enabled
        else:
            return wrapper_disabled


if __name__ == "__main__":
    print("Running from encrypt_log.py as <__main__>")
    
    log_path = "encrypter/logs/"
    log_title = "log_test"
    log_format = "%(message)s"
    Logger.configureLogger(log_path,log_title,log_format,log_level="info")
    Logger.start()

elif Config.show_run_test:
    print(f"{__name__} Running...")