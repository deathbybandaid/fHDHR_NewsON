from flask import Response, request, redirect, abort, stream_with_context
import urllib.parse
import uuid

from fHDHR.exceptions import TunerError


class Watch():
    """Methods to create xmltv.xml"""
    endpoints = ["/api/watch"]
    endpoint_name = "api_watch"
    endpoint_methods = ["GET", "POST"]

    def __init__(self, fhdhr):
        self.fhdhr = fhdhr

    def __call__(self, *args):
        return self.get(*args)

    def get(self, *args):

        client_address = request.remote_addr

        accessed_url = request.args.get('accessed', default=request.url, type=str)

        method = request.args.get('method', default=self.fhdhr.config.dict["fhdhr"]["stream_type"], type=str)

        tuner_number = request.args.get('tuner', None, type=str)

        redirect_url = request.args.get('redirect', default=None, type=str)

        if method in ["direct", "ffmpeg", "vlc"]:

            channel_number = request.args.get('channel', None, type=str)
            if not channel_number:
                return "Missing Channel"

            if str(channel_number) not in [str(x) for x in self.fhdhr.device.channels.get_channel_list("number")]:
                response = Response("Not Found", status=404)
                response.headers["X-fHDHR-Error"] = "801 - Unknown Channel"
                self.fhdhr.logger.error(response.headers["X-fHDHR-Error"])
                abort(response)

            channel_dict = self.fhdhr.device.channels.get_channel_dict("number", channel_number)
            if not channel_dict["enabled"]:
                response = Response("Service Unavailable", status=503)
                response.headers["X-fHDHR-Error"] = str("806 - Tune Failed")
                self.fhdhr.logger.error(response.headers["X-fHDHR-Error"])
                abort(response)

            duration = request.args.get('duration', default=0, type=int)

            transcode = request.args.get('transcode', default=None, type=str)
            valid_transcode_types = [None, "heavy", "mobile", "internet720", "internet480", "internet360", "internet240"]
            if transcode not in valid_transcode_types:
                response = Response("Service Unavailable", status=503)
                response.headers["X-fHDHR-Error"] = "802 - Unknown Transcode Profile"
                self.fhdhr.logger.error(response.headers["X-fHDHR-Error"])
                abort(response)

            stream_args = {
                            "channel": channel_number,
                            "method": method,
                            "duration": duration,
                            "transcode": transcode,
                            "accessed": accessed_url,
                            "client": client_address,
                            "client_id": str(client_address) + "_" + str(uuid.uuid4())
                            }

            try:
                if not tuner_number:
                    tunernum = self.fhdhr.device.tuners.first_available()
                else:
                    tunernum = self.fhdhr.device.tuners.tuner_grab(tuner_number)
            except TunerError as e:
                self.fhdhr.logger.info("A %s stream request for channel %s was rejected due to %s"
                                       % (stream_args["method"], str(stream_args["channel"]), str(e)))
                response = Response("Service Unavailable", status=503)
                response.headers["X-fHDHR-Error"] = str(e)
                self.fhdhr.logger.error(response.headers["X-fHDHR-Error"])
                abort(response)
            tuner = self.fhdhr.device.tuners.tuners[int(tunernum)]

            try:
                stream_args = self.fhdhr.device.tuners.get_stream_info(stream_args)
            except TunerError as e:
                self.fhdhr.logger.info("A %s stream request for channel %s was rejected due to %s"
                                       % (stream_args["method"], str(stream_args["channel"]), str(e)))
                response = Response("Service Unavailable", status=503)
                response.headers["X-fHDHR-Error"] = str(e)
                self.fhdhr.logger.error(response.headers["X-fHDHR-Error"])
                tuner.close()
                abort(response)

            self.fhdhr.logger.info("Tuner #" + str(tunernum) + " to be used for stream.")
            tuner.set_status(stream_args)

            if stream_args["method"] == "direct":
                return Response(tuner.get_stream(stream_args, tuner), content_type=stream_args["content_type"], direct_passthrough=True)
            elif stream_args["method"] in ["ffmpeg", "vlc"]:
                return Response(stream_with_context(tuner.get_stream(stream_args, tuner)), mimetype=stream_args["content_type"])

        elif method == "close":

            if not tuner_number or int(tuner_number) not in list(self.fhdhr.device.tuners.tuners.keys()):
                return "%s Invalid tuner" % str(tuner_number)

            tuner = self.fhdhr.device.tuners.tuners[int(tuner_number)]
            tuner.close()

        else:
            return "%s Invalid Method" % method

        if redirect_url:
            return redirect(redirect_url + "?retmessage=" + urllib.parse.quote("%s Success" % method))
        else:
            return "%s Success" % method
