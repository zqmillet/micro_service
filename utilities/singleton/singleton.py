class Singleton:
    def __new__(self, *args, **kwargs):
        if not hasattr(self, '_instance'):
            self._instance = super().__new__(self)
        return self._instance
