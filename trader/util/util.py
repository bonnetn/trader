from datetime import timedelta


def get_nth_parent(element, n):
    e = element
    for i in range(n):
        e = e.find_element_by_xpath("..")

    return e


def convert_single_to_timedelta(time_val):
    num = int(time_val[:-1])
    if time_val.endswith('s'):
        return timedelta(seconds=num)
    elif time_val.endswith('m'):
        return timedelta(minutes=num)
    elif time_val.endswith('h'):
        return timedelta(hours=num)
    elif time_val.endswith('j'):
        return timedelta(days=num)


def convert_to_timedelta(time_val):
    time_val = time_val.split(" ")
    time = timedelta()
    for t in time_val:
        time += convert_single_to_timedelta(t)
    return time
