from .init_test import client, test_db


def test_user_feed_selection(test_db):
    client.post("/users/register", json={"email": "user@example.com", "password": "string"})
    token_resp = client.post("/users/login", json={"email": "user@example.com", "password": "string"})
    client.post("/feeds", json={"title": "RealPython", "link": "https://realpython.com",
                                "rss_link": "https://realpython.com/atom.xml"})
    response = client.post(f"/users/me/feeds/{1}", json={"is_selected": True},
                           headers={"Authorization": f'Bearer {token_resp.json().get("access_token")}'})
    assert response.status_code == 204

    response = client.get("/users/me/feeds",
                          headers={"Authorization": f'Bearer {token_resp.json().get("access_token")}'})
    assert response.status_code == 200
    assert response.json().get("items")[0].get("rss_link") == "https://realpython.com/atom.xml"

    response = client.post(f"/users/me/feeds/{1}", json={"is_selected": False},
                           headers={"Authorization": f'Bearer {token_resp.json().get("access_token")}'})
    assert response.status_code == 204

    response = client.get("/users/me/feeds",
                          headers={"Authorization": f'Bearer {token_resp.json().get("access_token")}'})
    assert response.status_code == 200
    assert len(response.json().get("items")) == 0

