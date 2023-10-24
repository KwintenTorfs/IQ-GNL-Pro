import datetime
import os
import shutil


def string_datestamp():
    timestamp = datetime.datetime.now()
    return timestamp.strftime("%Y%m%d_%H%M%S")


def add_to_db_log(message, level, dir_name, excel_file_name=''):
    log_file = os.path.join(dir_name, 'log_db.txt')
    log_text = '%s, %s, %s, %s' % (string_datestamp(), level, excel_file_name, message)
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.write(log_text + '\n')
    else:
        with open(log_file, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(log_text + '\n' + content)
    return


def rename_current_log(name, dir_name):
    # during pipeline, log deposited in log with temporary name 'current_log' is used.
    # At end code. remove rename current_log to a more appropriate
    # name and delete current_log
    if not os.path.exists('logs'):
        os.mkdir('logs')

    temporary_name = 'current_log.txt'
    if os.path.exists(temporary_name):
        filename = os.path.join(dir_name, ' Log_%s__%s.txt' % (name, string_datestamp()))
        shutil.copyfile(temporary_name, filename)
        os.remove(temporary_name)
    else:
        filename = os.path.join(dir_name, 'Ok_Log_%s__%s.txt' % (name, string_datestamp()))
        with open(filename, 'w') as f:
            f.write('smooth upload.')
        f.close()
    return


def add_to_active_log(log_string):
    if os.path.exists('current_log.txt'):
        f = open('current_log.txt', 'a')
    else:
        f = open('current_log.txt', 'w')
    f.write(log_string + '\n')
    f.close()
    return
