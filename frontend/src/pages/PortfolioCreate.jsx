
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    TextField,
    SubmitButton,
    CancelButton
} from '../components/Common';
import { CurrencyMenu } from '../components/CurrencyMenu';
import { useAxios } from '../hooks/useAxios';
import { useCurrency } from '../hooks/useCurrency';

export default function PortfolioCreate() {
    // useNavigate returns a function that lets you navigate programatically
    const [error, setError] = useState(null);
    const [currency, setCurrency] = useState(null);
    const currencies = useCurrency();
    const navigate = useNavigate();
    const axios = useAxios();

    // Setup a default currency
    if (!currency && currencies.length > 0) {
        setCurrency(currencies[0]);
    }

    const handleSubmit = async (event) => {
        // Prevents the default action that the browser takes
        // when an event occurs
        event.preventDefault();
        const formData = new FormData(event.target);

        try {
            await axios.request({
                method: "POST",
                data: {
                    name: formData.get("name"),
                    currency_id: currency.id,
                },
                url: "/api/portfolios"
            });
        } catch (error) {
            setError(error.response.data.detail);
            return;
        }
        navigate("/portfolios");
    }

    // Extract a message from the error response
    return (
        <div>
            <h2>Create Portfolio</h2>
            <form
                method="post"
                onSubmit={handleSubmit}
            >
                <TextField placeholder="Portfolio name" /><br />
                <CurrencyMenu
                    currency={ currency }
                    setCurrency={ setCurrency }
                    currencies={ currencies } /><br />
                <SubmitButton name="Create"/>
                <CancelButton />
            </form>
            { error && <span>{error}</span> }
        </div>
    );
}
