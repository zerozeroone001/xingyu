from fastapi.testclient import TestClient
from sqlalchemy import func, select
from uuid import uuid4

from app.db import models
from app.db.session import SessionLocal
from app.main import app


def login_headers(client: TestClient) -> dict[str, str]:
    code = f"test-{uuid4().hex}"
    login = client.post(
        "/api/v1/auth/wx-login",
        json={"code": code, "profile": {"nickname": "测试用户"}},
    )
    assert login.status_code == 200
    token = login.json()["data"]["token"]
    return {"Authorization": f"Bearer {token}"}


def admin_headers(client: TestClient) -> dict[str, str]:
    login = client.post(
        "/api/v1/admin/auth/login",
        json={"username": "admin", "password": "admin123456"},
    )
    assert login.status_code == 200
    token = login.json()["data"]["token"]
    return {"Authorization": f"Bearer {token}"}


def test_health_home_and_login_flow():
    with TestClient(app) as client:
        health = client.get("/api/v1/health")
        assert health.status_code == 200
        assert health.json()["data"]["status"] == "ok"

        home = client.get("/api/v1/home")
        assert home.status_code == 200
        assert home.json()["code"] == 0
        assert home.json()["data"]["today_poem"] is not None

        login = client.post(
            "/api/v1/auth/wx-login",
            json={"code": "guest", "profile": {"nickname": "测试用户"}},
        )
        assert login.status_code == 200
        token = login.json()["data"]["token"]
        assert token

        me = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
        assert me.status_code == 200
        assert me.json()["data"]["nickname"] == "测试用户"


def test_core_api_contracts():
    with TestClient(app) as client:
        headers = login_headers(client)

        poems = client.get("/api/v1/poems", params={"page": 1, "page_size": 2})
        assert poems.status_code == 200
        assert poems.json()["data"]["page_size"] == 2
        assert poems.json()["data"]["total"] >= 250
        first_poem = poems.json()["data"]["items"][0]
        assert "translation" not in first_poem
        assert "annotation" not in first_poem
        assert "appreciation" not in first_poem

        search = client.get("/api/v1/poems/search", params={"keyword": "月"})
        assert search.status_code == 200
        assert "items" in search.json()["data"]

        categories = client.get("/api/v1/categories")
        assert categories.status_code == 200
        assert categories.json()["data"]["items"]
        assert categories.json()["data"]["items"][0]["poem_count"] >= 1
        assert categories.json()["data"]["items"][0]["poemCount"] >= 1
        category_id = categories.json()["data"]["items"][0]["id"]
        category_poems = client.get(f"/api/v1/categories/{category_id}/poems")
        assert category_poems.status_code == 200

        favorite = client.post("/api/v1/favorites/1", headers=headers)
        assert favorite.status_code == 200
        assert favorite.json()["data"]["is_favorite"] is True
        assert client.get("/api/v1/favorites", headers=headers).json()["data"]["total"] >= 1
        poem_one = client.get("/api/v1/poems/1", headers=headers).json()["data"]
        poem_like = client.post("/api/v1/poems/1/like", headers=headers)
        assert poem_like.status_code == 200
        assert poem_like.json()["data"]["is_liked"] is True
        assert poem_like.json()["data"]["like_count"] >= poem_one["like_count"]
        poem_unlike = client.delete("/api/v1/poems/1/like", headers=headers)
        assert poem_unlike.status_code == 200
        assert poem_unlike.json()["data"]["is_liked"] is False
        poem_share = client.post("/api/v1/poems/1/share")
        assert poem_share.status_code == 200
        assert poem_share.json()["data"]["share_count"] >= poem_one["share_count"]

        history = client.post("/api/v1/history/1", headers=headers)
        assert history.status_code == 200
        assert client.get("/api/v1/history", headers=headers).json()["data"]["total"] >= 1

        created = client.post(
            "/api/v1/square/feed",
            headers=headers,
            json={"content": "今晚读到明月松间照。", "tags": ["摘句"]},
        )
        assert created.status_code == 200
        topic_id = created.json()["data"]["id"]
        liked = client.post(f"/api/v1/square/feed/{topic_id}/like", headers=headers)
        assert liked.status_code == 200
        assert liked.json()["data"]["id"] == topic_id
        assert "content" in liked.json()["data"]
        shared = client.post(f"/api/v1/square/feed/{topic_id}/share")
        assert shared.status_code == 200
        assert shared.json()["data"]["id"] == topic_id
        commented = client.post(
            f"/api/v1/square/feed/{topic_id}/comments",
            headers=headers,
            json={"content": "这句很适合夜读。"},
        )
        assert commented.status_code == 200
        assert commented.json()["data"]["comments"]

        answer = client.post("/api/v1/feihualing/check", json={"keyword": "月", "answer": "床前看月光"})
        assert answer.status_code == 200
        assert answer.json()["data"]["score"] == 10
        record = client.post("/api/v1/feihualing/records", headers=headers, json=answer.json()["data"])
        assert record.status_code == 200
        assert client.get("/api/v1/feihualing/records", headers=headers).json()["data"]["total"] >= 1

        room = client.post(
            "/api/v1/feihualing/rooms",
            headers=headers,
            json={"keyword": "月", "title": "测试雅集", "maxPlayers": 4},
        )
        assert room.status_code == 200
        assert client.get(f"/api/v1/feihualing/rooms/{room.json()['data']['id']}").status_code == 200
        rooms = client.get("/api/v1/feihualing/rooms")
        assert rooms.status_code == 200
        first_room = rooms.json()["data"]["items"][0]
        assert "latestLine" in first_room
        assert "statusText" in first_room
        assert "resultText" in first_room

        feedback = client.post("/api/v1/feedback", headers=headers, json={"content": "测试反馈"})
        assert feedback.status_code == 200
        assert feedback.json()["data"]["status"] == "received"


def test_imported_poetry_counts_and_name_table():
    with SessionLocal() as db:
        poem_total = db.scalar(select(func.count()).select_from(models.Poem))
        name_total = db.scalar(select(func.count()).select_from(models.PoemName))
        ci_total = db.scalar(select(func.count()).select_from(models.Poem).where(models.Poem.dynasty == "宋"))
        yuan_total = db.scalar(select(func.count()).select_from(models.Poem).where(models.Poem.dynasty == "元"))
        ming_total = db.scalar(select(func.count()).select_from(models.Poem).where(models.Poem.dynasty == "明"))
        qing_total = db.scalar(select(func.count()).select_from(models.Poem).where(models.Poem.dynasty == "清"))

        traditional_chars = "駱賓靜牀爲為無風國雲鄉樓萬"
        traditional_total = sum(
            db.scalar(
                select(func.count())
                .select_from(models.Poem)
                .where(
                    models.Poem.title.contains(char)
                    | models.Poem.author.contains(char)
                    | models.Poem.content.contains(char)
                )
            )
            or 0
            for char in traditional_chars
        )

    assert poem_total >= 930
    assert name_total == poem_total
    assert ci_total >= 200
    assert yuan_total >= 200
    assert ming_total >= 30
    assert qing_total >= 200
    assert traditional_total == 0


def test_admin_console_core_flow():
    with TestClient(app) as client:
        headers = admin_headers(client)

        dashboard = client.get("/api/v1/admin/dashboard", headers=headers)
        assert dashboard.status_code == 200
        assert dashboard.json()["data"]["counts"]["poems"] >= 1

        categories = client.get("/api/v1/admin/categories", headers=headers)
        assert categories.status_code == 200
        category_items = categories.json()["data"]["items"]
        category_ids = [category_items[0]["id"]] if category_items else []

        created = client.post(
            "/api/v1/admin/poems",
            headers=headers,
            json={
                "title": f"Admin Test Poem {uuid4().hex}",
                "dynasty": "Test",
                "author": "Admin",
                "content": "line one\nline two",
                "recommend_sentence": "line one",
                "tags": ["test", "admin"],
                "category_ids": category_ids,
                "like_count": 1,
                "favorite_count": 2,
                "share_count": 3,
            },
        )
        assert created.status_code == 200
        poem_id = created.json()["data"]["id"]

        updated = client.put(
            f"/api/v1/admin/poems/{poem_id}",
            headers=headers,
            json={
                "title": "Admin Test Poem Updated",
                "dynasty": "Test",
                "author": "Admin",
                "content": "updated",
                "recommend_sentence": "updated",
                "tags": ["updated"],
                "category_ids": category_ids,
                "like_count": 4,
                "favorite_count": 5,
                "share_count": 6,
            },
        )
        assert updated.status_code == 200
        assert updated.json()["data"]["title"] == "Admin Test Poem Updated"

        listed = client.get("/api/v1/admin/poems", headers=headers, params={"keyword": "Admin Test Poem Updated"})
        assert listed.status_code == 200
        assert listed.json()["data"]["total"] >= 1

        feedback = client.post("/api/v1/feedback", json={"content": "admin flow feedback"})
        assert feedback.status_code == 200
        feedback_id = feedback.json()["data"]["id"]
        feedback_update = client.put(
            f"/api/v1/admin/feedback/{feedback_id}",
            headers=headers,
            json={"status": "resolved"},
        )
        assert feedback_update.status_code == 200
        assert feedback_update.json()["data"]["status"] == "resolved"

        deleted = client.delete(f"/api/v1/admin/poems/{poem_id}", headers=headers)
        assert deleted.status_code == 200
        assert deleted.json()["data"]["deleted"] is True
