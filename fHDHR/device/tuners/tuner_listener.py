import socket
import multiprocessing
import threading

from .stream import Stream


class Internal_Tuner_Socket():

    def __init__(self, fhdhr, stream_args, tuner):
        self.fhdhr = fhdhr

        self.stream = Stream(self.fhdhr, stream_args, tuner)

        self.host = '127.0.0.1'
        self.port = 0

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))

        self.port = self.sock.getsockname()[1]

    def socket_start(self):
        if self.fhdhr.config.dict["main"]["thread_method"] in ["multiprocessing"]:
            streamsocket = multiprocessing.Process(target=self.socket_run)
        elif self.fhdhr.config.dict["main"]["thread_method"] in ["threading"]:
            streamsocket = threading.Thread(target=self.socket_run)
        if self.fhdhr.config.dict["main"]["thread_method"] in ["multiprocessing", "threading"]:
            streamsocket.start()

    def socket_run(self):

        while self.tuner.tuner_lock.locked():
            connection, client_address = self.sock.accept()
            self.sock.sendto(self.stream.get(), client_address)
