
from .lineup_post import Lineup_Post
from .device_xml import HDHR_Device_XML


class fHDHR_HDHR():

    def __init__(self, fhdhr):
        self.fhdhr = fhdhr

        self.lineup_post = Lineup_Post(fhdhr)

        self.device_xml = HDHR_Device_XML(fhdhr)
