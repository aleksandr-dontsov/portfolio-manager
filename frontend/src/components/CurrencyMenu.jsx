import { useEffect } from 'react';
import { useLocalStorage } from '../hooks/useLocalStorage';
import { useAxios } from '../hooks/useAxios';
import { calculateTimeDiffInHours } from '../utils/utils';

const CURRENCY_UPDATE_INTERVAL_HOURS = 24 * 7;

export function CurrencyMenu({ currency, setCurrency }) {
    const [currencies, setCurrencies] = useLocalStorage("currencies", null);
    const axios = useAxios();

    useEffect(() => {
        const loadCurrencies = async () => {
            try {
                const response = await axios.request({
                    url: "/api/v1/currencies",
                    method: "GET",
                });
                setCurrencies(response.data);
            } catch (error) {
                console.error(`Cannot load currencies. ${error}`);
            }
        };
        const diffInHours = calculateTimeDiffInHours(new Date(currencies.updateTimestamp), new Date());
        if (!currencies.value || diffInHours >= CURRENCY_UPDATE_INTERVAL_HOURS) {
            loadCurrencies();
        }
    }, []);

    // Update selected currency
    const handleSelectChange = (event) => {
        const result = currencies.value.filter((currency) => {
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
                {currencies.value.map((currency, index) => (
                    <option key={index} value={currency.code}>
                        {currency.code}
                    </option>
                ))}
            </select>
        </label>
    );
}
