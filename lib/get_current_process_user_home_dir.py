import os
import pwd


def get_current_process_user_home_dir():
    pid = os.getpid()
    
    # the /proc/PID is owned by process creator
    proc_stat_file = os.stat("/proc/%d" % pid)
    # get UID via stat call
    uid = proc_stat_file.st_uid
    # look up the username from uid
    username = pwd.getpwuid(uid)[0]
    return pwd.getpwuid(uid)[5]
