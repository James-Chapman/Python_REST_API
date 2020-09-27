import json
import logging
import re
import sys
import http.client
from urllib.parse import urlparse
from DefaultHTTPRequestHandler import DefaultHTTPRequestHandler
from JobManager import JobManager, JobStatus, jobStatusAsString

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class RESTfulHTTPRequestHandler(DefaultHTTPRequestHandler):
    """Default HTTP Request Handler Interface class."""
    jobManager = JobManager()

    def _handle_OPTIONS(self):
        """Handle OPTIONS function."""
        try:
            self.send_response(200, "OK")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.end_headers()
            logger.debug("Sent response: \"200\"")
        except Exception as ex:
            logger.error(str(ex))
            raise ex


    def _handle_GET(self):
        """Handle GET function. Override this method."""
        try:
            parsed_path = urlparse(self.path)
            if (parsed_path.path == "/api/jobs"):
                if (parsed_path.query == "status=running"):
                    self._handle_get_jobs_running()
                elif (parsed_path.query == "status=stopped"):
                    self._handle_get_jobs_stopped()
                elif (parsed_path.query == "status=completed"):
                    self._handle_get_jobs_completed()
                else:
                    self._handle_get_jobs_all()

            m = re.match(r"/api/jobs/(\d+)", parsed_path.path)
            if (m):
                self._handle_get_job(int(m[1]))
            else:
                self.send_response(404)
                self.end_headers()
                logger.debug("Sent response: \"404\"")
        except Exception as ex:
            logger.error(ex)
            raise ex
            #self.send_response(501, "Not implemented")


    def _handle_POST(self):
        """Handle POST function."""
        try:
            parsed_path = urlparse(self.path)
            if (parsed_path.path == "/api/jobs"):
                self._handle_post_job_start()
            else:
                self.send_response(404)
                self.end_headers()
        except Exception as ex:
            logger.error(str(ex))
            raise ex


    def _handle_DELETE(self):
        """Handle POST function."""
        try:
            self.send_response(404)
            self.end_headers()
        except Exception as ex:
            logger.error(str(ex))
            raise ex


    def _handle_PUT(self):
        """Handle POST function."""
        try:
            parsed_path = urlparse(self.path)
            m = re.match(r"/api/jobs/(\d+)/stop", parsed_path.path)
            if (m):
                self._handle_put_job_stop(int(m[1]))
            else:
                self.send_response(404)
                self.end_headers()
        except Exception as ex:
            logger.error(str(ex))
            raise ex


    def _handle_post_job_start(self):
        try:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            self.send_response(200)
            self.end_headers()
            jobData = json.loads(body)
            # process json and gets args
            cmd = jobData["command"]
            jobMap = dict()
            if cmd != "":
                id = self.jobManager.create_job(cmd)
                jobMap = {
                    "id": id,
                    "status": "running"
                }
            else:
                jobMap = {
                    "id": -1,
                    "status": "stopped"
                }
            jsonString = json.dumps(jobMap)
            self.wfile.write(bytes(jsonString, "utf8"))
        except Exception as ex:
            logger.error(str(ex))
            raise ex


    def _handle_put_job_stop(self, id):
        if self.jobManager.kill_job(id):
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(500)


    def _send_json_response(self, code, map):
        jsonString = json.dumps(map)
        self.send_response(code)
        self.send_header('Content-type', 'application/json;charset=utf-8')
        self.send_header('Content-length', len(jsonString))
        self.end_headers()
        self.wfile.write(bytes(jsonString, "utf8"))


    def _handle_get_job(self, id):
        job = self.jobManager.get_job(id)
        jobMap = dict()
        code = 404
        if job:
            jobstatus = jobStatusAsString(job.status)
            jobout = job.stdout.decode("utf-8")
            jobMap = {"id": job.id, "status": jobstatus, "command": job.command, "stdout": jobout}
            code = 200
        else:
            jobMap = {"id": -1}
        self._send_json_response(code, jobMap)


    def _handle_get_jobs_all(self):
        joblist = self.jobManager.get_jobs()
        jobMap = {
            "jobs": joblist
        }
        self._send_json_response(200, jobMap)


    def _handle_get_jobs_running(self):
        joblist = self.jobManager.get_jobs_running()
        jobMap = {
            "jobs": joblist
        }
        self._send_json_response(200, jobMap)


    def _handle_get_jobs_stopped(self):
        joblist = self.jobManager.get_jobs_stopped()
        jobMap = {
            "jobs": joblist
        }
        self._send_json_response(200, jobMap)


    def _handle_get_jobs_completed(self):
        joblist = self.jobManager.get_jobs_completed()
        jobMap = {
            "jobs": joblist
        }
        self._send_json_response(200, jobMap)

