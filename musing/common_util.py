#!usr/bin/env python
# coding=utf8
'''
Common Util
'''

import os
import hashlib
import time


def make_hash():
    '''
    randomly generate a hash string
    '''
    m_generator = hashlib.md5()
    m_generator.update(bytes(os.urandom(32)))
    return m_generator.hexdigest()


def get_date_time():
    '''
    get today's date and time
    '''
    return time.strftime("%Y%m%d_%H%M%S", time.localtime())
