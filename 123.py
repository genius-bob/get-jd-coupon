import time

t = time.localtime(time.time())
format_time = '%Y-%m-%d %H:%M:%S'
print(time.strftime(format_time, t))