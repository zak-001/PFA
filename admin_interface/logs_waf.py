import time
import json
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from sqlalchemy import insert
from db import engine
from models import WAFLog

LOG_PATH = "/mnt/modsec-logs/modsec_audit.log"

def insert_log(client_ip, host_cible, uri, method, attack_type, status, created_at):
    with engine.begin() as conn:
        conn.execute(insert(WAFLog).values(
            client_ip=client_ip,
            host_cible=host_cible,
            uri=uri,
            method=method,
            attack_type=attack_type,
            status=status,
            created_at=created_at
        ))

def parse_and_insert(line):
    try:
        entry = json.loads(line.strip())
        tx = entry.get("transaction", {})
        client_ip = tx.get("client_ip")
        uri = tx.get("request", {}).get("uri", "/").split('?')[0]
        created_at = tx.get("time_stamp")
        date = datetime.strptime(created_at, "%a %b %d %H:%M:%S %Y")
        method = tx.get("request", {}).get("method", "UNKNOWN")
        host_cible = tx.get("request", {}).get("headers", {}).get("Host", "UNKNOWN")

        messages = tx.get("messages", [])
        attack_type = ""
        if messages and "details" in messages[0]:
            tags = messages[0]["details"].get("tags", [])
            if len(tags) >= 4:
                attack_type = tags[3]

        status = "blocked" if tx.get("response", {}).get("http_code", 0) == 403 else "allowed"

        insert_log(client_ip, host_cible, uri, method, attack_type, status, date)
        print(f"[OK] {client_ip} {host_cible} {uri} {method} {attack_type} {status} {date}")

    except Exception as e:
        print(f"[ERREUR] Ligne ignorée : {e}")

class LogHandler(FileSystemEventHandler):
    def __init__(self):
        self._seek_end()

    def _seek_end(self):
        self._file = open(LOG_PATH, "r")
        self._file.seek(0, 2)  # end of file

    def on_modified(self, event):
        if event.src_path.endswith("modsec_audit.log"):
            for line in self._file:
                parse_and_insert(line)

if __name__ == "__main__":
    print("[INFO] Surveillance du fichier de logs…")
    event_handler = LogHandler()
    observer = Observer()
    observer.schedule(event_handler, path="/mnt/modsec-logs", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
