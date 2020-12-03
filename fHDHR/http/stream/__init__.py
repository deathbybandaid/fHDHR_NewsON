
from .auto import Auto
from .tuner import Tuner


class fHDHR_Stream():

    def __init__(self, fhdhr):
        self.fhdhr = fhdhr

        self.auto = Auto(fhdhr)
        self.tuner = Tuner(fhdhr)
