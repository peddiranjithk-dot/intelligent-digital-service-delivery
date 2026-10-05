import sqlite3
from datetime import datetime
from flask import Flask, g, jsonify, render_template, request
from classifier import classify

DB = "services.db"
STATUSES = ["Submitted", "Assigned", "In Progress", "Resolved"]
app = Flask(__name__)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_):
    db = g.pop("db", None)
    if db:
        db.close()


def init_db():
    with sqlite3.connect(DB) as db:
        db.execute("""CREATE TABLE IF NOT EXISTS requests(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, contact TEXT, description TEXT,
            category TEXT, priority TEXT,
            status TEXT DEFAULT 'Submitted', created_at TEXT)""")


@app.route("/")
def index():
    return render_template("index.html", statuses=STATUSES)


@app.post("/api/requests")
def create_request():
    d = request.get_json(force=True)
    if not d.get("name") or not d.get("description"):
        return jsonify(error="name and description are required"), 400
    category, priority = classify(d["description"])
    db = get_db()
    cur = db.execute(
        "INSERT INTO requests(name,contact,description,category,priority,created_at) VALUES(?,?,?,?,?,?)",
        (d["name"], d.get("contact", ""), d["description"], category, priority,
         datetime.now().isoformat(timespec="seconds")))
    db.commit()
    return jsonify(id=cur.lastrowid, category=category, priority=priority, status="Submitted"), 201


@app.get("/api/requests")
def list_requests():
    order = "CASE priority WHEN 'High' THEN 0 WHEN 'Medium' THEN 1 ELSE 2 END, id DESC"
    rows = get_db().execute(f"SELECT * FROM requests ORDER BY {order}").fetchall()
    return jsonify([dict(r) for r in rows])


@app.get("/api/requests/<int:rid>")
def get_request(rid):
    r = get_db().execute("SELECT * FROM requests WHERE id=?", (rid,)).fetchone()
    return (jsonify(dict(r)) if r else (jsonify(error="not found"), 404))


@app.patch("/api/requests/<int:rid>")
def update_status(rid):
    status = (request.get_json(force=True) or {}).get("status")
    if status not in STATUSES:
        return jsonify(error=f"status must be one of {STATUSES}"), 400
    db = get_db()
    db.execute("UPDATE requests SET status=? WHERE id=?", (status, rid))
    db.commit()
    return jsonify(id=rid, status=status)


@app.get("/api/stats")
def stats():
    db = get_db()
    by = lambda col: {r[0]: r[1] for r in db.execute(f"SELECT {col}, COUNT(*) FROM requests GROUP BY {col}")}
    return jsonify(by_category=by("category"), by_status=by("status"), by_priority=by("priority"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
