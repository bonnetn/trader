# coding=utf-8
"""
Misc. utility functions.
"""


def get_nth_parent(element, n):
    """
    Get the nth parent.

    For instance if n=3, will return element.parent.parent.parent.
    :param element: web element
    :param n: positive integer
    :return: web element
    """
    e = element
    for i in range(n):
        e = e.find_element_by_xpath("..")

    return e
