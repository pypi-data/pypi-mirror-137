class StopParsingError(Exception):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
        def __str__(self):
            return super().__str__()

class BrokenAccountError(Exception):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
        def __str__(self):
            return super().__str__()
