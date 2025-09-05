from sqlalchemy import text
from sqlalchemy.engine import Engine


def _column_exists(engine: Engine, table: str, column: str) -> bool:
    with engine.connect() as connection:
        result = connection.execute(text(f"PRAGMA table_info('{table}')"))
        rows = result.mappings().all()
        return any(row["name"] == column for row in rows)


def run_sqlite_migrations(engine: Engine) -> None:
    # users.role
    if not _column_exists(engine, "users", "role"):
        with engine.connect() as connection:
            connection.execute(
                text("ALTER TABLE users ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT 'employee'")
            )

    # users.date_of_birth
    if not _column_exists(engine, "users", "date_of_birth"):
        with engine.connect() as connection:
            connection.execute(
                text("ALTER TABLE users ADD COLUMN date_of_birth DATE NULL")
            )

    # attendance table creation if missing
    with engine.connect() as connection:
        exists = connection.execute(text("""
            SELECT name FROM sqlite_master WHERE type='table' AND name='attendance'
        """)).fetchone()
        if not exists:
            connection.execute(text("""
                CREATE TABLE attendance (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    started_at DATETIME NOT NULL,
                    ended_at DATETIME NULL,
                    work_date DATE NOT NULL,
                    hours REAL NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """))

