import { useCurrencyConverter } from "../hooks/useCurrencyConverter";

export function CurrencyAmount({ usdAmount, currency }) {
    const { convertFromUsd } = useCurrencyConverter()
    const amount = convertFromUsd(usdAmount, currency.code);
    return (
        <span>{ amount && amount.toFixed(2) }{ currency.symbol }</span>
    );
}
