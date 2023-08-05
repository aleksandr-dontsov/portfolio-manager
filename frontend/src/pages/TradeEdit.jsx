
import { useState } from 'react';
import { useNavigate, useParams, useLocation } from 'react-router-dom';
import { useApi } from '../hooks/useApi';
import {
    toInputDatetimeLocal,
    toUtcDatetime,
    convertToUsd
} from '../utils/utils';
import { Currencies, SecuritySymbolToId } from '../constants/constants';
import {
    AmountField,
    CancelButton,
    CurrencyAmountField,
    DatetimeField,
    TradeTypeMenu,
    SecuritySearchField,
    SubmitButton,
} from '../components/Common';

function TradeEditForm({ axios, trade }) {
    const [error, setError] = useState(null);
    const [security, setSecurity] = useState(trade.security.symbol);
    const navigate = useNavigate();
    const { state } = useLocation();

    const handleSubmit = async (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        try {
            await axios.request({
                method: "PUT",
                data: {
                    security_id: SecuritySymbolToId.get(security),
                    currency_id: Currencies["USD"].id, // always usd
                    trade_type: formData.get("tradeType"),
                    trade_datetime: toUtcDatetime(formData.get("datetime")),
                    unit_price: convertToUsd(parseFloat(formData.get("unitPrice")), state.currencyCode),
                    quantity: parseInt(formData.get("quantity")),
                    brokerage_fee: convertToUsd(parseFloat(formData.get("brokerageFee")), state.currencyCode),
                },
                url: `/api/portfolios/${trade.portfolio_id}/trades/${trade.id}`
            });
        } catch (error) {
            setError(error);
            return;
        }
        navigate(`/portfolios/${trade.portfolio_id}`);
    }

    return (
        <div>
            <h2>Edit Trade</h2>
            <form
                method="post"
                onSubmit={handleSubmit}
            >
                <SecuritySearchField
                    securityText={ security }
                    onSecurityTextChange={ setSecurity } /><br/>
                <DatetimeField
                    defaultValue={ toInputDatetimeLocal(trade.trade_datetime) } /><br/>
                <TradeTypeMenu selectedTradeType="BUY" /><br/>
                <AmountField
                    label="Quantity:"
                    name="quantity"
                    min="1"
                    step="1"
                    defaultValue={ trade.quantity } /><br/>
                <CurrencyAmountField
                    label="Unit Price:"
                    name="unitPrice"
                    min="0.01"
                    currencyCode={ state.currencyCode }
                    defaultValue={ trade.unit_price } /><br/>
                <CurrencyAmountField
                    label="Fee Amount:"
                    name="brokerageFee"
                    min="0"
                    currencyCode={ state.currencyCode }
                    defaultValue={ trade.brokerage_fee } /><br/>
                {/* TODO: Add a dynamic total price field */}
                <SubmitButton name="Save" />
                <CancelButton />
            </form>
            { error && <span>{error.data.detail}</span> }
        </div>
    );
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
                url: `/api/portfolios/${trade.portfolio_id}/trades/${trade.id}`
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
        useApi(`/api/portfolios/${params.portfolioId}/trades/${params.tradeId}`, "GET");

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
