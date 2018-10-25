class Context:
    """
    Context is an object containing the relevant variables that need to be passed across states.
    """
    def __init__(self, driver):
        self.driver = driver
        assert driver
