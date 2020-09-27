import http.server
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class DefaultHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """Default HTTP Request Handler Interface class."""

    def do_OPTIONS(self):
        """Default OPTIONS function for the Request Handler"""
        try:
            logger.debug("OPTIONS request from: {0} to {1}".format(self.client_address, self.path[1]))
            self._handle_OPTIONS()
        except Exception as ex:
            self.send_response(500, ex)
            print("Exception in DefaultHTTPRequestHandler.do_OPTIONS(): {0}".format(ex))


    def do_HEAD(self):
        """Default HEAD function for the Request Handler"""
        try:
            logger.debug("HEAD request from: {0} to {1}".format(self.client_address, self.path[1]))
            self._handle_HEAD()
        except Exception as ex:
            self.send_response(500, ex)
            print("Exception in DefaultHTTPRequestHandler.do_HEAD(): {0}".format(ex))


    def do_GET(self):
        """Default GET function for the Request Handler"""
        try:
            logger.debug("GET request from: {0} to {1}".format(self.client_address, self.path[1]))
            self._handle_GET()
        except Exception as ex:
            self.send_response(500, ex)
            print("Exception in DefaultHTTPRequestHandler.do_GET(): {0}".format(ex))


    def do_PUT(self):
        """Default PUT function for the Request Handler"""
        try:
            logger.debug("PUT request from: {0} to {1}".format(self.client_address, self.path[1]))
            self._handle_PUT()
        except Exception as ex:
            self.send_response(500, ex)
            print("Exception in DefaultHTTPRequestHandler.do_PUT(): {0}".format(ex))


    def do_POST(self):
        """Default POST function for the Request Handler"""
        try:
            logger.debug("POST request from: {0} to {1}".format(self.client_address, self.path[1]))
            self._handle_POST()
        except Exception as ex:
            self.send_response(500, ex)
            print("Exception in DefaultHTTPRequestHandler.do_POST(): {0}".format(ex))


    def do_DELETE(self):
        """Default DELETE function for the Request Handler"""
        try:
            logger.debug("DELETE request from: {0} to {1}".format(self.client_address, self.path[1]))
            self._handle_DELETE()
        except Exception as ex:
            self.send_response(500, ex)
            print("Exception in DefaultHTTPRequestHandler.do_POST(): {0}".format(ex))


    def _handle_OPTIONS(self):
        """Handle OPTIONS function. Override this method."""
        self.send_response(501, "Not implemented")


    def _handle_HEAD(self):
        """Handle HEAD function. Override this method."""
        self.send_response(501, "Not implemented")


    def _handle_GET(self):
        """Handle GET function. Override this method."""
        self.send_response(501, "Not implemented")


    def _handle_PUT(self):
        """Handle PUT function. Override this method."""
        self.send_response(501, "Not implemented")


    def _handle_POST(self):
        """Handle POST function. Override this method."""
        self.send_response(501, "Not implemented")


    def _handle_DELETE(self):
        """Handle DELETE function. Override this method."""
        self.send_response(501, "Not implemented")
