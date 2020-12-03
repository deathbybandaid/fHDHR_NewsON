
from .rmg_ident_xml import RMG_Ident_XML
from .device_xml import RMG_Device_XML


class fHDHR_RMG():

    def __init__(self, fhdhr):
        self.fhdhr = fhdhr

        self.rmg_ident_xml = RMG_Ident_XML(fhdhr)
        self.device_xml = RMG_Device_XML(fhdhr)
