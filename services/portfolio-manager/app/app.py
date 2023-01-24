from flask import (
    Flask,
    # The glogal request object to access submitted data
    request,
    jsonify
)
from models import (
    db,
    User,
    Portfolio,
    Currency
)
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config.from_object("config.Config")
db.init_app(app)

def init_db():
    db.drop_all()
    db.create_all()

    usd = Currency(code="USD", name="United States dollar")
    eur = Currency(code="EUR", name="Euro")
    
    john = User(email="john.smith@gmail.com", password_hash="qwerty")
    bob = User(email="bob.tailor@gmail.com", password_hash="asdfg")

    for portfolio in [
        Portfolio(name="High yield", user=john, currency=usd),
        Portfolio(name="Retirement", user=bob, currency=eur)]:
        db.session.add(portfolio)

    db.session.commit()

@app.route('/portfolios', methods=['GET'])
def portfolios():
    portfolios = db.session.execute(db.select(Portfolio).order_by(Portfolio.name)).scalars()
    portfolios = [portfolio.as_dict() for portfolio in portfolios]
    return jsonify(portfolios), 200

@app.route('/portfolios/<int:id>', methods=['GET'])
def get_portfolio(id):
    portfolio = db.get_or_404(Portfolio, id)
    return jsonify(portfolio.as_dict()), 200

@app.route('/portfolios/<int:id>', methods=['GET', 'PUT'])
def update_portfolio(id):
    json = request.get_json()
    portfolio = db.get_or_404(Portfolio, id)
    portfolio.name = json["name"]
    portfolio.user_id = json["user_id"]
    portfolio.currency_id=json["currency_id"]
    db.session.add(portfolio)
    db.session.commit()
    return {'id': portfolio.id}, 200

@app.route('/portfolios/<int:id>', methods=["DELETE"])
def delete_portfolio(id):
    portfolio = db.get_or_404(Portfolio, id)
    db.session.delete(portfolio)
    db.session.commit()
    return '', 200

@app.route('/portfolios', methods=['POST'])
def add_portfolio():
    json = request.get_json()
    portfolio = Portfolio(
        name=json["name"],
        user_id=json["user_id"],
        currency_id=json["currency_id"]
    )
    db.session.add(portfolio)
    db.session.commit()
    return {'id': portfolio.id}, 200

# @app.route('/portfolios/<int:index>', methods=['PUT'])
# def update_portfolio(index):
#     portfolio = request.get_json()
#     portfolios_data[index] = portfolio
#     return jsonify(portfolios_data[index]), 200

# @app.route('/portfolios/<int:index>', methods=['DELETE'])
# def delete_portfolio(index):
#     portfolios_data.pop(index)
#     return 'None', 200

if  __name__ == '__main__':
    # Init the database
    with app.app_context():
        init_db()
        

    # 127.0.0.1 is a default value.
    # Here we need to bind our service to the 0.0.0.0 
    # to make it accessible to machines other than docker.
    # Otherwise the service will be only accessible
    # from the docker localhost
    app.run(host="0.0.0.0")