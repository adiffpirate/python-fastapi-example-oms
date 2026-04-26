def test_create_user_success(client):
    response = client.post("/users/register", json={
        "username": "integrationtestuser",
        "password": "testpassword123"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "integrationtestuser"
    assert "id" in data


def test_create_duplicate_user_fails(client):
    client.post("/users/register", json={
        "username": "duplicateuser",
        "password": "testpassword123"
    })

    response = client.post("/users/register", json={
        "username": "duplicateuser",
        "password": "testpassword123"
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"
