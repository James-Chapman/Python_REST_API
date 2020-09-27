import http.server
import logging
import signal
import sys

from RESTfulHTTPRequestHandler import RESTfulHTTPRequestHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console and file handlers and set log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s %(threadName)s %(filename)s %(lineno)d [%(levelname)s] : %(funcName)s : %(message)s')

# set formatter for console and file handlers
ch.setFormatter(formatter)

# add console and file handlers to logger
logger.addHandler(ch)

logging.getLogger("DefaultHTTPRequestHandler").addHandler(ch)
logging.getLogger("RESTfulHTTPRequestHandler").addHandler(ch)
logging.getLogger("JobManager").addHandler(ch)

def interupt_handler(signum, frame):
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, interupt_handler)

    SERVER_IP = "0.0.0.0"
    SERVER_PORT = 8080

    server = http.server.ThreadingHTTPServer((SERVER_IP, SERVER_PORT), RESTfulHTTPRequestHandler)
    print("Starting server, use <Ctrl-C> to stop")
    server.serve_forever()


if __name__ == '__main__':
    main()