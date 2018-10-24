import threading

# Lock access to Selenium while using a screen.
lock = threading.Lock()

"""
This define a generic screen that you can find in the game. You usually access a screen by clicking on the right menu.
"""


class Screen:
    """
    Tab represents a screen, with its information and interactions.
    """

    def extract_info(self):
        """
        Fetch the information that you can find on this screen.
        :return: a dictionnary containing revelant pieces of info
        """
        raise NotImplementedError()

    def move(self):
        """
        This function is called when you have to go to this screen.
        Override this function.
        """
        raise NotImplementedError()

    def __enter__(self):
        lock.acquire()
        self.move()
        return self

    def __exit__(self, type, value, traceback):
        lock.release()
