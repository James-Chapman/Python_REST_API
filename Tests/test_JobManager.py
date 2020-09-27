import time

from JobManager import *

def test_JobManager_get_jobs():
    jobManager = JobManager()
    id1 = jobManager.create_job("ping 127.0.0.1")
    id2 = jobManager.create_job("ping 127.0.0.1")
    id3 = jobManager.create_job("ping 127.0.0.1")
    id4 = jobManager.create_job("ping 127.0.0.1")
    idarr = jobManager.get_jobs()
    assert(len(idarr) == 4)
    # killed = jobManager.kill_job(id1)
    # assert(killed == True)
    # stdout = jobManager.get_job_output(id2)
    # running = jobManager.get_jobs_running()
    # while (len(running) > 0):
    #      for job_id in running:
    #          job = jobManager.get_job(job_id)
    #          assert(job.status == JobStatus.RUNNING)
    #          time.sleep(0.5)
    #  assert(len(jobManager.get_jobs_completed()) == 3)
    #  assert(len(jobManager.get_jobs_stopped()) == 1)


def test_JobManager_kill_jobs():
    jobManager = JobManager()
    id1 = jobManager.create_job("ping 127.0.0.1")
    id2 = jobManager.create_job("ping 127.0.0.1")
    id3 = jobManager.create_job("ping 127.0.0.1")
    id4 = jobManager.create_job("ping 127.0.0.1")
    time.sleep(2) # Give thread and proc a chance to start
    killed = jobManager.kill_job(id1)
    assert(killed == True)
    assert(len(jobManager.get_jobs_stopped()) == 1)


def test_JobManager_kill_get_jobs_running_completed_stopped():
    jobManager = JobManager()
    id1 = jobManager.create_job("ping 127.0.0.1")
    id2 = jobManager.create_job("ping 127.0.0.1")
    id3 = jobManager.create_job("ping 127.0.0.1")
    id4 = jobManager.create_job("ping 127.0.0.1")
    time.sleep(2) # Give thread and proc a chance to start
    killed = jobManager.kill_job(id1)
    assert(killed == True)
    assert(len(jobManager.get_jobs_stopped()) == 1)
    running = jobManager.get_jobs_running()
    while (len(running) > 0):
        for job_id in running:
            job = jobManager.get_job(job_id)
            assert (job.status == JobStatus.RUNNING)
        running = jobManager.get_jobs_running()
        time.sleep(0.5)
    assert (len(jobManager.get_jobs_completed()) == 3)
    assert (len(jobManager.get_jobs_stopped()) == 1)

