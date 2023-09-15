import { useParams, Link } from 'react-router-dom';
import { toLocalDatetime } from '../utils/utils';
import { useApi } from '../hooks/useApi';
import { CurrencyAmount } from '../components/CurrencyAmount';
import { useStream } from '../hooks/useStream';
import { getQuotesUrl } from '../api/api';

function getSecurities(trades) {
    return Array.from(new Set(trades.map(trade => trade.security.symbol)))
}

function calculatePortfolioPerformance(positions) {
    let performance = {
        buyIn: 0,
        marketValue: 0,
        totalReturn: 0,
    };

    performance = positions.reduce((performance, position) => {
        if (position.security.status === "DELISTED") {
            return performance;
        }
        performance.buyIn += position.buyIn;
        performance.marketValue += position.marketValue;
        performance.totalReturn += position.totalReturn;
        return performance;
    }, performance);

    return performance;
}

function calculatePositionsPerformance(trades, quotes) {
    // Calculate static values
    let result = trades.reduce((positions, trade) => {
        let position = positions.get(trade.security);
        if (!position) {
            position = {
                security: trade.security,
                quantity: 0,
                buyIn: 0,
                marketValue: 0,
                totalReturn: 0,
            };
        }
        position.quantity += trade.quantity;
        position.buyIn += trade.quantity * trade.unit_price;
        positions.set(trade.security, position);
        return positions;
    }, new Map());

    // Calculate dynamic values
    let positions = Array.from(result.values());
    for (let i = 0; i < positions.length; ++i) {
        const position = positions[i];
        if (!quotes.has(position.security.symbol)) {
            continue;
        }
        const marketPrice = quotes.get(position.security.symbol);
        positions[i].marketValue = position.quantity * marketPrice;
        positions[i].totalReturn = position.marketValue - position.buyIn;
    }

    return positions;
}

function TotalReturnAmount({ totalReturn, currency }) {
    let color = 'black';
    if (totalReturn > 0) {
        color = 'green';
    } else if (totalReturn < 0) {
        color = 'red';
    }
    const style = {color: color};
    return (
        <td style={style}>
            <CurrencyAmount usdAmount={totalReturn} currency={currency} />
        </td>
    );
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
                        <th>Buy in</th>
                        <th>Market Value</th>
                        <th>Total Return</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><CurrencyAmount usdAmount={performance.buyIn} currency={currency} /></td>
                        <td><CurrencyAmount usdAmount={performance.marketValue} currency={currency} /></td>
                        <TotalReturnAmount totalReturn={performance.totalReturn} currency={currency} />
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
            <td>{position.quantity}</td>
            <td><CurrencyAmount usdAmount={position.buyIn} currency={currency} /></td>
            <td><CurrencyAmount usdAmount={position.marketValue} currency={currency} /></td>
            <TotalReturnAmount totalReturn={position.totalReturn} currency={currency} />
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
                        <th>Quantity</th>
                        <th>Buy in</th>
                        <th>Market Value</th>
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

function PortfolioPerformancePanel({ portfolio }) {
    const { data } = useStream(getQuotesUrl(getSecurities(portfolio.trades)))
    let quotes = new Map()
    if (data) {
        quotes = new Map(Object.entries(JSON.parse(data)));
    }
    const positions = calculatePositionsPerformance(portfolio.trades, quotes);
    const performance = calculatePortfolioPerformance(positions);

    return (
        <>
            <Portfolio
                name={ portfolio.name }
                performance={ performance }
                currency={ portfolio.currency } />
            <Positions
                positions={ positions }
                currency={ portfolio.currency } />
        </>
    );
}

export default function PortfolioDashboard() {
    const params = useParams();
    const { data: portfolio, error, isLoaded } =
        useApi(`/api/v1/portfolios/${params.portfolioId}`, "GET");

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

    return (
        <div>
            <PortfolioPerformancePanel
                portfolio={ portfolio } />
            <Trades
                trades={ trades }
                currency={ portfolio.currency } />
        </div>
    );
}
