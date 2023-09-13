import { useEffect, useState } from 'react';
import { useAxios } from '../hooks/useAxios';
import { useDebounce } from '../hooks/useDebounce';

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

export function SecuritySearchBar({ security, setSecurity }) {
    const [securityText, setSecurityText] = useState(security ? security.symbol : "");
    const [suggestions, setSuggestions] = useState([]);
    const [showSuggestions, setShowSuggestions] = useState(!security);
    const axios = useAxios();

    // Update suggestions
    useDebounce(() => {
        const searchText = securityText.toLowerCase();
        if (searchText === "") {
            setSuggestions([]);
            return;
        }

        const searchSecurities = async () => {
            try {
                const response = await axios.request({
                    url: "/api/securities/search",
                    method: "GET",
                    params: {
                        query: securityText
                    }
                })
                setSuggestions(response.data.slice(0, SECURITY_SUGGESTIONS_NUMBER))
            } catch (error) {
                console.error(`Unable to search for securities. ${error}`);
                setSuggestions([]);
            }
        }

        searchSecurities();
    }, 1000);

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
