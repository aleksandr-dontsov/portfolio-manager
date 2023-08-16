import { useLocation, useParams } from 'react-router-dom';
import { TradeForm } from '../components/TradeForm';

export default function TradeCreate() {
    const { state } = useLocation();
    const params = useParams();
    const createTradeRequest = {
        method: "POST",
        url: `/api/portfolios/${params.portfolioId}/trades`
    };

    return (
        <TradeForm
            formName="Create"
            currency={ state.currency }
            tradeRequest={ createTradeRequest } />
    )
}
