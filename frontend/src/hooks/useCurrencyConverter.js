import { useEffect } from 'react';
import { useLocalStorage } from './useLocalStorage';
import { useAxios } from './useAxios';
import { calculateTimeDiffInHours } from '../utils/utils'

const EXCHANGE_RATE_UPDATE_INTERVAL_HOURS = 24;

export const useCurrencyConverter = () => {
    const [exchangeRates, setExchangeRates] = useLocalStorage("exchangeRates", null);
    const axios = useAxios();

    useEffect(() => {
        const loadExchangeRates = async () => {
            try {
                const response = await axios.request({
                    url: "/api/v1/exchange-rates",
                    method: "GET",
                });
                const exchangeRates = response.data.reduce((accumulator, exchangeRate) => {
                    accumulator[exchangeRate.to] = exchangeRate.rate;
                    return accumulator;
                }, {})
                setExchangeRates(exchangeRates);
            } catch (error) {
                console.error(`Cannot load currency exchange rates. ${error}`);
            }
        }

        const diffInHours = calculateTimeDiffInHours(new Date(exchangeRates.updateTimestamp), new Date());
        if (!exchangeRates.value || diffInHours >= EXCHANGE_RATE_UPDATE_INTERVAL_HOURS) {
            loadExchangeRates();
        }
    }, []);

    const convertFromUsd = (amount, currencyCode) => {
        if (!amount) {
            return amount;
        }

        if (!exchangeRates.value) {
            console.error('Exchange rates are not available');
            return null;
        }

        if (currencyCode !== "USD") {
            amount *= exchangeRates.value[currencyCode];
        }

        return amount;
    }

    const convertToUsd = (amount, currencyCode) => {
        if (!amount) {
            return amount;
        }

        if (!exchangeRates.value) {
            console.error('Exchange rates are not available');
            return null;
        }

        if (currencyCode !== "USD") {
            amount *= 1 / exchangeRates.value[currencyCode];
        }

        return amount;
    }

    return { convertFromUsd, convertToUsd }
}
