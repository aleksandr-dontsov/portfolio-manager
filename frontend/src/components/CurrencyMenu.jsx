import React from 'react';

export function CurrencyMenu({ currency, setCurrency, currencies }) {
    // Update selected currency
    const handleSelectChange = (event) => {
        const result = currencies.filter((currency) => {
            return currency.code === event.target.value;
        });
        console.assert(result.length === 1, "Currencies must be unique");
        setCurrency(result[0]);
    }

    return (
        <label>
            Currency:
            <select
                name="currency"
                defaultValue={ currency ? currency.code : "" }
                onChange={ handleSelectChange }
                required
            >
                {currencies.map((currency, index) => (
                    <option key={index} value={currency.code}>
                        {currency.code}
                    </option>
                ))}
            </select>
        </label>
    );
}
