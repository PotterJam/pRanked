from utility import sqlite_db


def main():
    with sqlite_db.connection() as con:
        migrations_to_skip = 0

        # Check if the 'migrations' table exists
        result = con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='migrations'")
        table_exists = result.fetchone()

        if table_exists:
            # The 'migrations' table exists, so get the latest 'migration_id'
            max_migration_result = con.execute("SELECT MAX(migration_id) FROM migrations")
            latest_migration_id = max_migration_result.fetchone()[0]

            if latest_migration_id is not None:
                migrations_to_skip = latest_migration_id
            else:
                print("No migration_id found in the 'migrations' table.")

        counter = 0

        for migration_number, description, sql in __migrations()[migrations_to_skip:]:
            try:
                con.executescript(sql)
                __add_migration(con, migration_number, description)
                counter += 1
            except Exception:
                raise Exception(f"Failed to apply migration {migration_number}")
                sys.exit(1)

        print(f"Applied {counter} migrations. Went from version {migrations_to_skip} to {migrations_to_skip + counter}")


def __add_migration(connection, migration_id, description):
    insert_query = "INSERT INTO migrations (migration_id, description) VALUES (?, ?)"
    result = connection.execute(insert_query, (migration_id, description))
    rows_changed = result.rowcount
    if rows_changed != 1:
        print(f"Unexpected number of rows changed when adding migration. Changed {rows_changed} rows")


def __migrations():
    return [
        (
            1,
            "Initialise database",
            """
            CREATE TABLE migrations (
                migration_id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL
            );
            
            CREATE TABLE players (
                player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                current_rating REAL DEFAULT 1500 NOT NULL,
                current_rating_deviation REAL DEFAULT 350 NOT NULL
            );
            
            CREATE TABLE rating_period (
                rating_period_id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_games_played INTEGER DEFAULT NULL,
                started TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
                ended TEXT DEFAULT NULL
            );
            
            CREATE TABLE games (
                game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                rating_period_id INTEGER NOT NULL,
                date_played TEXT DEFAULT CURRENT_TIMESTAMP,
                winner_id INTEGER NOT NULL,
                loser_id INTEGER NOT NULL,
                winner_rating REAL NOT NULL,
                loser_rating REAL NOT NULL,
                winner_rating_deviation REAL NOT NULL,
                loser_rating_deviation REAL NOT NULL,
                FOREIGN KEY (rating_period_id) REFERENCES rating_period(rating_period_id),
                FOREIGN KEY (winner_id) REFERENCES players(player_id),
                FOREIGN KEY (loser_id) REFERENCES players(player_id)
            );

            CREATE TABLE players_rating_history (
                rating_period_id INTEGER NOT NULL,
                player_id INTEGER NOT NULL,
                rating REAL NOT NULL,
                rating_deviation REAL NOT NULL,
                FOREIGN KEY (rating_period_id) REFERENCES rating_period(rating_period_id),
                FOREIGN KEY (player_id) REFERENCES players(player_id)
            );
            
            CREATE INDEX idx_games ON players_rating_history(player_id, rating_period_id);
            """
        )
    ]


if __name__ == "__main__":
    main()
