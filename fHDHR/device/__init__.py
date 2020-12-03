from .channels import Channels
from .epg import EPG
from .tuners import Tuners
from .images import imageHandler
from .ssdp import SSDPServer
from .cluster import fHDHR_Cluster


class fHDHR_Device():

    def __init__(self, fhdhr, origin):

        self.channels = Channels(fhdhr, origin)

        self.epg = EPG(fhdhr, self.channels, origin)

        self.tuners = Tuners(fhdhr, self.epg, self.channels)

        self.images = imageHandler(fhdhr, self.epg)

        self.ssdp = SSDPServer(fhdhr)

        self.cluster = fHDHR_Cluster(fhdhr, self.ssdp)
