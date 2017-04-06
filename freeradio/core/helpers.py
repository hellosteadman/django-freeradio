import time


def unique_id():
    return hex(int(time.time() * 10000000))[2:]
