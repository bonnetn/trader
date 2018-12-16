from datetime import timedelta


class Context:
    """
    Context is an object containing the relevant variables that need to be passed across states.
    """

    def __init__(self):
        self.driver = True
        self.sleep_for = timedelta()
