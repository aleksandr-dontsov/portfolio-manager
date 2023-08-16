import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { toLocalDatetime } from '../utils/utils';
import { useApi } from '../hooks/useApi';
import { CurrencyAmount } from '../components/CurrencyAmount';

function calculatePerformance(positions) {
    const performance = {
        marketValue: 0,
        capitalGain: 0,
        dividends: 0,
        totalReturn: 0,
    };

    performance.marketValue = positions.reduce((marketValue, position) => {
        if (position.security.status === "DELISTED") {
            return marketValue;
        }
        return marketValue + position.marketValue;
    }, 0);
    return performance
}

function getPositions(trades) {
    let result = trades.reduce((positions, trade) => {
        let position = positions.get(trade.security.symbol);
        if (!position) {
            position = {
                security: trade.security,
                quantity: 0,
                marketValue: 0,
            };
        }
        position.quantity += trade.quantity;
        position.marketValue += trade.quantity * trade.unit_price;
        positions.set(trade.security.symbol, position);
        return positions;
    }, new Map());

    return Array.from(result.values());
}

function Portfolio({ name, performance, currency }) {
    return (
        <div>
            <div>
                <h3>Portfolio: {name}</h3>
                <Link to="edit">Settings</Link>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Market Value</th>
                        <th>Capital Gain</th>
                        <th>Dividends</th>
                        <th>Total Return</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><CurrencyAmount usdAmount={performance.marketValue} currency={currency} /></td>
                        <td><CurrencyAmount usdAmount={performance.capitalGain} currency={currency} /></td>
                        <td><CurrencyAmount usdAmount={performance.dividends} currency={currency} /></td>
                        <td><CurrencyAmount usdAmount={performance.totalReturn} currency={currency} /></td>
                    </tr>
                </tbody>
            </table>
        </div>
    )
}

function PositionRow({ position, currency }) {
    // TODO: Calculate dynamic parameters
    const isDelisted = position.security.status === "DELISTED"
    const style = isDelisted ? {color: 'gray'} : {color: 'black'};
    return (
        <tr style={style}>
            <td>{`${position.security.symbol} | ${position.security.name}`} {isDelisted && <span style={{color: 'red'}}>[DELISTED]</span>}</td>
            <td><CurrencyAmount usdAmount={position.marketValue} currency={currency} /></td>
            <td>{position.quantity}</td>
            <td><CurrencyAmount usdAmount={0} currency={currency} /></td>
            <td><CurrencyAmount usdAmount={0} currency={currency} /></td>
            <td><CurrencyAmount usdAmount={0} currency={currency} /></td>
        </tr>
    );
}

function Positions({ positions, currency }) {
    const rows = positions.map((position, index) => {
        return (
            <PositionRow
                key={index}
                position={position}
                currency={ currency } />
        );
    });
    // calculate values
    return (
        <div>
            <h3>Positions</h3>
            <table>
                <thead>
                    <tr>
                        <th>Security</th>
                        <th>Market Value</th>
                        <th>Quantity</th>
                        <th>Capital Gain</th>
                        <th>Dividends</th>
                        <th>Total Return</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
    );
}

function TradeRow({ trade, currency }) {
    const isDelisted = trade.security.status === "DELISTED"
    const style = isDelisted ? {color: 'gray'} : {color: 'black'};
    return (
        <tr style={style}>
            <td>{toLocalDatetime(trade.trade_datetime)}</td>
            <td>{`${trade.security.symbol} | ${trade.security.name}`} {isDelisted && <span style={{color: 'red'}}>[DELISTED]</span>}</td>
            <td>{trade.trade_type}</td>
            <td><CurrencyAmount usdAmount={trade.unit_price} currency={currency} /></td>
            <td>{trade.quantity}</td>
            <td><CurrencyAmount usdAmount={trade.brokerage_fee} currency={currency} /></td>
            <td><CurrencyAmount usdAmount={trade.unit_price * trade.quantity} currency={currency} /></td>
            <td>
                <Link
                    to={`trades/${trade.id}/edit`}
                    state={{ currency }}
                >
                    edit
                </Link>
            </td>
        </tr>
    );
}

function Trades({ trades, currency }) {
    const rows = trades.map((trade) => {
        return (
            <TradeRow
                key={trade.id}
                trade={trade}
                currency={ currency } />
        );
    })
    return (
        <div>
            <h3>Trades</h3>
            <Link
                to="trades/create"
                state={{ currency }}
            >
                Add Trades
            </Link>
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Security</th>
                        <th>Type</th>
                        <th>Price</th>
                        <th>Quantity</th>
                        <th>Brokerage fee</th>
                        <th>Value</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
    );
}

export default function PortfolioDashboard() {
    const params = useParams();

    const { data: portfolio, error, isLoaded } =
        useApi(`/api/portfolios/${params.portfolioId}`, "GET");

    if (!isLoaded) {
        return (
            <span>Loading portfolios...</span>
        );
    }

    if (error) {
        throw error;
    }

    const trades = portfolio.trades;
    if (!trades.length) {
        return (
            <div>
                <p>{`Portfolio '${portfolio.name}' doesn't have any trades yet.`} </p>
                <Link
                    to="trades/create"
                    state={{ currency: portfolio.currency }}
                >
                    Add your first Trade
                </Link>
            </div>
        );
    }
    const positions = getPositions(trades);
    const performance = calculatePerformance(positions);
    return (
        <div>
            <Portfolio
                name={ portfolio.name }
                performance={ performance }
                currency={ portfolio.currency } />
            <Positions
                positions={ positions }
                currency={ portfolio.currency } />
            <Trades
                trades={ trades }
                currency={ portfolio.currency } />
        </div>
    );
}
