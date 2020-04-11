import time


def log(*args, **kwargs):
    now_time_stamp = time.localtime(time.time())
    format_time = '%Y-%m-%d %H:%M:%S'
    now_time = time.strftime(format_time, now_time_stamp)
    print(now_time, *args, **kwargs)



