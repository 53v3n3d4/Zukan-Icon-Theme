import time


def st_time(func):
    """
    st decorator to calculate the total time of a func

    From https://stackoverflow.com/questions/1593019/is-there-any-simple-way-to-benchmark-python-script
    """

    def st_func(*args, **keyArgs):
        t1 = time.time()
        r = func(*args, **keyArgs)
        t2 = time.time()
        print('Function %s, Time %s' % (func.__name__, t2 - t1))
        return r

    return st_func
