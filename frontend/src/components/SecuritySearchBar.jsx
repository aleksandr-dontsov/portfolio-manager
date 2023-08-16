import { useEffect, useState } from 'react';

const SECURITY_SUGGESTIONS_NUMBER = 10;

function SecuritySuggestion({ suggestion, onSuggestionClick }) {
    return (
        <div
            onClick={ () => onSuggestionClick(suggestion) }
        >
            {suggestion.symbol} | {suggestion.exchange} | {suggestion.name}
        </div>
    );
}

export function SecuritySearchBar({ security, setSecurity, securities }) {
    const [securityText, setSecurityText] = useState(security ? security.symbol : "");
    const [suggestions, setSuggestions] = useState([]);
    const [showSuggestions, setShowSuggestions] = useState(!security);

    // Update suggestions
    useEffect(() => {
        const searchText = securityText.toLowerCase();
        if (searchText === "") {
            setSuggestions([]);
            return;
        }

        if (securities.length === 0) {
            setSuggestions([]);
            return;
        }

        const result = securities.filter((security) => {
            if (security.status === "DELISTED") {
                return false;
            }
            return security.symbol.toLowerCase().includes(searchText) ||
                   security.name.toLowerCase().includes(searchText);
        }).slice(0, SECURITY_SUGGESTIONS_NUMBER);
        setSuggestions(result);
    }, [securityText]);

    const handleSearchInputChange = (event) => {
        setSecurityText(event.target.value);
        setSecurity(null);
        setShowSuggestions(true);
    }

    const handleFocus = () => {
        setShowSuggestions(!security);
    }

    const handleBlur = () => {
        // Use a slight delay to give some time
        // to handle a click suggestion event
        setTimeout(() => {
            setShowSuggestions(false);
        }, 150)
    }

    const handleClickSuggestion = (suggestion) => {
        setSecurityText(suggestion.symbol);
        setSecurity(suggestion);
    }

    return (
        <label>
            Security:
            <input
                type="search"
                value={ securityText }
                onChange= { handleSearchInputChange }
                onFocus={ handleFocus }
                onBlur={ handleBlur }
                placeholder="AAPL / Apple Inc"
                required />
            <div>
                {showSuggestions && suggestions.map((suggestion, index) => (
                    <SecuritySuggestion
                        key={ index }
                        onSuggestionClick={ handleClickSuggestion }
                        suggestion={ suggestion } />
                ))}
            </div>
        </label>
    );
}
