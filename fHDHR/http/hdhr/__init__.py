
from .device_xml import HDHR_Device_XML


class fHDHR_HDHR():

    def __init__(self, fhdhr):
        self.fhdhr = fhdhr

        self.device_xml = HDHR_Device_XML(fhdhr)
