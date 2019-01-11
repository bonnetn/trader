def get_nth_parent(element, n):
    e = element
    for i in range(n):
        e = e.find_element_by_xpath("..")

    return e
