import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAxios } from '../hooks/useAxios';
import {
    CancelButton,
    SubmitButton,
} from './Common';
import { SecuritySearchBar } from './SecuritySearchBar'
import { AmountField } from './AmountField';
import { CurrencyAmountField } from './CurrencyAmountField';
import { DatetimeField } from './DatetimeField';
import { TradeTypeMenu } from './TradeTypeMenu';
import { useSecurity } from '../hooks/useSecurity';
import {
    toInputDatetimeLocal,
    toUtcDatetime,
    convertToUsd
} from '../utils/utils';

const USD_CURRENCY_ID = 1;

export function TradeForm({ formName, currency, trade, tradeRequest }) {
    const [error, setError] = useState(null);
    const [securities] = useSecurity();
    const [security, setSecurity] = useState(trade ? trade.security : null);
    const navigate = useNavigate();
    const axios = useAxios();

    const handleSubmit = async (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        tradeRequest.data = {
            security_id: security.id,
            currency_id: USD_CURRENCY_ID, // Always use USD as a storing currency
            trade_type: formData.get("tradeType"),
            trade_datetime: toUtcDatetime(formData.get("datetime")),
            unit_price: convertToUsd(parseFloat(formData.get("unitPrice")), currency.code),
            quantity: parseInt(formData.get("quantity")),
            brokerage_fee: convertToUsd(parseFloat(formData.get("brokerageFee")), currency.code),
        }

        try {
            await axios.request(tradeRequest);
        } catch (error) {
            setError(error);
            return;
        }
        navigate(-1);
    };

    return (
        <div>
            <h2>{formName} Trade</h2>
            <form
                method="post"
                onSubmit={handleSubmit}
            >
                <SecuritySearchBar
                    security={ security }
                    setSecurity={ setSecurity }
                    securities={ securities } /><br/>
                <DatetimeField
                    datetime={ trade && toInputDatetimeLocal(trade.trade_datetime) } /><br/>
                <TradeTypeMenu tradeType="BUY" /><br/>
                <AmountField
                    label="Quantity:"
                    name="quantity"
                    min="1"
                    max="1000000"
                    step="1"
                    placeholder="10"
                    defaultValue={ trade && trade.quantity } /><br/>
                <CurrencyAmountField
                    label="Unit Price:"
                    name="unitPrice"
                    min="0.01"
                    max="1000000"
                    currency={ currency }
                    usdAmount={ trade && trade.unit_price } /><br/>
                <CurrencyAmountField
                    label="Fee Amount:"
                    name="brokerageFee"
                    min="0"
                    max="10000"
                    currency={ currency }
                    usdAmount={ trade && trade.brokerage_fee } /><br/>
                {/* TODO: Add a dynamic total price field */}
                <SubmitButton name={formName} />
                <CancelButton />
            </form>
            { error && <span>{error.response.data.detail}</span> }
        </div>
    );
}
