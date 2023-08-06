import re

s = 1
m = s * 60
h = m * 60
d = h * 24
w = d * 7
mon = w * 4
y = d * 365


def ms(query: str):
    """
    Query to ms convert
    """


    temp = re.findall(pattern = r'^(-?(?:\d+)?.?\d+) *(milliseconds?|msecs?|ms|seconds?|secs?|s|minutes?|mins?|m|hours?|hrs?|h|days?|d|weeks?|w|years?|yrs?|y)?$', string = query, flags = re.I)
    if temp == []:
    	return None

    number = int(temp[0][0])

    mat = temp[0][1]
    if mat == 'm' or mat == 'min' or mat == 'minute':
        return m * number
    elif mat == 'h' or mat == 'ho' or mat == 'hour':
        return h * number
    elif mat == 'd' or mat == 'day':
        return d * number
    elif mat == 'w' or mat == 'week':
        return w * number
    elif mat == 'y' or mat == 'year':
        return y * number
    elif mat == 'mon' or mat == 'month':
        return mon * number
    else:
        return None