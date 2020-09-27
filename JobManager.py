import logging
import subprocess
import threading
from enum import Enum

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class JobStatus(Enum):
    RUNNING = 1
    STOPPED = 2
    COMPLETED = 3

def jobStatusAsString(status):
    if status == JobStatus.RUNNING:
        return "running"
    elif status == JobStatus.COMPLETED:
        return "completed"
    elif status == JobStatus.STOPPED:
        return "stopped"


class Job(object):
    id = 0
    status = JobStatus.STOPPED
    command = ""
    stdout = bytearray()
    stderr = bytearray()
    proc = None


class JobManager(object):
    """JobManager is a class to manage jobs"""

    def __init__(self):
        self.jobs = dict()
        self.job_ids = []
        self.running_job_ids = []
        self.stopped_job_ids = []
        self.completed_job_ids = []
        self.arraylock = threading.Lock()

    def get_jobs(self):
        """Returns a list of jobs"""
        return self.job_ids

    def get_jobs_running(self):
        """Returns a list of jobs"""
        return self.running_job_ids

    def get_jobs_stopped(self):
        """Returns a list of jobs"""
        return self.stopped_job_ids

    def get_jobs_completed(self):
        """Returns a list of jobs"""
        return self.completed_job_ids

    def get_job(self, id):
        """Returns job object of supplied <id>"""
        if id in self.jobs:
            return self.jobs[id]
        else:
            return None

    def create_job(self, cmd):
        """Creates job, returns its id"""
        if (len(self.job_ids) == 0):
            try:
                self.arraylock.acquire()
                self.job_ids.append(0)
            finally:
                self.arraylock.release()
        else:
            try:
                self.arraylock.acquire()
                self.job_ids.append(self.job_ids[-1] + 1)
            finally:
                self.arraylock.release()
        job = Job()
        job.id = self.job_ids[-1]
        job.status = JobStatus.RUNNING
        job.command = cmd
        try:
            self.arraylock.acquire()
            self.jobs[job.id] = job
        finally:
            self.arraylock.release()
        thread1 = threading.Thread(target=self.start_job, args=(job.id,))
        thread1.start()
        return job.id


    def start_job(self, id):
        """Starts job <id>"""
        cmdargs = self.jobs[id].command.split(" ")
        try:
            self.jobs[id].proc = subprocess.Popen(cmdargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.arraylock.acquire()
            self.running_job_ids.append(id)
            self.arraylock.release()
            self.jobs[id].stdout, self.jobs[id].stderr = self.jobs[id].proc.communicate()
            # proc.communicate() should block until process exits.
            if self.jobs[id].proc.returncode == 0:
                self.jobs[id].status = JobStatus.COMPLETED
                if id not in self.completed_job_ids:
                    self.arraylock.acquire()
                    self.completed_job_ids.append(id)
                    self.arraylock.release()
            else:
                self.jobs[id].status = JobStatus.STOPPED
                if id not in self.stopped_job_ids:
                    self.arraylock.acquire()
                    self.stopped_job_ids.append(id)
                    self.arraylock.release()
            if id in self.running_job_ids:
                self.arraylock.acquire()
                self.running_job_ids.remove(id)
                self.arraylock.release()
        except FileNotFoundError as ex:
            self.jobs[id].status = JobStatus.STOPPED
            if id not in self.stopped_job_ids:
                self.arraylock.acquire()
                self.stopped_job_ids.append(id)
                self.arraylock.release()


    def kill_job(self, id):
        """Send terminate to job <id>"""
        if id in self.jobs:
            if self.jobs[id].proc != None:
                self.jobs[id].proc.kill()
                self.jobs[id].status = JobStatus.STOPPED
                if id in self.running_job_ids:
                    try:
                        self.arraylock.acquire()
                        self.running_job_ids.remove(id)
                        self.stopped_job_ids.append(id)
                    finally:
                        self.arraylock.release()
                return True
        return False


    def get_job_output(self, id):
        """Returns std out from job <id>"""
        return self.jobs[id].stdout


