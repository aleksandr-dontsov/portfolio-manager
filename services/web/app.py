from crypt import methods
from flask import Flask, jsonify, request

import datetime

app = Flask(__name__)

portfolios_data = [
    {
        "potfolio_id": 0,
        "portfolio_name": "Tech conpanies",
        "user_id": 0,
        "currency_id": 0,
        "created_date": datetime.datetime.now().date()
    },
    {
        "potfolio_id": 1,
        "portfolio_name": "ETFs",
        "user_id": 0,
        "currency_id": 0,
        "created_date": datetime.datetime.now().date()
    },
]

# Portfolio
# ################
# portfolio_id
# portfolio_name
# user_id
# currency_id
# created_date

# Currency table
# ################
# currency_code
# currency_name

@app.route('/portfolios', methods=['GET'])
def portfolios():
    return jsonify(portfolios_data)

@app.route('/portfolios', methods=['POST'])
def add_portfolio():
    portfolio = request.get_json()
    portfolios_data.append(portfolio)
    return {'id': len(portfolios_data)}, 200

@app.route('/portfolios/<int:index>', methods=['PUT'])
def update_portfolio(index: int):
    portfolio = request.get_json()
    portfolios_data[index] = portfolio
    return jsonify(portfolios_data[index]), 200

@app.route('/portfolios/<int:index>', methods=['DELETE'])
def delete_portfolio(index: int):
    portfolios_data.pop(index)
    return 'None', 200

app.run()