"""
Test the screen interface.
"""
from trader.interface.screen.base_screen import Screen, lock


class TestScreen(Screen):
    """
    Stub screen.
    """

    # noinspection PyMissingOrEmptyDocstring
    def extract_info(self) -> dict:
        pass

    def __init__(self, driver):
        super().__init__(driver)
        self.moved = False

    # noinspection PyMissingOrEmptyDocstring
    def move(self) -> None:
        self.moved = True


# noinspection PyMissingOrEmptyDocstring
def test_base_screen_move():
    with TestScreen(None) as s:
        assert s.moved


# noinspection PyMissingOrEmptyDocstring
def test_base_screen_lock():
    assert not lock.locked()
    with TestScreen(None):
        assert lock.locked()
