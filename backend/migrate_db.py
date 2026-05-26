from app.db.session import engine
from sqlalchemy import text

def run_migrations():
    with engine.connect() as conn:
        # Phase 2: Add telegram_chat_id to users
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN telegram_chat_id VARCHAR;"))
            print("Added telegram_chat_id to users")
        except Exception as e:
            print("Skipped users (probably exists)")
            
        # Phase 3: Create collections table
        try:
            conn.execute(text("""
            CREATE TABLE collections (
                id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL,
                user_email VARCHAR NOT NULL
            );
            """))
            print("Created collections table")
        except Exception as e:
            print("Skipped collections (probably exists)")
            
        # Phase 3: Add collection_id to products
        try:
            conn.execute(text("ALTER TABLE products ADD COLUMN collection_id INTEGER REFERENCES collections(id) ON DELETE SET NULL;"))
            print("Added collection_id to products")
        except Exception as e:
            print("Skipped products.collection_id (probably exists)")
            
        conn.commit()

if __name__ == "__main__":
    run_migrations()
