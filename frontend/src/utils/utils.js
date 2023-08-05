import { DateTime } from 'luxon';

export function toLocalDate(utcDatetime) {
    return DateTime.fromISO(utcDatetime).toISODate();
}

export function toUtcDatetime(localDatetime) {
    return DateTime.fromISO(localDatetime).toUTC().toString();
}

export function toLocalDatetime(utcDatetime) {
    return DateTime.fromISO(utcDatetime).setLocale('en-gb').toLocaleString();
}

export function toLocalIsoDatetime(utcDatetime) {
    return DateTime.fromISO(utcDatetime).to().toString();
}

// Converts UTC datetime to HTML input type datetime-local
export function toInputDatetimeLocal(utcDatetime) {
    return DateTime.fromISO(utcDatetime).toLocal().toISO({ includeOffset: false });
}

const UsdToCurrencyExchangeRates = {
    EUR: 0.91,
    RUB: 94.50,
}

// Converts an amount in USD to a given currency
export function convertFromUsd(amount, currencyCode) {
    if (currencyCode === "USD") {
        return amount;
    }

    return amount * UsdToCurrencyExchangeRates[currencyCode];
}

export function convertToUsd(amount, currencyCode) {
    if (currencyCode === "USD") {
        return amount;
    }

    return amount * (1 / UsdToCurrencyExchangeRates[currencyCode]);
}
