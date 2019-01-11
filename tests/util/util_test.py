from unittest.mock import Mock, MagicMock

from selenium.webdriver.remote.webelement import WebElement

from trader.util.util import get_nth_parent


def test_get_nth_parent():
    m = Mock(spec=WebElement)
    m.find_element_by_xpath = MagicMock(return_value=m)
    get_nth_parent(m, 3)
    assert 3 == m.find_element_by_xpath.call_count
