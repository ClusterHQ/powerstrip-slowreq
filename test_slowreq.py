# Copyright ClusterHQ Limited. See LICENSE file for details.

"""
Tests for the sample slowreq plugin.
"""

from treq.client import HTTPClient
from twisted.internet import reactor
from twisted.trial.unittest import TestCase
from twisted.web.client import Agent
import json
import treq
import slowreq

class TestSlowRequests(TestCase):
    def setUp(self):
        self.agent = Agent(reactor) # no connectionpool
        self.client = HTTPClient(self.agent)
        self.slowreqAPI = slowreq.getAdapter()
        self.slowreqServer = reactor.listenTCP(0, self.slowreqAPI)
        self.slowreqPort = self.slowreqServer.getHost().port

    def tearDown(self):
        return self.slowreqServer.stopListening()

    def test_passthrough_request(self):
        d = self.client.post('http://127.0.0.1:%d/slowreq-adapter' % (self.slowreqPort,),
                      json.dumps({
                          "PowerstripProtocolVersion": 1,
                          "Type": "pre-hook",
                          "ClientRequest": {
                              "Method": "POST",
                              "Request": "/fictional",
                              "Body": {"Number": 7}}
                          }),
                      headers={'Content-Type': ['application/json']})
        def verifyResponseCode(response):
            self.assertEqual(response.code, 200)
            return response
        d.addCallback(verifyResponseCode)
        d.addCallback(treq.json_content)
        def verify(body):
            self.assertEqual(body, {
                "PowerstripProtocolVersion": 1,
                "ModifiedClientRequest": {
                  "Method": "POST",
                  "Request": "/fictional",
                  "Body": {"Number": 7}}})
        d.addCallback(verify)
        return d
