import datetime

def time_in_range(start, end, x):
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

start = datetime.time(23, 0, 0)
end = datetime.time(4, 0, 0)

print(time_in_range(start, end, datetime.datetime.now().time()))