from asyncore import write
import os
import logging
from logging import Formatter, StreamHandler
from logging.handlers import RotatingFileHandler
import traceback
import subprocess
import getpass

LOG_LEVEL_MAP = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}


def init_logger(
    name = 'default_logger',
    log_path = '/var/log/slg/default_location.log',
    log_level = 'INFO',
    stream_log_level = 'DEBUG',
    formatter_str = '%(asctime)s | %(levelname)-8s | Line %(lineno)-4s | %(pathname)s | %(message)s',
    max_bytes=10000000,
    backup_count=5
) -> logging.Logger:
    '''
    It's recommended to set name = __name__ as the name parameter when calling this function in order to get the logger name to be the same as the file's name.

    It's also advised to set the log_path to "/var/log/slg/{__file__.split("/")[-1]}.log" when calling from a script so you don't log to a default file but also one relevant to the script.
    '''
    log_level = LOG_LEVEL_MAP[log_level]
    stream_log_level = LOG_LEVEL_MAP[stream_log_level]

    def find_existing_dir(directory_path):
        '''Finds the lowest directory that actually exists, to check if we have write access to said dir'''
        if os.path.isdir(directory_path):
            return directory_path
        while directory_path:
            directory_path = '/'.join(directory_path.split('/')[:-1])
            if os.path.isdir(directory_path):
                return directory_path
        return '/'

    write_directory = os.path.dirname(log_path)

    if not os.path.isdir(write_directory):
        lowest_real_directory = find_existing_dir(write_directory)
        # checks if we have write access to this lowest directory
        if os.access(lowest_real_directory, os.W_OK):
            subprocess.run(f'mkdir -p {write_directory}', shell=True)
        else:
            username = input('The write directory does not exist and is write-protected, please enter the username this directory should belong to: ')
            password = getpass.getpass('Now please enter the sudo password so we can create the directory in write protected directory: ')
            subprocess.run(f'echo {password} | sudo -S mkdir -p {write_directory} 2>&1 /dev/null && echo {password} | sudo -S chown -R {username}:{username} {write_directory} 2>&1 /dev/null', shell=True)

    try:
        logger = logging.getLogger(name)
        file_handler = RotatingFileHandler(log_path, maxBytes=max_bytes, backupCount=backup_count)
        stream_handler = StreamHandler()

        file_formatter = Formatter(formatter_str, datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(file_formatter)

        # we also log to the stream where the logs are saved
        stream_formatter = Formatter(f'------- Log message saved to {log_path} ------- \n' + formatter_str, datefmt='%Y-%m-%d %H:%M:%S')
        stream_handler.setFormatter(stream_formatter)

        stream_handler.setLevel(stream_log_level)
        logger.addHandler(stream_handler)

        logger.setLevel(log_level)
        file_handler.setLevel(log_level)
        logger.addHandler(file_handler)

        return logger

    except FileNotFoundError:
        print(f'\nLogging directory not found. Please create {os.path.dirname(log_path)} directory and change the user to the user running this script')
        print('\nUse the following commands to create the directory and set the user to the user running this script:')
        print(f'\nsudo mkdir -p {os.path.dirname(log_path)}')
        print(f'sudo chown -R $USER:$USER {os.path.dirname(log_path)}')
        exit(0)
    except:
        print('Unhandled error occured, as described below:\n\n')
        print(traceback.format_exc())

def generate_cron_log_absolute_filepath(file_, location="global"):
    # Pass in __file__ as the argument every time

    abs_path = os.path.abspath(file_)

    if location == "global":
        log_path = "/var/log/slg/cron/"
    elif location == "local":
        log_path = abs_path.split('cron')[0] + 'cron/logs/'

    filename = abs_path.split('cron')[1][1:].replace('/', '.') + '.log'
    return log_path + filename