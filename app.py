import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "certificates.db")

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

app.secret_key = "digital-document-secret-key"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS certificates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            certificate_id TEXT UNIQUE NOT NULL,
            student_name TEXT NOT NULL,
            course TEXT NOT NULL,
            institution TEXT NOT NULL,
            issue_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Valid'
        )
    """)

    conn.commit()
    conn.close()


def get_all_certificates():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM certificates
        ORDER BY id DESC
    """)

    certificates = cursor.fetchall()
    conn.close()

    return certificates
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "GET":
        return render_template("verify.html")

    certificate_id = request.form.get("certificate_id", "").strip()

    if not certificate_id:
        return render_template(
            "verify.html",
            error="Please enter a Certificate ID."
        )

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM certificates WHERE certificate_id = ?",
        (certificate_id,)
    )

    certificate = cursor.fetchone()
    conn.close()

    if certificate:
        return render_template(
            "result.html",
            certificate=certificate,
            valid=True
        )

    return render_template(
        "result.html",
        certificate=None,
        certificate_id=certificate_id,
        valid=False
    )
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))

        return render_template(
            "admin_login.html",
            error="Invalid username or password."
        )

    return render_template("admin_login.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    certificates = get_all_certificates()

    return render_template(
        "admin_dashboard.html",
        certificates=certificates
    )
@app.route("/admin/add", methods=["POST"])
def add_certificate():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    certificate_id = request.form.get("certificate_id", "").strip()
    student_name = request.form.get("student_name", "").strip()
    course = request.form.get("course", "").strip()
    institution = request.form.get("institution", "").strip()
    issue_date = request.form.get("issue_date", "").strip()
    status = request.form.get("status", "Valid").strip()

    if not certificate_id or not student_name or not course:
        return render_template(
            "admin_dashboard.html",
            certificates=get_all_certificates(),
            error="Certificate ID, student name and course are required."
        )

    if not institution:
        institution = "Digital Document Verification System"

    if not issue_date:
        issue_date = "2026-09-27"

    if not status:
        status = "Valid"

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO certificates
            (certificate_id, student_name, course, institution, issue_date, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            certificate_id,
            student_name,
            course,
            institution,
            issue_date,
            status
        ))

        conn.commit()

    except sqlite3.IntegrityError:
        conn.close()

        return render_template(
            "admin_dashboard.html",
            certificates=get_all_certificates(),
            error="Certificate ID already exists."
        )

    conn.close()

    return redirect(url_for("admin_dashboard"))
@app.route("/admin/delete/<int:certificate_id>", methods=["GET", "POST"])
def delete_certificate(certificate_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM certificates WHERE id = ?",
        (certificate_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("admin_dashboard"))


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("home"))
if __name__ == "__main__":
    init_database()

    print("==============================================")
    print("Digital Document Verification System")
    print("==============================================")
    print("Admin Username :", ADMIN_USERNAME)
    print("Admin Password :", ADMIN_PASSWORD)
    print("Database       :", DB_PATH)
    print("Templates      :", os.path.join(BASE_DIR, "templates"))
    print("Static         :", os.path.join(BASE_DIR, "static"))
    print("==============================================")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )