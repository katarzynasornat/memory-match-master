import argparse
from .database import init_db

def main():
    parser = argparse.ArgumentParser(description="Initialize the database.")
    parser.add_argument("--seed", action="store_true", help="Seed the database with mock data.")
    args = parser.parse_args()

    # The init_db function already seeds if the database is empty.
    # We can force it or just call it.
    print(f"Initializing database (Seed: {args.seed})...")
    init_db()
    print("Database initialized successfully.")

if __name__ == "__main__":
    main()
