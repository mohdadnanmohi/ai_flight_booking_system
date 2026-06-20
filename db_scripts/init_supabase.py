# Script to initialize Supabase Database with schema.sql and seeds.sql
import os
import psycopg2
from dotenv import load_dotenv

# Load env variables
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(basedir, '.env'))

db_url = os.getenv('DATABASE_URL')
print(f"Connecting to database: {db_url.split('@')[-1]}")

try:
    # Connect to Supabase PostgreSQL
    conn = psycopg2.connect(db_url)
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Read and execute schema.sql
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    print("Executing schema.sql...")
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
        cursor.execute(schema_sql)
    print("Schema executed successfully.")

    # Read and execute seeds.sql
    seeds_path = os.path.join(os.path.dirname(__file__), 'seeds.sql')
    print("Executing seeds.sql...")
    with open(seeds_path, 'r') as f:
        seeds_sql = f.read()
        cursor.execute(seeds_sql)
    print("Seed records executed successfully.")
    
    cursor.close()
    conn.close()
    print("\nDatabase initialization complete! All tables, indexes, and seed records have been created in your Supabase project.")

except Exception as e:
    print(f"\nError initializing database: {e}")
