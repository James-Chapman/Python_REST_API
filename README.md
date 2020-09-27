# Python_REST_API
REST API written in Python 3

### API
POST /api/jobs - Start a job, submit JSON '{"command": "ping -n 10 127.0.0.1"}'
GET  /api/jobs - Get a list of all jobs
GET  /api/jobs?status=running - Get a list of running jobs
GET  /api/jobs?status=stopped - Get a list of stopped jobs
GET  /api/jobs?status=completed - Get a list of completed jobs
GET  /api/jobs/<job_id> - Get details of a particular job
PUT  /api/jobs/<job_id>/stop - Stop a job
