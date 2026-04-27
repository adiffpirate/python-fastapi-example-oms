def _login(client):
    """Register a user and login to get a bearer token."""
    client.post("/users/register", json={
        "username": "testuser",
        "password": "testpassword123"
    })
    response = client.post("/users/login", json={
        "username": "testuser",
        "password": "testpassword123"
    })
    return response.json()["access_token"]


def test_create_order(client):
    token = _login(client)
    response = client.post("/orders/", json={"item": "laptop"}, headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200

    data = response.json()
    assert data["item"] == "laptop"
    assert data["status"] == "received"


def test_get_order(client):
    token = _login(client)
    created = client.post("/orders/", json={"item": "phone"}, headers={
        "Authorization": f"Bearer {token}"
    }).json()

    response = client.get(f"/orders/{created['id']}", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert response.json()["item"] == "phone"


def test_list_orders(client):
    token = _login(client)
    client.post("/orders/", json={"item": "a"}, headers={
        "Authorization": f"Bearer {token}"
    })
    client.post("/orders/", json={"item": "b"}, headers={
        "Authorization": f"Bearer {token}"
    })

    response = client.get("/orders/", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_order_status(client):
    token = _login(client)
    created = client.post("/orders/", json={"item": "widget"}, headers={
        "Authorization": f"Bearer {token}"
    }).json()
    order_id = created["id"]
    assert created["status"] == "received"

    response = client.put(f"/orders/{order_id}", json={"status": "processing"}, headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["item"] == "widget"
    assert data["status"] == "processing"

    get_response = client.get(f"/orders/{order_id}", headers={
        "Authorization": f"Bearer {token}"
    })
    assert get_response.status_code == 200
    assert get_response.json()["status"] == "processing"


def test_update_order_item(client):
    token = _login(client)
    created = client.post("/orders/", json={"item": "gadget"}, headers={
        "Authorization": f"Bearer {token}"
    }).json()
    order_id = created["id"]

    response = client.put(f"/orders/{order_id}", json={"item": "new_gadget"}, headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["item"] == "new_gadget"
    assert data["status"] == "received"

    get_response = client.get(f"/orders/{order_id}", headers={
        "Authorization": f"Bearer {token}"
    })
    assert get_response.status_code == 200
    assert get_response.json()["item"] == "new_gadget"


def test_update_order_not_found(client):
    token = _login(client)
    response = client.put("/orders/9999", json={"status": "delivered"}, headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 404


def test_delete_order(client):
    token = _login(client)
    created = client.post("/orders/", json={"item": "delete_me"}, headers={
        "Authorization": f"Bearer {token}"
    }).json()
    order_id = created["id"]

    response = client.delete(f"/orders/{order_id}", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 204

    get_response = client.get(f"/orders/{order_id}", headers={
        "Authorization": f"Bearer {token}"
    })
    assert get_response.status_code == 404


def test_delete_order_not_found(client):
    token = _login(client)
    response = client.delete("/orders/9999", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 404


def test_orders_without_auth_returns_401(client):
    response = client.get("/orders/")
    assert response.status_code == 401
