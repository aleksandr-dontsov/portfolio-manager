const TRADE_TYPES = ["BUY", "SELL"];

export function TradeTypeMenu({ selectedTradeType }) {
    return (
        <label>
            Trade Type:
            <select
                name="tradeType"
                defaultValue={selectedTradeType}
                required
            >
                {TRADE_TYPES.map((type, index) => {
                    return <option key={index} value={type}>{type}</option>
                })}
            </select>
        </label>
    );
}
