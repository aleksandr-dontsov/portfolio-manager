
import { useState } from 'react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { Currencies, SecuritySymbolToId } from '../constants/constants';
import { toUtcDatetime, convertToUsd } from '../utils/utils';
import { useAxios } from '../hooks/useAxios';
import {
    AmountField,
    CancelButton,
    CurrencyAmountField,
    DatetimeField,
    TradeTypeMenu,
    SecuritySearchField,
    SubmitButton,
} from '../components/Common';


export default function TradeCreate() {
    const params = useParams();
    const navigate = useNavigate();
    const { state } = useLocation();
    const [error, setError] = useState(null);
    const [security, setSecurity] = useState("");
    const axios = useAxios();

    const handleSubmit = async (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        try {
            await axios.request({
                method: "POST",
                data: {
                    security_id: SecuritySymbolToId.get(security),
                    currency_id: Currencies["USD"].id, // always usd
                    trade_type: formData.get("tradeType"),
                    trade_datetime: toUtcDatetime(formData.get("datetime")),
                    unit_price: convertToUsd(parseFloat(formData.get("unitPrice")), state.currencyCode),
                    quantity: parseInt(formData.get("quantity")),
                    brokerage_fee: convertToUsd(parseFloat(formData.get("brokerageFee")), state.currencyCode),
                },
                url: `/api/portfolios/${params.portfolioId}/trades`
            });
        } catch (error) {
            setError(error);
            return;
        }
        navigate(`/portfolios/${params.portfolioId}`);
    }

    return (
        <div>
            <h2>Create Trade</h2>
            <form
                method="post"
                onSubmit={handleSubmit}
            >
                <SecuritySearchField
                    securityText={ security }
                    onSecurityTextChange={ setSecurity } /><br/>
                <DatetimeField /><br/>
                <TradeTypeMenu selectedTradeType="BUY" /><br/>
                <AmountField
                    label="Quantity:"
                    name="quantity"
                    min="1"
                    step="1"
                    placeholder="10" /><br/>
                <CurrencyAmountField
                    label="Unit Price:"
                    name="unitPrice"
                    min="0.01"
                    currencyCode={ state.currencyCode } /><br/>
                <CurrencyAmountField
                    label="Fee Amount:"
                    name="brokerageFee"
                    min="0"
                    currencyCode={ state.currencyCode } /><br/>
                {/* TODO: Add a dynamic total price field */}
                <SubmitButton name="Create" />
                <CancelButton />
            </form>
            { error && <span>{error.data.detail}</span> }
        </div>
    );
}
