
import { Link } from 'react-router-dom';
import { toLocalDate } from '../utils/utils';
import { useApi } from '../hooks/useApi';

function countPositions(trades) {
    return [...new Set(trades.map(trade => trade.security.symbol))].length;
}

function PortfolioRow({ index, portfolio }) {
    return (
        <tr>
            <td>{index}</td>
            <td><Link to={`${portfolio.id}`}>{portfolio.name}</Link></td>
            <td>{countPositions(portfolio.trades)}</td>
            <td>{portfolio.currency.code}</td>
            <td>{toLocalDate(portfolio.created_at)}</td>
            <td>
                <Link to={`${portfolio.id}/edit`}>edit</Link>
            </td>
        </tr>
    )
}

export default function Portfolios() {
    const { data: portfolios, error, isLoaded } = useApi("/api/portfolios", "GET");

    if (!isLoaded) {
        return (
            <span>Loading portfolios...</span>
        );
    }

    if (error) {
        throw error;
    }

    if (!portfolios.length) {
        return (
            <Link to="create">Add your first Portfolio</Link>
        );
    }

    const rows = portfolios.map((portfolio, index) => {
        return (
            <PortfolioRow
                key={portfolio.id}
                index={index + 1}
                portfolio={portfolio} />
        );
    });

    return (
        <>
            <div>
                <h2>Portfolios</h2>
                <Link to="create">Add a Portfolio</Link>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Name</th>
                        <th>Positions</th>
                        <th>Currency</th>
                        <th>Created date</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
        </>
    );
}
