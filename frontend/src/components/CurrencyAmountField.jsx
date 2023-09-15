import { AmountField } from "./AmountField";
import { useCurrencyConverter } from "../hooks/useCurrencyConverter";

export function CurrencyAmountField({ label, name, min, max, usdAmount, currency }) {
    const { convertFromUsd } = useCurrencyConverter()
    const amount = convertFromUsd(usdAmount, currency.code);
    return (
        <div>
            <AmountField
                label={ label }
                name={ name }
                min={ min }
                max={ max }
                step="0.01"
                defaultValue={ amount && amount.toFixed(2) } />
            <span>{currency.code}</span>
        </div>
    );
}
