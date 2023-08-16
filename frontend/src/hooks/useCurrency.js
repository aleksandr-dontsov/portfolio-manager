import { useEffect } from 'react';
import { useLocalStorage } from './useLocalStorage';
import { useAxios } from './useAxios';
import { calculateTimeDiffInHours } from '../utils/utils';

const CURRENCY_UPDATE_INTERVAL_HOURS = 24 * 7;

export function useCurrency() {
    const [currencies, setCurrencies] = useLocalStorage("currencies", []);
    const axios = useAxios();

    useEffect(() => {
        const loadCurrencies = async () => {
            try {
                const response = await axios.request({
                    url: "/api/currencies",
                    method: "GET",
                });
                setCurrencies(response.data);
            } catch (error) {
                console.error(`Cannot load currencies. ${error}`);
            }
        };
        const diffInHours = calculateTimeDiffInHours(new Date(currencies.updateTimestamp), new Date());
        if (currencies.value.length === 0 || diffInHours >= CURRENCY_UPDATE_INTERVAL_HOURS) {
            loadCurrencies();
        }
    }, []);

    return currencies.value;
}
