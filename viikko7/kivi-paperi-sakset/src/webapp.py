import sys
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, session

# Ensure we can import modules from src when running via Flask or python
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
SRC_DIR = CURRENT_DIR
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from tuomari import Tuomari
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu

app = Flask(__name__)
# Simple dev secret key for session; replace in production
app.secret_key = "dev-secret-key-rps"

VALID_MOVES = {"k", "p", "s"}


def reset_game_state():
    session.clear()


def init_game(mode: str):
    session["mode"] = mode  # 'a' human vs human, 'b' vs ai, 'c' vs better ai
    session["tuomari"] = {"ekan": 0, "tokan": 0, "tasapelit": 0}
    if mode == "b":
        # basic AI state
        session["ai"] = {"type": "basic", "_siirto": 0}
    elif mode == "c":
        # better AI with memory of size 10
        session["ai"] = {"type": "better", "_muisti": [None] * 10, "_vapaa_muisti_indeksi": 0}
    else:
        session["ai"] = None


def ai_next_move():
    ai = session.get("ai")
    if not ai:
        return None
    if ai["type"] == "basic":
        # emulate Tekoaly.anna_siirto
        ai["_siirto"] = (ai["_siirto"] + 1) % 3
        if ai["_siirto"] == 0:
            return "k"
        elif ai["_siirto"] == 1:
            return "p"
        else:
            return "s"
    else:
        # emulate TekoalyParannettu.anna_siirto
        idx = ai["_vapaa_muisti_indeksi"]
        if idx == 0 or idx == 1:
            return "k"
        viimeisin = ai["_muisti"][idx - 1]
        k = p = s = 0
        for i in range(0, idx - 1):
            if viimeisin == ai["_muisti"][i]:
                seuraava = ai["_muisti"][i + 1]
                if seuraava == "k":
                    k += 1
                elif seuraava == "p":
                    p += 1
                else:
                    s += 1
        if k > p or k > s:
            return "p"
        elif p > k or p > s:
            return "s"
        else:
            return "k"


def ai_record_human_move(move: str):
    ai = session.get("ai")
    if not ai:
        return
    if ai["type"] == "basic":
        # Tekoaly.aseta_siirto does nothing
        return
    # emulate TekoalyParannettu.aseta_siirto
    idx = ai["_vapaa_muisti_indeksi"]
    muisti = ai["_muisti"]
    if idx == len(muisti):
        # shift left
        for i in range(1, len(muisti)):
            muisti[i - 1] = muisti[i]
        ai["_vapaa_muisti_indeksi"] = idx - 1
        idx = ai["_vapaa_muisti_indeksi"]
    muisti[idx] = move
    ai["_vapaa_muisti_indeksi"] = idx + 1


def update_scores(ekan_siirto: str, tokan_siirto: str):
    # Reuse Tuomari logic by instantiating and syncing counts from session
    t_state = session.get("tuomari", {"ekan": 0, "tokan": 0, "tasapelit": 0})
    t = Tuomari()
    t.ekan_pisteet = t_state.get("ekan", 0)
    t.tokan_pisteet = t_state.get("tokan", 0)
    t.tasapelit = t_state.get("tasapelit", 0)
    t.kirjaa_siirto(ekan_siirto, tokan_siirto)
    session["tuomari"] = {"ekan": t.ekan_pisteet, "tokan": t.tokan_pisteet, "tasapelit": t.tasapelit}


@app.get("/")
def menu():
    return render_template("menu.html")


@app.post("/start")
def start():
    mode = request.form.get("mode")
    if mode not in {"a", "b", "c"}:
        reset_game_state()
        return redirect(url_for("menu"))
    init_game(mode)
    return redirect(url_for("play"))


@app.get("/play")
def play():
    mode = session.get("mode")
    t = session.get("tuomari", {"ekan": 0, "tokan": 0, "tasapelit": 0})
    message = session.pop("message", None)
    # Hot seat: step 1 asks for player 1 move, step 2 asks for player 2
    hot_seat_step = None
    if mode == "a":
        hot_seat_step = 2 if session.get("pending_move1") else 1

    return render_template(
        "play.html",
        mode=mode,
        scores=t,
        last_moves=session.get("last_moves"),
        message=message,
        hot_seat_step=hot_seat_step,
    )


@app.post("/play")
def play_post():
    mode = session.get("mode")
    if not mode:
        # Fallback: try to recover mode from form if session cookie was lost
        fallback_mode = request.form.get("mode")
        if fallback_mode in {"a", "b", "c"}:
            init_game(fallback_mode)
            mode = fallback_mode
        else:
            return redirect(url_for("menu"))

    # Human vs human hot seat: collect moves in two steps
    if mode == "a":
        pending = session.get("pending_move1")
        if not pending:
            # Step 1: receive first player's move
            move1 = request.form.get("move1", "")
            if move1 not in VALID_MOVES:
                session["message"] = "Virheellinen siirto, anna k/p/s"
                return redirect(url_for("play"))
            session["pending_move1"] = move1
            return redirect(url_for("play"))
        else:
            # Step 2: receive second player's move
            move2 = request.form.get("move2", "")
            if move2 not in VALID_MOVES:
                session["message"] = "Virheellinen siirto, anna k/p/s"
                return redirect(url_for("play"))
            move1 = session.pop("pending_move1")
            update_scores(move1, move2)
            session["last_moves"] = {"first": move1, "second": move2}
    else:
        # vs AI: single step
        move1 = request.form.get("move1", "")
        if move1 not in VALID_MOVES:
            session["message"] = "Virheellinen siirto, anna k/p/s"
            return redirect(url_for("play"))
        move2 = ai_next_move()
        # record human move for better AI
        ai_record_human_move(move1)
        update_scores(move1, move2)
        session["last_moves"] = {"first": move1, "second": move2}

    # Check victory condition: first to 3 wins
    t = session.get("tuomari", {"ekan": 0, "tokan": 0, "tasapelit": 0})
    if t.get("ekan", 0) >= 3 or t.get("tokan", 0) >= 3:
        return redirect(url_for("finish"))
    return redirect(url_for("play"))


@app.get("/finish")
def finish():
    t = session.get("tuomari", {"ekan": 0, "tokan": 0, "tasapelit": 0})
    reset_game_state()
    return render_template("finish.html", final_scores=t)


if __name__ == "__main__":
    # Dev server for quick run
    app.run(host="127.0.0.1", port=5000, debug=True)
