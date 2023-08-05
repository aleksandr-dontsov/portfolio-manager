import { useNavigate } from 'react-router-dom';
import { DateTime } from 'luxon';
import { Currencies, TradeTypes } from '../constants/constants';
import { toInputDatetimeLocal, convertFromUsd } from '../utils/utils';

export function EmailField({ email, onEmailChange }) {
    return (
        <label>
            Email:
            <input
                type="email"
                name="email"
                value={ email }
                onChange={event => onEmailChange(event.target.value)}
                required>
            </input>
        </label>
    );
}

export function PasswordField({ label, password, onPasswordChange }) {
    return (
        <label>
            {label}
            <input
                type="password"
                autoComplete="password"
                value={ password }
                onChange={ event => onPasswordChange(event.target.value) }
                required>
            </input>
        </label>
    );
}

export function TextField({ text, placeholder }) {
    return (
        <label>
            Name:
            <input
                type="plain"
                name="name"
                defaultValue={ text }
                placeholder={ placeholder }
                maxLength="150"
                required />
        </label>
    );
}

export function SecuritySearchField({ securityText, onSecurityTextChange }) {
    return (
        <label>
            Security:
            <input
                type="search"
                value={ securityText }
                onChange= { (e) => onSecurityTextChange(e.target.value) }
                placeholder="AAPL"
                required />
        </label>
    );
}

export function CurrencyAmount({ value, currencyCode }) {
    return (
        <span>{convertFromUsd(value, currencyCode).toFixed(2)}{Currencies[currencyCode].symbol}</span>
    );
}

export function AmountField({ label, name, min, placeholder, step, defaultValue }) {
    return (
        <label>
            {label}
            <input
                type="number"
                name={ name }
                min={ min }
                placeholder={ placeholder }
                step={ step }
                defaultValue={ defaultValue }
                required />
        </label>
    );
}

export function CurrencyAmountField({ label, name, min, defaultValue, currencyCode }) {
    return (
        <div>
            <AmountField
                label={ label }
                name={ name }
                min={ min }
                placeholder="1.23"
                step="0.01"
                defaultValue={ convertFromUsd(defaultValue, currencyCode).toFixed(2) } />
            <span>{Currencies[currencyCode].symbol}</span>
        </div>
    );
}

export function DatetimeField({ defaultValue }) {
    return (
        <label>
            Date and time:
            <input
                type="datetime-local"
                name="datetime"
                defaultValue={ defaultValue }
                max={toInputDatetimeLocal(DateTime.now())}
                required />
        </label>
    );
}


export function CurrencyMenu({ selectedCurrency }) {
    const options = Object.entries(Currencies).map(([code,], index) => {
        return <option key={index} value={code}>{code}</option>
    });

    return (
        <label>
            Currency:
            <select
                name="currency"
                defaultValue={selectedCurrency}
                required
            >
                { options }
            </select>
        </label>
    );
}

export function TradeTypeMenu({ selectedTradeType }) {
    const options = TradeTypes.map((type, index) => {
        return <option key={index} value={type}>{type}</option>
    });

    return (
        <label>
            Trade Type:
            <select
                name="tradeType"
                defaultValue={selectedTradeType}
                required
            >
                { options }
            </select>
        </label>
    );
}

export function SubmitButton({ name }) {
    return (
        <button type="submit">{name}</button>
    );
}

export function CancelButton() {
    const navigate = useNavigate();
    const onClick = () => {
        navigate(-1);
    }
    return (
        <button type="button" onClick={onClick}>Cancel</button>
    );
}
