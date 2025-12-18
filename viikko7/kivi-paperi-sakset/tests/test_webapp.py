import sys
from pathlib import Path

# Ensure we can import the app from src
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

import pytest
from webapp import app

app.config["TESTING"] = True


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_menu_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Kivi-Paperi-Sakset" in resp.data


def test_start_invalid_mode_redirects_to_menu(client):
    resp = client.post("/start", data={"mode": "x"}, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Kivi-Paperi-Sakset" in resp.data


def test_start_human_vs_human_and_play_round(client):
    # Start game mode a (human vs human)
    resp = client.post("/start", data={"mode": "a"}, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Pelitilanne" in resp.data

    # Hot seat: first submit player 1 move
    resp = client.post(
        "/play",
        data={"mode": "a", "move1": "k"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    # No last moves yet
    assert b"Viimeisin kierros" not in resp.data

    # Then submit player 2 move
    resp = client.post(
        "/play",
        data={"mode": "a", "move2": "s"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    # Score should show Eka: 1 | Toka: 0
    assert b"Eka: 1" in resp.data
    assert b"Toka: 0" in resp.data
    assert b"Tasapelit: 0" in resp.data
    # Last moves should be visible
    assert b"eka = k, toka = s" in resp.data


def test_invalid_move_keeps_game_running(client):
    # Start game
    client.post("/start", data={"mode": "a"}, follow_redirects=True)
    # Invalid input should not finish game, shows message and stays on play page
    resp = client.post(
        "/play",
        data={"mode": "a", "move1": "x", "move2": "k"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Pelitilanne" in resp.data
    assert b"Virheellinen siirto" in resp.data


def test_start_vs_basic_ai_and_play_round(client):
    # Start game mode b (vs basic AI)
    resp = client.post("/start", data={"mode": "b"}, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Pelitilanne" in resp.data

    # First AI move should be 'p' (basic ai cycles k->p->s starting at p)
    resp = client.post(
        "/play",
        data={"mode": "b", "move1": "k"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    # Human chose k, AI chose p -> AI wins -> Toka: 1
    assert b"Toka: 1" in resp.data
    assert b"Eka: 0" in resp.data
    assert b"eka = k" in resp.data


def test_game_finishes_when_player_reaches_three_wins(client):
    # Start game mode a (human vs human)
    client.post("/start", data={"mode": "a"}, follow_redirects=True)
    # Play 3 winning rounds for player 1: k vs s
    for _ in range(3):
        client.post(
            "/play",
            data={"mode": "a", "move1": "k"},
            follow_redirects=True,
        )
        resp = client.post(
            "/play",
            data={"mode": "a", "move2": "s"},
            follow_redirects=True,
        )
    assert resp.status_code == 200
    # Should be on finish page now
    assert b"Kiitos!" in resp.data
    assert b"Eka: 3" in resp.data


def test_start_vs_better_ai_and_play_round(client):
    # Start game mode c (vs better AI)
    resp = client.post("/start", data={"mode": "c"}, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Pelitilanne" in resp.data

    # Better AI returns 'k' initially; human picks 'p' -> human wins
    resp = client.post(
        "/play",
        data={"mode": "c", "move1": "p"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Eka: 1" in resp.data
    assert b"Toka: 0" in resp.data
