from flask import (
    Flask,
    jsonify,
    # The glogal request object to access submitted data
    request
)
from db import (
    init_db,
    get_db_connection
)

app = Flask(__name__)

@app.route('/portfolios', methods=['GET'])
def portfolios():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM portfolio;')
            portfolios = cursor.fetchall()
    return jsonify(portfolios), 200


@app.route('/portfolios', methods=['POST'])
def add_portfolio():
    portfolio = request.get_json()
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            # Insert a portfolio
            cursor.execute('INSERT INTO portfolio (portfolio_name, user_id, currency_id)'
                                'VALUES(%s, %s, %s) RETURNING portfolio_id',
                           (portfolio['portfolio_name'],
                            portfolio['user_id'],
                            portfolio['currency_id']))
            connection.commit()
            id = cursor.fetchone()[0]

    return {'id': id}, 200

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
    init_db()

    # 127.0.0.1 is a default value.
    # Here we need to bind our service to the 0.0.0.0 
    # to make it accessible to machines other than docker.
    # Otherwise the service will be only accessible
    # from the docker localhost
    app.run(host="0.0.0.0")