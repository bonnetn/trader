from trader.interface.screen.base_screen import Screen, lock


class TestScreen(Screen):
    def extract_info(self) -> dict:
        pass

    def __init__(self, driver):
        super().__init__(driver)
        self.moved = False

    def move(self) -> None:
        self.moved = True


def test_base_screen_move():
    with TestScreen(None) as s:
        assert s.moved


def test_base_screen_lock():
    assert not lock.locked()
    with TestScreen(None):
        assert lock.locked()
