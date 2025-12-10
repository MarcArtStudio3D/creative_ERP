import sys

from sqlalchemy import inspect, text

from core.db import get_engine_from_url

# Add project root to path
sys.path.append("/home/marc/Documents/Artstudio3D/Creative_ERP")


def inspect_db():
    db_url = "mysql+pymysql://admin:admin123@127.0.0.1:3306/creative_erp_main"
    print(f"Connecting to {db_url}...")

    try:
        engine = get_engine_from_url(db_url)
        inspector = inspect(engine)

        # Check if table exists
        tables = inspector.get_table_names()
        print(f"Tables in DB: {tables}")

        if "empresas" in tables:
            print("\nColumns in 'empresas' table:")
            columns = inspector.get_columns("empresas")
            for col in columns:
                print(f"  - {col['name']} ({col['type']})")

            # Query data
            print("\nData in 'empresas' table (first 3 rows):")
            with engine.connect() as conn:
                result = conn.execute(text("SELECT * FROM empresas LIMIT 3"))
                rows = result.fetchall()
                if not rows:
                    print("  No rows found.")
                else:
                    for row in rows:
                        print(f"  - {row}")
        else:
            print("\nTable 'empresas' NOT found!")
            # Check for case sensitivity issues
            for t in tables:
                if t.lower() == "empresas":
                    print(f"  Found similar table: '{t}'")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    inspect_db()
