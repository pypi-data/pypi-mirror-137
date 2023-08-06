# @Time    : 2021/11/18 20:06
# @Author  : tk
# @FileName: test_prctl.py

import sys_prctl
import time
import os
'''
    sys_prctl: Linux syscall prctl setting the process name and the thread name
    
    sys_prctl had test pass at linux python3.6,python3.7,python3.8,python3.9
    
    support only for linux
'''


def test_prctl():
    # 参见linux prctl
    # sys_prctl.prctl
    pass
#set current process id
def test_process():
    #get process name
    name = sys_prctl.getprocname()
    print(name)

    # set process name
    name = "my_process"
    sys_prctl.setprocname(name)

    #get process name
    name = sys_prctl.getprocname()
    print(name)

    print(os.getpid())
    time.sleep(10 * 60)
    #ps -ef | grep my_process

def test_process_with_tid():
    #pthread_id is not thread id , it is c pthread id
    pthread_id = -1
    print('pthread_id:',pthread_id)
    # get process name
    name = sys_prctl.getprocname(pthread_id=pthread_id)
    print(name)

    # set process name
    name = "my_process"
    # tid thread id
    sys_prctl.setprocname(name, pthread_id=pthread_id)

    # get process name
    name = sys_prctl.getprocname(pthread_id=pthread_id)
    print(name)

    print(os.getpid())
    time.sleep(10 * 60)



    #ps -ef | grep my_process

if __name__ == '__main__':
    test_process()