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

export function calculateTimeDiffInHours(from, to) {
    return (to - from) / (1000 * 60 * 60);
}
