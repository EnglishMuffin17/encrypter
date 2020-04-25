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


if __name__ == "__main__":
    pass
elif Config.show_run_test:
    print(f"{__name__} Running...")