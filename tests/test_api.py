import pytest
from fastapi.testclient import TestClient
from app.main import app, items

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_store(): #Очищення списку сутностей
    items.clear()
    import app.main as main_module
    main_module.next_id = 1
    yield
    items.clear()

def test_health(): #реревірка активності сервісу
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_crud_lifecycle(): #Тести
    created = client.post("/api/items", json={"name": "Item1", "description": "Перша сутність"}) #Створення сутності методом POST
    assert created.status_code == 201
    item = created.json()
    assert item["id"] == 1
    assert item["name"] == "Item1"

    assert client.get("/api/items").json() == [item] #Отримання сутності методом GET
    assert client.get("/api/items/1").status_code == 200

    updated = client.put("/api/items/1", json={"name": "Item67", "description": "Оновлена сутність"}) #Оновлення сутності методом PUT
    assert updated.status_code == 200
    assert updated.json()["name"] == "Item67"

    deleted = client.delete("/api/items/1") #Видалення сутності методом DELETE
    assert deleted.status_code == 204
    assert client.get("/api/items/1").status_code == 404

def test_missing_item_returns_404(): #Перевірка після видалення
    assert client.get("/api/items/999").status_code == 404
    assert client.put("/api/items/999", json={"name": "X"}).status_code == 404
    assert client.delete("/api/items/999").status_code == 404

def test_validation_error(): #Перевірка валідації запитів
    response = client.post("/api/items", json={"name": ""})
    assert response.status_code == 422
