from flask import Response, request
from io import BytesIO
import xml.etree.ElementTree

from fHDHR.tools import sub_el


class Device_XML():
    endpoints = ["/device.xml"]
    endpoint_name = "file_device_xml"

    def __init__(self, fhdhr):
        self.fhdhr = fhdhr

    def __call__(self, *args):
        return self.get(*args)

    def get(self, *args):

        base_url = request.url_root[:-1]

        user_agent = request.headers.get('User-Agent')

        out = xml.etree.ElementTree.Element('root')
        out.set('xmlns', "urn:schemas-upnp-org:device-1-0")

        if not (self.fhdhr.config.dict["rmg"]["enabled"] and str(user_agent).lower().startswith("plexmediaserver")):
            sub_el(out, 'URLBase', base_url)

        specVersion_out = sub_el(out, 'specVersion')
        sub_el(specVersion_out, 'major', "1")
        sub_el(specVersion_out, 'minor', "0")

        device_out = sub_el(out, 'device')

        if self.fhdhr.config.dict["rmg"]["enabled"] and str(user_agent).lower().startswith("plexmediaserver"):
            sub_el(device_out, 'deviceType', "urn:plex-tv:device:Media:1")
        else:
            sub_el(device_out, 'deviceType', "urn:schemas-upnp-org:device:MediaServer:1")

        sub_el(device_out, 'friendlyName', self.fhdhr.config.dict["fhdhr"]["friendlyname"])
        sub_el(device_out, 'manufacturer', self.fhdhr.config.dict["fhdhr"]["reporting_manufacturer"])
        sub_el(device_out, 'manufacturerURL', "https://github.com/fHDHR/%s" % self.fhdhr.config.dict["main"]["reponame"])
        sub_el(device_out, 'modelName', self.fhdhr.config.dict["fhdhr"]["reporting_model"])
        sub_el(device_out, 'modelNumber', self.fhdhr.config.internal["versions"]["fHDHR"])

        if self.fhdhr.config.dict["rmg"]["enabled"] and str(user_agent).lower().startswith("plexmediaserver"):
            sub_el(device_out, 'modelDescription', self.fhdhr.config.dict["fhdhr"]["friendlyname"])
            sub_el(device_out, 'modelURL', "https://github.com/fHDHR/%s" % self.fhdhr.config.dict["main"]["reponame"])
        else:
            sub_el(device_out, 'serialNumber')

        if self.fhdhr.config.dict["rmg"]["enabled"] and str(user_agent).lower().startswith("plexmediaserver"):
            serviceList_out = sub_el(device_out, 'serviceList')
            service_out = sub_el(serviceList_out, 'service')
            sub_el(service_out, 'URLBase', base_url)
            sub_el(service_out, 'serviceType', "urn:plex-tv:service:MediaGrabber:1")
            sub_el(service_out, 'serviceId', "urn:plex-tv:serviceId:MediaGrabber")

        sub_el(device_out, 'UDN', "uuid:" + self.fhdhr.config.dict["main"]["uuid"])

        fakefile = BytesIO()
        fakefile.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        fakefile.write(xml.etree.ElementTree.tostring(out, encoding='UTF-8'))
        device_xml = fakefile.getvalue()

        return Response(status=200,
                        response=device_xml,
                        mimetype='application/xml')
