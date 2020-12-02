
from .root_url import Root_URL

from .cluster import Cluster
from .settings import Settings
from .channels import Channels
from .lineup_post import Lineup_Post
from .xmltv import xmlTV
from .m3u import M3U
from .epg import EPG
from .watch import Watch
from .debug import Debug_JSON

from .images import Images


class fHDHR_API():

    def __init__(self, fhdhr):
        self.fhdhr = fhdhr

        self.root_url = Root_URL(fhdhr)

        self.cluster = Cluster(fhdhr)
        self.settings = Settings(fhdhr)
        self.channels = Channels(fhdhr)
        self.xmltv = xmlTV(fhdhr)
        self.m3u = M3U(fhdhr)
        self.epg = EPG(fhdhr)
        self.watch = Watch(fhdhr)
        self.debug = Debug_JSON(fhdhr)
        self.lineup_post = Lineup_Post(fhdhr)

        self.images = Images(fhdhr)
