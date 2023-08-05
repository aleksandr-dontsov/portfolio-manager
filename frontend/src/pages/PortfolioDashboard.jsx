import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { toLocalDatetime } from '../utils/utils';
import { useApi } from '../hooks/useApi';
import { CurrencyAmount } from '../components/Common';

function calculatePerformance(positions) {
    const performance = {
        marketValue: 0,
        capitalGain: 0,
        dividends: 0,
        totalReturn: 0,
    };

    performance.marketValue = positions.reduce((marketValue, position) => {
        return marketValue + position.marketValue;
    }, 0);
    return performance
}

function getPositions(trades) {
    let result = trades.reduce((positions, trade) => {
        let position = positions.get(trade.security.isin);
        if (!position) {
            position = {
                security: trade.security,
                quantity: 0,
                marketValue: 0,
            };
        }
        position.quantity += trade.quantity;
        position.marketValue += trade.quantity * trade.unit_price;
        positions.set(trade.security.isin, position);
        return positions;
    }, new Map());

    return Array.from(result.values());
}

function Portfolio({ name, performance, currencyCode }) {
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
                        <td><CurrencyAmount value={performance.marketValue} currencyCode={currencyCode} /></td>
                        <td><CurrencyAmount value={performance.capitalGain} currencyCode={currencyCode} /></td>
                        <td><CurrencyAmount value={performance.dividends} currencyCode={currencyCode} /></td>
                        <td><CurrencyAmount value={performance.totalReturn} currencyCode={currencyCode} /></td>
                    </tr>
                </tbody>
            </table>
        </div>
    )
}

function PositionRow({ position, currencyCode }) {
    // TODO: Calculate dynamic parameters
    return (
        <tr>
            <td>{`${position.security.symbol} / ${position.security.isin}`}</td>
            <td><CurrencyAmount value={position.marketValue} currencyCode={currencyCode} /></td>
            <td>{position.quantity}</td>
            <td><CurrencyAmount value={0} currencyCode={currencyCode} /></td>
            <td><CurrencyAmount value={0} currencyCode={currencyCode} /></td>
            <td><CurrencyAmount value={0} currencyCode={currencyCode} /></td>
        </tr>
    );
}

function Positions({ positions, currencyCode }) {
    const rows = positions.map((position, index) => {
        return (
            <PositionRow
                key={index}
                position={position}
                currencyCode={ currencyCode } />
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

function TradeRow({ trade, currencyCode }) {
    return (
        <tr>
            <td>{toLocalDatetime(trade.trade_datetime)}</td>
            <td>{`${trade.security.symbol} / ${trade.security.isin}`}</td>
            <td>{trade.trade_type}</td>
            <td><CurrencyAmount value={trade.unit_price} currencyCode={currencyCode} /></td>
            <td>{trade.quantity}</td>
            <td><CurrencyAmount value={trade.brokerage_fee} currencyCode={currencyCode} /></td>
            <td><CurrencyAmount value={trade.unit_price * trade.quantity} currencyCode={currencyCode} /></td>
            <td>
                <Link
                    to={`trades/${trade.id}/edit`}
                    state={{ currencyCode }}
                >
                    edit
                </Link>
            </td>
        </tr>
    );
}

function Trades({ trades, currencyCode }) {
    const rows = trades.map((trade) => {
        return (
            <TradeRow
                key={trade.id}
                trade={trade}
                currencyCode={ currencyCode } />
        );
    })
    return (
        <div>
            <h3>Trades</h3>
            <Link
                to="trades/create"
                state={{ currencyCode }}
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
                <Link to="trades/create">Add your first Trade</Link>
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
                currencyCode={ portfolio.currency.code } />
            <Positions
                positions={ positions }
                currencyCode={ portfolio.currency.code } />
            <Trades
                trades={ trades }
                currencyCode={ portfolio.currency.code } />
        </div>
    );
}
