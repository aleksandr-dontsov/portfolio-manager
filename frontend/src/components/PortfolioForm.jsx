import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAxios } from '../hooks/useAxios';
import { TextField, SubmitButton, CancelButton } from './Common';
import { CurrencyMenu } from './CurrencyMenu';

export function PortfolioForm({ formName, portfolio, portfolioRequest }) {
    const [error, setError] = useState(null);
    const [currency, setCurrency] = useState(portfolio ? portfolio.currency : null);
    const navigate = useNavigate();
    const axios = useAxios();

    const handleSubmit = async (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        portfolioRequest.data = {
            name: formData.get("name"),
            currency_id: currency.id,
        }
        try {
            await axios.request(portfolioRequest);
        } catch (error) {
            setError(error);
            return;
        }
        navigate(-1);
    };

    return (
        <div>
            <h2>{formName} Portfolio</h2>
            <form
                method="post"
                onSubmit={handleSubmit}
            >
                <TextField
                    text={ portfolio && portfolio.name }
                    placeholder="Portfolio name" /><br />
                <CurrencyMenu
                    currency={ currency }
                    setCurrency={ setCurrency } /><br />
                <SubmitButton name={ formName }/>
                <CancelButton />
            </form>
            { error && <span>{error}</span> }
        </div>
    );
}
