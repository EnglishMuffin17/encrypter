class Config:

    """Console configuration"""

    #Show 'Running...' statements from dependancies
    show_run_test = False

    #Show Console messages concerning threads
    show_thread_test = False

    #Show Console messages concerning logging
    show_log_test = False

    #Show getCharacterCheck on instantiation of 
    # CharGenerator
    show_character_check = False

    #Show miscellaneous Console messages for debugging
    show_console = False

    show_config_settings = False

    """Logging configuration"""

    #Use the default logging config for encrypt_logger.Logger
    use_config_logger = False

    #Enable setting up and logging of encrypt_logger.Logger
    config_log_enabled = False

    #Set the log level of encrypt_logger.Logger
    config_log_level = "debug"

    #Set path folder for Logger
    config_log_path = "encrypter/logs/"

    #Set file name for Logger
    config_log_title = "default_encrypt_log"

    #Set message format for Logger
    config_log_format = "%(message)s"

    @classmethod
    def showConfig(cls):
        ignore = {"__module__","__doc__","showConfig",
        "configurations","__dict__","__weakref__"}

        for i in Config.__dict__:
            if ignore.__contains__(i):
                continue
            else:
                print(f"[{i}] --> {Config.__dict__[i]}")

    @classmethod
    def configurations(cls,preset):
        """
        Initializes a config preset from a defined list
        """
    
        def disable():
            cls.show_run_test = False
            cls.show_log_test = False
            cls.show_thread_test = False
            cls.show_console = False
            cls.show_character_check = False
            
            cls.use_config_logger = False
            cls.config_log_enabled = False

        def debug():
            cls.show_run_test = True
            cls.show_log_test = True
            cls.show_thread_test = True
            cls.show_console = True
            cls.show_character_check = True
            cls.show_config_settings = True
            
            cls.use_config_logger = True
            cls.config_log_enabled = True
            cls.config_log_level = "debug"

        def log():
            cls.use_config_logger = True
            cls.config_log_enabled = True

        def console():
            cls.show_run_test = True
            cls.show_log_test = True
            cls.show_thread_test = True
            cls.show_console = True
            cls.show_character_check = True

        def custom():
            pass

        presets = {
            "custom":custom,
            "debug":debug,
            "log":log,
            "console":console
        }

        if preset != "disable":
            disable()
            return presets[preset]()
        else:
            return disable()

Config.configurations("disable")

if __name__ == "__main__":
    pass
elif Config.show_run_test:
    print(f"{__name__} Running...")

    if Config.show_config_settings:
        print(f"{__name__} show_config_settings set to {Config.show_config_settings}")
        Config.showConfig()