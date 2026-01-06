# ---- Silence TensorFlow warnings ----
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from flask import Flask, render_template, request, redirect, session
import sqlite3, os as _os

from extract_text import extract_text
from model import predict_fraud

app = Flask(__name__)
app.secret_key = "secure123"

UPLOAD_FOLDER = "uploads"
_os.makedirs(UPLOAD_FOLDER, exist_ok=True)

from werkzeug.security import generate_password_hash, check_password_hash
@app.route("/home")
def home():
    if "user" not in session:
        return redirect("/")
    return render_template("home.html")

# ---------- REGISTER ----------
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form.get("police_name")
        pid = request.form.get("police_id")
        pwd = generate_password_hash(request.form.get("password"))

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO police_users (police_name, police_id, password) VALUES (?,?,?)",
            (name, pid, pwd)
        )
        conn.commit()
        conn.close()

        return redirect("/home")

    return render_template("register.html")


# ---------- LOGIN ----------
@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        pid = request.form.get("police_id")
        pwd = request.form.get("password")

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT password FROM police_users WHERE police_id=?", (pid,))
        row = cur.fetchone()
        conn.close()

        if row and check_password_hash(row[0], pwd):
            session["user"] = pid
            return redirect("/home")

        return render_template("login.html", error="Invalid Police Credentials")

    return render_template("login.html")


# ---------------- UPLOAD ----------------
@app.route("/upload")
def upload():
    if "user" not in session:
        return redirect("/")
    return render_template("upload.html")

@app.route("/submit", methods=["POST"])
def submit():
    if "user" not in session:
        return redirect("/")

    file = request.files.get("file")
    if not file:
        return redirect("/upload")

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    text = extract_text(path)
    category, fraud, summary = predict_fraud(text)

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO complaints (filename, content, category, fraud_level, summary)
        VALUES (?,?,?,?,?)
    """, (file.filename, text, category, fraud, summary))
    conn.commit()
    conn.close()

    # 🔥 SEND VALUES BACK TO UPLOAD PAGE
    return render_template(
        "upload.html",
        category=category,
        fraud=fraud,
        summary=summary
    )

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # All complaints
    cur.execute("SELECT * FROM complaints ORDER BY id DESC")
    data = cur.fetchall()

    # KPI counts
    cur.execute("SELECT COUNT(*) FROM complaints")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM complaints WHERE fraud_level='High Risk'")
    high = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM complaints WHERE fraud_level='Medium Risk'")
    medium = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM complaints WHERE fraud_level='Low Risk'")
    low = cur.fetchone()[0]

    # 🔴 Critical alerts (Top 5)
    cur.execute("""
        SELECT * FROM complaints
        WHERE fraud_level='High Risk'
        ORDER BY id DESC
        LIMIT 5
    """)
    critical = cur.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        data=data[:6],
        critical=critical,
        total=total,
        high=high,
        medium=medium,
        low=low
    )


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")





if __name__ == "__main__":
    app.run(debug=True)
