import webob
import webob.exc

import StringIO


from . import xml
from . import basedec

class xslt(basedec.BaseDecorator):
    def __init__(self, func):
        self.func = func

    def __call__(self, request, *args):
        response = self.func(request, *args)
        if 'xsl' in request.GET:
            self.link_stylesheet(request, response)
            response.content_type = 'application/xml; charset=UTF-8'
        elif 'xslt' in request.GET:
            self.apply_stylesheet(request, response)
            response.content_type = 'text/html; charset=UTF-8'
        else:
            self.serialize_xml(response)
            response.content_type = 'application/xml; charset=UTF-8'
        return response

    def link_stylesheet(self, request, response):
        response.body = xml.serialize_ws(
            [xml.FRAGMENT,
                [xml.PROCINC, 'xml', ('version', '1.0'), ('encoding', 'UTF-8')],
                [xml.PROCINC, 'xml-stylesheet', ('type', 'text/xsl'), ('href', request.GET['xsl'])],
                response.body]).encode('utf8')

    def apply_stylesheet(self, request, response):
        import lxml.etree
        filename = request.environ['DOCUMENT_ROOT'] + '/web/' + request.GET['xslt']
        print 'xslt: serializing XML'
        self.serialize_xml(response)
        print 'xslt: reading XSL', filename
        xsl_xml = lxml.etree.parse(filename)
        print 'xslt: compiling XSL'
        xsl = lxml.etree.XSLT(xsl_xml)
        print 'xslt: reading XML'
        xml = lxml.etree.parse(StringIO.StringIO(response.body))
        print 'xslt: applying XSLT'
        response.body = str(xsl(xml))
        print 'xslt: done'

    def serialize_xml(self, response):
        response.body = xml.serialize_ws(response.body).encode('utf8')
