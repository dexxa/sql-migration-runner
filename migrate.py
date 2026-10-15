import os
import pathlib
import sqlite3

MIGRATIONS_DIR = pathlib.Path('migrations')
DB = os.environ.get('DB_URL', 'app.db')


def get_db():
    conn = sqlite3.connect(DB)
    conn.execute("CREATE TABLE IF NOT EXISTS schema_migrations (version TEXT PRIMARY KEY, applied_at TEXT DEFAULT (datetime('now')))")
    return conn


def run():
    conn = get_db()
    applied = {r[0] for r in conn.execute('SELECT version FROM schema_migrations')}
    for f in sorted(MIGRATIONS_DIR.glob('*.sql')):
        ver = f.stem
        if ver in applied:
            continue
        conn.executescript(f.read_text())
        conn.execute('INSERT INTO schema_migrations (version) VALUES (?)', (ver,))
        conn.commit()
        print('applied ' + ver)


if __name__ == '__main__':
    run()
