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
    const [query, setQuery] = useState(security ? security.symbol : "");
    const [suggestions, setSuggestions] = useState([]);
    const [showSuggestions, setShowSuggestions] = useState(!security);
    const axios = useAxios();

    // Update suggestions
    useDebounce(() => {
        if (query === "") {
            setSuggestions([]);
            return;
        }

        const searchSecurities = async () => {
            try {
                const response = await axios.request({
                    url: "/api/v1/securities",
                    method: "GET",
                    params: {
                        query: query.toLowerCase()
                    }
                })
                setSuggestions(response.data.slice(0, SECURITY_SUGGESTIONS_NUMBER))
            } catch (error) {
                console.error(`Unable to search for securities. ${error}`);
                setSuggestions([]);
            }
        }

        searchSecurities();
    }, 250, query);

    const handleSearchInputChange = (event) => {
        setQuery(event.target.value);
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
        setQuery(suggestion.symbol);
        setSecurity(suggestion);
    }

    return (
        <label>
            Security:
            <input
                type="search"
                value={ query }
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
