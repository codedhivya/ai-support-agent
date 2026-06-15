import sys
from sqlalchemy import create_engine, text

def main():
    print("=========================================")
    print("      AWS RDS pgvector Enabler")
    print("=========================================\n")
    
    endpoint = input("Enter your RDS Endpoint/Host: ").strip()
    username = input("Enter Master Username [postgres]: ").strip() or "postgres"
    password = input("Enter Master Password: ").strip()
    dbname = input("Enter Database Name [support_agent]: ").strip() or "support_agent"
    port = input("Enter Port [5432]: ").strip() or "5432"

    if not endpoint or not password:
        print("\nError: Host and Password are required.")
        return

    # Construct connection URL
    db_url = f"postgresql://{username}:{password}@{endpoint}:{port}/{dbname}"
    
    print(f"\nConnecting to database at {endpoint}...")
    
    try:
        engine = create_engine(db_url)
        # We use AUTOCOMMIT isolation level since CREATE EXTENSION cannot run in a transaction
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            print("Connected! Enabling pgvector...")
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
            print("\n[SUCCESS] Successfully enabled pgvector extension on your database!")
            
    except Exception as e:
        print(f"\n[ERROR] Connection failed: {e}")
        print("\nCommon troubleshooting steps:")
        print("1. Wait for your RDS database status to turn green ('Available').")
        print("2. Ensure you selected 'Public accessibility = Yes' during RDS setup.")
        print("3. Ensure your RDS Security Group (ai-support-db-sg) allows incoming traffic on port 5432 from your current public IP address.")

if __name__ == "__main__":
    main()
