# Copyright ClusterHQ Limited. See LICENSE file for details.

from twisted.internet import reactor
from twisted.internet.task import deferLater
from twisted.web import server, resource
import json

class AdapterResource(resource.Resource):
    isLeaf = True
    def render_POST(self, request):
        """
        Handle a pre-hook.
        """
        requestJson = json.loads(request.content.read())
        if requestJson["Type"] == "pre-hook":
            return self._handlePreHook(request, requestJson)
        elif requestJson["Type"] == "post-hook":
            return self._handlePostHook(request, requestJson)
        else:
            raise Exception("unsupported hook type %s" %
                (requestJson["Type"],))

    def _handlePreHook(self, request, requestJson):
        # The desired response is the entire client request
        # payload, unmodified.
        def waited():
            request.write(json.dumps({
                "PowerstripProtocolVersion": 1,
                "ModifiedClientRequest":
                    requestJson["ClientRequest"]}))
            request.finish()
        deferLater(reactor, 1, waited)
        return server.NOT_DONE_YET

    def _handlePostHook(self, request, requestJson):
        # The desired response is the entire client request
        # payload, unmodified.
        def waited():
            request.write(json.dumps({
                "PowerstripProtocolVersion": 1,
                "ModifiedServerResponse":
                    requestJson["ServerResponse"]}))
            request.finish()
        deferLater(reactor, 1, waited)
        return server.NOT_DONE_YET


def getAdapter():
    root = resource.Resource()
    root.putChild("slowreq-adapter", AdapterResource())
    site = server.Site(root)
    return site

if __name__ == "__main__":
    reactor.listenTCP(80, getAdapter())
    reactor.run()
