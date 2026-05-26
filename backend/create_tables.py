from app.db.base import Base
from app.db.session import engine
import app.models.product
import app.models.price_history
import app.models.event
import app.models.user
import app.models.collection

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done!")
