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

