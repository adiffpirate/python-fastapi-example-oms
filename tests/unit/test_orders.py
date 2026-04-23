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
