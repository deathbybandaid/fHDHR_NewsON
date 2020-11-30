import threading
import datetime

from fHDHR.exceptions import TunerError
from fHDHR.tools import humanized_time

from .tuner_listener import Internal_Tuner_Socket


class Tuner():
    def __init__(self, fhdhr, inum, epg):
        self.fhdhr = fhdhr

        self.number = inum
        self.epg = epg

        self.internal_socket = None

        self.tuner_lock = threading.Lock()
        self.set_off_status()

    def add_downloaded_size(self, bytes_count):
        if "downloaded" in list(self.status.keys()):
            self.status["downloaded"] += bytes_count

    def grab(self):
        if self.tuner_lock.locked():
            self.fhdhr.logger.error("Tuner #" + str(self.number) + " is not available.")
            raise TunerError("804 - Tuner In Use")
        self.tuner_lock.acquire()
        self.status["status"] = "Acquired"
        self.fhdhr.logger.info("Tuner #" + str(self.number) + " Acquired.")

    def close(self):
        self.set_off_status()
        if self.tuner_lock.locked():
            self.tuner_lock.release()
        self.fhdhr.logger.info("Tuner #" + str(self.number) + " Released.")

    def get_status(self):
        current_status = self.status.copy()
        if current_status["status"] == "Active":
            current_status["Play Time"] = str(
                humanized_time(
                    int((datetime.datetime.utcnow() - current_status["time_start"]).total_seconds())))
            current_status["time_start"] = str(current_status["time_start"])
            current_status["epg"] = self.epg.whats_on_now(current_status["channel"])
        return current_status

    def set_off_status(self):
        self.status = {"status": "Inactive"}

    def get_stream(self, stream_args, tuner):
        if not self.internal_socket:
            self.internal_socket = Internal_Tuner_Socket(self.fhdhr, stream_args, tuner)
        # start socket + generator
        # listen to socket and yeild
        return self.internal_socket.stream.get()

    def set_status(self, stream_args):
        if self.status["status"] != "Active":
            self.status = {
                            "status": "Active",
                            "clients": [],
                            "clients_id": [],
                            "method": stream_args["method"],
                            "accessed": [stream_args["accessed"]],
                            "channel": stream_args["channel"],
                            "proxied_url": stream_args["channelUri"],
                            "time_start": datetime.datetime.utcnow(),
                            "downloaded": 0
                            }
        if stream_args["client"] not in self.status["clients"]:
            self.status["clients"].append(stream_args["client"])
        if stream_args["client_id"] not in self.status["clients_id"]:
            self.status["clients_id"].append(stream_args["client_id"])
