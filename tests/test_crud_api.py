
def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "SUCCESS"

def test_create_db(test_client, db_payload):
    response = test_client.post("/add-connection", json=db_payload)
    response_json = response.json()
    assert response.status_code == 200

def test_get_db(test_client, db_payload):
    response = test_client.get("/read-all")
    assert response.status_code == 200

def test_get_by_id(test_client, db_payload):
    response = test_client.get("/read/1")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "SUCCESS"
    assert response_json["message"]["db_name"] == "test_database"
    assert response_json["message"]["db_type"] == "connection"
    assert response_json["message"]["db_host"] == "localhost"
    assert response_json["message"]["db_port"] == 3306

def test_update_by_id(test_client, db_payload):
    response = test_client.get("/read/1")
    assert response.status_code == 200
    response_json = response.json()
    updated_json = response_json["message"]
    updated_json 
    updated_json["db_port"] = 3306
    updated_json["db_name"] = "test_database_2"
    
    response = test_client.put("/update/1", json=updated_json)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["message"]["db_port"] == 3306
    assert response_json["message"]["db_name"] == "test_database_2"


def test_delete_by_id(test_client, db_payload):
    response = test_client.delete("/delete/1")
    response_json = response.json()
    assert response.status_code == 200


def test_get_db_not_found(test_client):
    response = test_client.get("/read/10")
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == "No database connection found"


def test_wrong_payload(test_client):
    response = test_client.post("/add-connection", json={})
    assert response.status_code == 422
