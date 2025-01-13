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
    response = test_client.post("/add-connection", json=db_payload)
    response = test_client.get(f"/read/{db_payload['id']}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "SUCCESS"
    assert response_json["message"]["db_name"] == "test_database"
    assert response_json["message"]["db_type"] == "connection"
    assert response_json["message"]["db_host"] == "localhost"
    assert response_json["message"]["db_port"] == 3306

def test_update_by_id(test_client, db_payload):
    response = test_client.post("/add-connection", json=db_payload)
    response = test_client.get(f"/read/{db_payload['id']}")
    assert response.status_code == 200
    response_json = response.json()
    updated_json = response_json["message"]
    updated_json 
    updated_json["db_port"] = 3306
    updated_json["db_name"] = "test_database_2"
    
    response = test_client.put(f"/update/{db_payload['id']}", json=updated_json)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["message"]["db_port"] == 3306
    assert response_json["message"]["db_name"] == "test_database_2"

def test_delete_by_id(test_client, db_payload):
    response = test_client.post("/add-connection", json=db_payload)
    response = test_client.delete(f"/delete/{db_payload['id']}")
    response_json = response.json()
    assert response.status_code == 200

def test_delete_all(test_client):
    response = test_client.delete("/delete-all")
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["status"] == "SUCCESS"

def test_get_empty_db(test_client, db_payload):
    response = test_client.get("/read-all")
    assert response.status_code == 404

def test_get_db_not_found(test_client,db_payload):
    response = test_client.get(f"/read/{db_payload['id']}")
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == "No database connection found"

    response = test_client.delete("/delete-all/")
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == "No database connection found"

    response = test_client.delete(f"/delete/{db_payload['id']}")
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == "No database connection found"

def test_wrong_payload(test_client):
    response = test_client.post("/add-connection", json={})
    assert response.status_code == 422
    
    response = test_client.get("/add-connection")
    assert response.status_code == 405

def test_handle_500_error(test_client,db_payload):
    response = test_client.put(f"/update/{db_payload['id']}", json=db_payload)
    assert response.status_code == 500

    


    