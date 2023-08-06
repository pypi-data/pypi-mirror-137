# -*- coding: utf-8 -*-
# @Time    : 2021/11/19 11:30
# @Author  : wyw

import threading
import os

# def thread_func(obj):
#     print(obj['tid'])
#
#
# obj = dict()
# obj['tid'] = -1
#
# mythd = threading.Thread(target=thread_func, args=(obj,))
# obj['tid'] = threading.get_native_id()

def load():
    print(threading.get_native_id())
    print(threading.get_ident())
    print(os.getpid())
load()
# mythd.start()
# mythd.join()
