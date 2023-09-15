
import { useState } from 'react';
import { useNavigate, useParams, useLocation } from 'react-router-dom';
import { useApi } from '../hooks/useApi';
import {
    SubmitButton,
} from '../components/Common';

import { TradeForm } from '../components/TradeForm';

function TradeEditForm({ trade }) {
    const { state } = useLocation();
    const updateTradeRequest = {
        method: "PUT",
        url: `/api/v1/portfolios/${trade.portfolio_id}/trades/${trade.id}`
    };

    return (
        <TradeForm
            formName="Edit"
            currency={ state.currency }
            trade={ trade }
            tradeRequest={ updateTradeRequest } />
    )
}


function TradeDeleteForm({ axios, trade }) {
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!window.confirm(`Please confirm you want to delete the trade.`)) {
            return;
        }
        try {
            await axios.request({
                method: "DELETE",
                url: `/api/v1/portfolios/${trade.portfolio_id}/trades/${trade.id}`
            });
        } catch (error) {
            setError(error);
            return;
        }
        navigate(`/portfolios/${trade.portfolio_id}`);
    }

    return (
        <div>
            <h2>Delete Trade</h2>
            <form
                method="delete"
                onSubmit={handleSubmit}
            >
                <SubmitButton name="Delete" />
            </form>
            { error && <span>{error.data.detail}</span> }
        </div>
    );
}


export default function TradeEdit() {
    const params = useParams();
    const { data: trade, error, isLoaded, axios } =
        useApi(`/api/v1/portfolios/${params.portfolioId}/trades/${params.tradeId}`, "GET");

    if (!isLoaded) {
        return (
            <span>Loading trade...</span>
        );
    }

    if (error) {
        throw error;
    }

    return (
        <div>
            <TradeEditForm
                axios={ axios }
                trade={ trade } /><br />
            <TradeDeleteForm
                axios={ axios }
                trade={ trade } />
        </div>
    );
}
