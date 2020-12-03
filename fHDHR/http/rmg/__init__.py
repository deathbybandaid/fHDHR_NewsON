
from .rmg_ident_xml import RMG_Ident_XML


class fHDHR_RMG():

    def __init__(self, fhdhr):
        self.fhdhr = fhdhr

        self.rmg_ident_xml = RMG_Ident_XML(fhdhr)
