import http.client
import json
import threading
import time
import pytest

from RESTfulHTTPRequestHandler import RESTfulHTTPRequestHandler


@pytest.fixture(scope="module", autouse=True)
def start_rest_service():
    print("Starting server")
    SERVER_IP = "0.0.0.0"
    SERVER_PORT = 8080
    SERVER = http.server.ThreadingHTTPServer((SERVER_IP, SERVER_PORT), RESTfulHTTPRequestHandler)
    thread1 = threading.Thread(target=SERVER.serve_forever, args=())
    thread1.daemon = True
    thread1.start()
    time.sleep(5) # Give server a chance to start
    yield SERVER


def test_POST_api_job_start():
    testData = {"command": "ping -n 5 127.0.0.1"}
    jsonString = json.dumps(testData)
    restConn = http.client.HTTPConnection("127.0.0.1", 8080)
    headers = {'Content-type': 'application/json;charset=utf-8', 'Content-length': len(jsonString)}
    # Create 101 jobs
    for i in range(101):
        restConn.connect()
        restConn.request('POST', '/api/jobs', jsonString, headers)
        resp = restConn.getresponse()
        restConn.close()
        assert(resp.status == 200)


def test_PUT_api_job_stop():
    time.sleep(1) # Sleep while server starts
    restConn = http.client.HTTPConnection("127.0.0.1", 8080)
    headers = {'Content-type': 'application/json;charset=utf-8'}
    restConn.connect()
    restConn.request("PUT", "/api/jobs/100/stop", headers=headers)
    resp = restConn.getresponse()
    assert(resp.status == 200)
    resp.close()
    restConn.close()
    # Now check that the job has been stopped.


def test_GET_api_job_100():
    restConn = http.client.HTTPConnection("127.0.0.1", 8080)
    headers = {'Content-type': 'application/json;charset=utf-8'}
    restConn.connect()
    restConn.request("GET", "/api/jobs/100", headers=headers)
    resp = restConn.getresponse()
    assert(resp.status == 200)
    bytedata = resp.read()
    data = json.loads(bytes.decode(bytedata, "utf-8"))
    restConn.close()
    assert (data["id"] == 100)
    assert (data["status"] == "stopped")
    assert (data["command"] == "ping -n 5 127.0.0.1")


def test_GET_api_job_99():
    restConn = http.client.HTTPConnection("127.0.0.1", 8080)
    restConn.connect()
    headers = {'Content-type': 'application/json;charset=utf-8', 'Content-length': 0}
    restConn.request('GET', '/api/jobs/99', "", headers)
    resp = restConn.getresponse()
    assert (resp.status == 200)
    bytedata = resp.read()
    data = json.loads(bytes.decode(bytedata, "utf-8"))
    restConn.close()
    assert (data["id"] == 99)
    assert (data["status"] == "running")
    assert (data["command"] == "ping -n 5 127.0.0.1")


def test_GET_api_job_0():
    time.sleep(4) # Give jobs time to complete
    restConn = http.client.HTTPConnection("127.0.0.1", 8080)
    restConn.connect()
    restConn.putrequest("GET", "/api/jobs/0")
    restConn.putheader("content-type", "application/json;charset=utf-8")
    restConn.endheaders()
    resp = restConn.getresponse()
    assert(resp.status == 200)
    bytedata = resp.read()
    data = json.loads(bytes.decode(bytedata, "utf-8"))
    restConn.close()
    assert (data["id"] == 0)
    assert (data["status"] == "completed")
    assert (data["command"] == "ping -n 5 127.0.0.1")
    assert(data["stdout"] != "")


def test_GET_api_job_5():
    restConn = http.client.HTTPConnection("127.0.0.1", 8080)
    restConn.connect()
    headers = {'Content-type': 'application/json;charset=utf-8', 'Content-length': 0}
    restConn.request('GET', '/api/jobs/5', "", headers)
    resp = restConn.getresponse()
    assert(resp.status == 200)
    bytedata = resp.read()
    data = json.loads(bytes.decode(bytedata, "utf-8"))
    restConn.close()
    assert (data["id"] == 5)
    assert (data["status"] == "completed")
    assert (data["command"] == "ping -n 5 127.0.0.1")
    assert (data["stdout"] != "")


def test_GET_api_job_9999():
    restConn = http.client.HTTPConnection("127.0.0.1", 8080)
    restConn.connect()
    headers = {'Content-type': 'application/json;charset=utf-8', 'Content-length': 0}
    restConn.request('GET', '/api/jobs/9999', "", headers)
    resp = restConn.getresponse()
    assert(resp.status == 404)
    bytedata = resp.read()
    data = json.loads(bytes.decode(bytedata, "utf-8"))
    restConn.close()
    assert(data["id"] == -1)


def test_GET_api_jobs():
    restConn = http.client.HTTPConnection("127.0.0.1", 8080)
    restConn.connect()
    restConn.putrequest("GET", "/api/jobs")
    restConn.putheader("content-type", "application/json;charset=utf-8")
    restConn.endheaders()
    resp = restConn.getresponse()
    assert(resp.status == 200)
    bytedata = resp.read()
    data = json.loads(bytes.decode(bytedata, "utf-8"))
    restConn.close()
    assert (len(data["jobs"]) > 0)


def test_GET_api_jobs_running():
    restConn = http.client.HTTPConnection("127.0.0.1", 8080)
    restConn.connect()
    restConn.putrequest("GET", "/api/jobs?status=running")
    restConn.putheader("content-type", "application/json;charset=utf-8")
    restConn.endheaders()
    resp = restConn.getresponse()
    assert(resp.status == 200)
    bytedata = resp.read()
    data = json.loads(bytes.decode(bytedata, "utf-8"))
    restConn.close()
    assert (len(data["jobs"]) > 0)


def test_GET_api_jobs_stopped():
    restConn = http.client.HTTPConnection("127.0.0.1", 8080)
    restConn.connect()
    restConn.putrequest("GET", "/api/jobs?status=stopped")
    restConn.putheader("content-type", "application/json;charset=utf-8")
    restConn.endheaders()
    resp = restConn.getresponse()
    assert(resp.status == 200)
    bytedata = resp.read()
    data = json.loads(bytes.decode(bytedata, "utf-8"))
    restConn.close()
    assert (len(data["jobs"]) > 0)


def test_GET_api_jobs_completed():
    restConn = http.client.HTTPConnection("127.0.0.1", 8080)
    restConn.connect()
    restConn.putrequest("GET", "/api/jobs?status=completed")
    restConn.putheader("content-type", "application/json;charset=utf-8")
    restConn.endheaders()
    resp = restConn.getresponse()
    assert(resp.status == 200)
    bytedata = resp.read()
    data = json.loads(bytes.decode(bytedata, "utf-8"))
    restConn.close()
    assert (len(data["jobs"]) > 0)


def test_POST_api_job_start_empty_command():
    testData = {"command": ""}
    jsonString = json.dumps(testData)
    restConn = http.client.HTTPConnection("127.0.0.1", 8080)
    headers = {'Content-type': 'application/json;charset=utf-8', 'Content-length': len(jsonString)}
    restConn.connect()
    restConn.request('POST', '/api/jobs', jsonString, headers)
    resp = restConn.getresponse()
    assert(resp.status == 200)
    bytedata = resp.read()
    restConn.close()
    data = json.loads(bytes.decode(bytedata, "utf-8"))
    assert(data["id"] == -1)


def test_rest_api_with_garbage_command():
    testData = {"command": "this_command_doesnt_exist even with args"}
    jsonString = json.dumps(testData)
    restConn = http.client.HTTPConnection("127.0.0.1", 8080)
    headers = {'Content-type': 'application/json;charset=utf-8', 'Content-length': len(jsonString)}
    restConn.connect()
    restConn.request('POST', '/api/jobs', jsonString, headers)
    resp = restConn.getresponse()
    assert(resp.status == 200)
    bytedata = resp.read()
    restConn.close()
    data = json.loads(bytes.decode(bytedata, "utf-8"))

    time.sleep(1) # server needs time to work out the command is garbage

    restConn1 = http.client.HTTPConnection("127.0.0.1", 8080)
    headers = {'Content-type': 'application/json;charset=utf-8'}
    restConn1.connect()
    path = "/api/jobs/{}".format(data["id"])
    restConn1.request("GET", path, headers=headers)
    resp = restConn1.getresponse()
    assert (resp.status == 200)
    bytedata = resp.read()
    data = json.loads(bytes.decode(bytedata, "utf-8"))
    restConn1.close()
    assert(data["status"] == "stopped")


def test_rest_api_false_path_GET():
    restConn = http.client.HTTPConnection("127.0.0.1", 8080)
    restConn.connect()
    headers = {'Content-type': 'application/json;charset=utf-8', 'Content-length': 0}
    restConn.request('GET', '/api/doesnt-exist', "", headers)
    resp = restConn.getresponse()
    assert (resp.status == 404)


def test_rest_api_false_path_POST():
    restConn = http.client.HTTPConnection("127.0.0.1", 8080)
    restConn.connect()
    headers = {'Content-type': 'application/json;charset=utf-8', 'Content-length': 0}
    restConn.request('POST', '/api/rubbish', "", headers)
    resp = restConn.getresponse()
    assert (resp.status == 404)


def test_rest_api_false_path_PUT():
    restConn = http.client.HTTPConnection("127.0.0.1", 8080)
    restConn.connect()
    headers = {'Content-type': 'application/json;charset=utf-8', 'Content-length': 0}
    restConn.request('PUT', '/api/rubbish', "", headers)
    resp = restConn.getresponse()
    assert (resp.status == 404)


def test_rest_api_false_path_DELETE():
    restConn = http.client.HTTPConnection("127.0.0.1", 8080)
    restConn.connect()
    headers = {'Content-type': 'application/json;charset=utf-8', 'Content-length': 0}
    restConn.request('DELETE', '/api/rubbish', "", headers)
    resp = restConn.getresponse()
    assert (resp.status == 404)


def test_rest_api_OPTIONS():
    restConn = http.client.HTTPConnection("127.0.0.1", 8080)
    restConn.connect()
    headers = {'Content-type': 'application/json;charset=utf-8', 'Content-length': 0}
    restConn.request('OPTIONS', '/path/doesnt/matter', "", headers)
    resp = restConn.getresponse()
    assert (resp.status == 200)


def test_rest_api_false_path_NON_EXISTANT():
    restConn = http.client.HTTPConnection("127.0.0.1", 8080)
    restConn.connect()
    headers = {'Content-type': 'application/json;charset=utf-8', 'Content-length': 0}
    restConn.request('NON_EXISTANT', '/api/rubbish', "", headers)
    resp = restConn.getresponse()
    assert (resp.status == 501)
