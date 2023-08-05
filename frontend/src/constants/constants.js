export const Currencies = {
    USD: {id: 1, symbol: '$' },
    EUR: {id: 2, symbol: '€' },
    RUB: {id: 3, symbol: '₽' },
};

export const TradeTypes = ["BUY", "SELL"];

export const Securities = {
    IBM: 1,
    TSLA: 2,
    AAPL: 3,
};

export const SecuritySymbolToId = new Map(Object.entries(Securities));
export const SecurityIdToSymbol = new Map(Object.entries(Securities).map(([k, v]) => [v, k]));
