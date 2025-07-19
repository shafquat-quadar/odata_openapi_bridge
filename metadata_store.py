import sqlite3
from datetime import datetime
from typing import Optional, List, Tuple, Dict

DB_PATH = "db/metadata.sqlite"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS odata_services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_url TEXT NOT NULL,
            metadata_json TEXT,
            version_hash TEXT,
            active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def add_service(service_url: str, metadata_json: str, version_hash: str) -> int:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO odata_services (service_url, metadata_json, version_hash) VALUES (?, ?, ?)",
        (service_url, metadata_json, version_hash),
    )
    conn.commit()
    service_id = c.lastrowid
    conn.close()
    return service_id


def list_services() -> List[Dict]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT id, service_url, active, created_at, last_updated FROM odata_services"
    )
    rows = c.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "service_url": r[1],
            "active": bool(r[2]),
            "created_at": r[3],
            "last_updated": r[4],
        }
        for r in rows
    ]


def get_service(service_id: int) -> Optional[Dict]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT id, service_url, metadata_json, version_hash, active FROM odata_services WHERE id = ?",
        (service_id,),
    )
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "service_url": row[1],
            "metadata_json": row[2],
            "version_hash": row[3],
            "active": bool(row[4]),
        }
    return None


def toggle_service(service_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "UPDATE odata_services SET active = NOT active, last_updated = ? WHERE id = ?",
        (datetime.utcnow(), service_id),
    )
    conn.commit()
    conn.close()


def delete_service(service_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM odata_services WHERE id = ?", (service_id,))
    conn.commit()
    conn.close()


def update_metadata(service_id: int, metadata_json: str, version_hash: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "UPDATE odata_services SET metadata_json = ?, version_hash = ?, last_updated = ? WHERE id = ?",
        (metadata_json, version_hash, datetime.utcnow(), service_id),
    )
    conn.commit()
    conn.close()
