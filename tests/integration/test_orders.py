def test_create_order(client):
    response = client.post("/orders/", json={"item": "laptop"})
    assert response.status_code == 200

    data = response.json()
    assert data["item"] == "laptop"
    assert data["status"] == "received"


def test_get_order(client):
    created = client.post("/orders/", json={"item": "phone"}).json()

    response = client.get(f"/orders/{created['id']}")
    assert response.status_code == 200
    assert response.json()["item"] == "phone"


def test_list_orders(client):
    client.post("/orders/", json={"item": "a"})
    client.post("/orders/", json={"item": "b"})

    response = client.get("/orders/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_order_status(client):
    created = client.post("/orders/", json={"item": "widget"}).json()
    order_id = created["id"]
    assert created["status"] == "received"

    response = client.put(f"/orders/{order_id}", json={"status": "processing"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["item"] == "widget"
    assert data["status"] == "processing"

    get_response = client.get(f"/orders/{order_id}")
    assert get_response.status_code == 200
    assert get_response.json()["status"] == "processing"


def test_update_order_item(client):
    created = client.post("/orders/", json={"item": "gadget"}).json()
    order_id = created["id"]

    response = client.put(f"/orders/{order_id}", json={"item": "new_gadget"})
    assert response.status_code == 200
    data = response.json()
    assert data["item"] == "new_gadget"
    assert data["status"] == "received"

    get_response = client.get(f"/orders/{order_id}")
    assert get_response.status_code == 200
    assert get_response.json()["item"] == "new_gadget"


def test_update_order_not_found(client):
    response = client.put("/orders/9999", json={"status": "delivered"})
    assert response.status_code == 404


def test_delete_order(client):
    created = client.post("/orders/", json={"item": "delete_me"}).json()
    order_id = created["id"]

    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 204

    get_response = client.get(f"/orders/{order_id}")
    assert get_response.status_code == 404


def test_delete_order_not_found(client):
    response = client.delete("/orders/9999")
    assert response.status_code == 404
