from flask import redirect, request


class Root_URL():
    endpoints = ["/"]
    endpoint_name = "page_root_html"
    endpoint_methods = ["GET", "POST"]

    def __init__(self, fhdhr):
        self.fhdhr = fhdhr

    def __call__(self, *args):
        return self.get(*args)

    def get(self, *args):

        user_agent = request.headers.get('User-Agent')

        # Client Devices Discovering Device Information
        if not user_agent or str(user_agent).lower().startswith("plexmediaserver"):

            # Plex Remote Media Grabber redirect
            if self.fhdhr.config.dict["rmg"]["enabled"] and str(user_agent).lower().startswith("plexmediaserver"):
                redirect_url = "/rmg_ident.xml"
                return redirect(redirect_url)

            # Client Device is looking for HDHR type device
            else:
                redirect_url = "/device.xml"
                return redirect(redirect_url)

        # Anything Else is likely a Web Browser
        else:

            redirect_url = "/index"
            return redirect(redirect_url)
