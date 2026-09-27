import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "certificates.db")


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS certificates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            certificate_id TEXT UNIQUE NOT NULL,
            holder_name TEXT NOT NULL,
            certificate_type TEXT NOT NULL,
            institution TEXT NOT NULL,
            issue_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_certificate(
    certificate_id,
    holder_name,
    certificate_type,
    institution,
    issue_date,
    status="Pending",
    created_at=""
):
    connection = get_connection()

    connection.execute("""
        INSERT INTO certificates (
            certificate_id,
            holder_name,
            certificate_type,
            institution,
            issue_date,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        certificate_id,
        holder_name,
        certificate_type,
        institution,
        issue_date,
        status,
        created_at
    ))

    connection.commit()
    connection.close()


def get_certificate(certificate_id):
    connection = get_connection()

    certificate = connection.execute("""
        SELECT *
        FROM certificates
        WHERE certificate_id = ?
    """, (certificate_id,)).fetchone()

    connection.close()

    return certificate


def get_all_certificates():
    connection = get_connection()

    certificates = connection.execute("""
        SELECT *
        FROM certificates
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    return certificates


def update_status(certificate_id, status):
    connection = get_connection()

    connection.execute("""
        UPDATE certificates
        SET status = ?
        WHERE certificate_id = ?
    """, (status, certificate_id))

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_table()
    print("Database initialized successfully.")