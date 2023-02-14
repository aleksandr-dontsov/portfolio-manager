from config import db
from models import Trade, trades_schema

def read_all(portfolio_id):
    trades = db.session.execute(
        db.select(Trade).where(Trade.portfolio_id == portfolio_id)).scalars()
    return trades_schema.dump(trades)

