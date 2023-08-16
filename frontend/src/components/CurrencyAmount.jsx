import { convertFromUsd } from "../utils/utils";

export function CurrencyAmount({ usdAmount, currency }) {
    const amount = convertFromUsd(usdAmount, currency.code);
    return (
        <span>{ amount && amount.toFixed(2) }{ currency.symbol }</span>
    );
}
