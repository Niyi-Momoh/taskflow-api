def test_create_task(client, auth_headers):
    resp = client.post("/tasks/", json={"title": "Buy milk"}, headers=auth_headers)
    assert resp.status_code == 201
    assert resp.json()["title"] == "Buy milk"
    assert resp.json()["completed"] is False
    assert resp.json()["priority"] == "medium"


def test_list_tasks(client, auth_headers):
    client.post("/tasks/", json={"title": "Task 1"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "Task 2"}, headers=auth_headers)
    resp = client.get("/tasks/", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_filter_by_completed(client, auth_headers):
    client.post("/tasks/", json={"title": "Done"}, headers=auth_headers)
    task = client.post("/tasks/", json={"title": "Pending"}, headers=auth_headers).json()
    client.patch(f"/tasks/{task['id']}", json={"completed": True}, headers=auth_headers)

    done = client.get("/tasks/?completed=true", headers=auth_headers).json()
    pending = client.get("/tasks/?completed=false", headers=auth_headers).json()
    assert len(done) == 1
    assert len(pending) == 1


def test_filter_by_priority(client, auth_headers):
    client.post("/tasks/", json={"title": "High", "priority": "high"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "Low", "priority": "low"}, headers=auth_headers)
    resp = client.get("/tasks/?priority=high", headers=auth_headers)
    assert len(resp.json()) == 1
    assert resp.json()[0]["title"] == "High"


def test_get_task(client, auth_headers):
    task_id = client.post("/tasks/", json={"title": "Buy milk"}, headers=auth_headers).json()["id"]
    resp = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["title"] == "Buy milk"


def test_get_task_not_found(client, auth_headers):
    resp = client.get("/tasks/9999", headers=auth_headers)
    assert resp.status_code == 404


def test_update_task(client, auth_headers):
    task_id = client.post("/tasks/", json={"title": "Old"}, headers=auth_headers).json()["id"]
    resp = client.patch(f"/tasks/{task_id}", json={"title": "New", "completed": True}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["title"] == "New"
    assert resp.json()["completed"] is True


def test_delete_task(client, auth_headers):
    task_id = client.post("/tasks/", json={"title": "Delete me"}, headers=auth_headers).json()["id"]
    resp = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert resp.status_code == 204
    assert client.get(f"/tasks/{task_id}", headers=auth_headers).status_code == 404


def test_cross_user_isolation(client, auth_headers, other_auth_headers):
    task_id = client.post("/tasks/", json={"title": "Private"}, headers=auth_headers).json()["id"]
    resp = client.get(f"/tasks/{task_id}", headers=other_auth_headers)
    assert resp.status_code == 404
