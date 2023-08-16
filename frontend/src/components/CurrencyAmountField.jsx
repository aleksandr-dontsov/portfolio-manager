import { AmountField } from "./AmountField";
import { convertFromUsd } from "../utils/utils";

export function CurrencyAmountField({ label, name, min, max, usdAmount, currency }) {
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
