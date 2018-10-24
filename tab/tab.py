class Tab:

    def extract_info(self):
        raise NotImplementedError()

    def move(self):
        raise NotImplementedError()

    def __enter__(self):
        self.move()
        return self

    def __exit__(self, type, value, traceback):
        pass
