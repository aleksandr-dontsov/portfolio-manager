
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    CurrencyMenu,
    TextField,
    SubmitButton,
    CancelButton
} from '../components/Common';
import { useAxios } from '../hooks/useAxios';
import { Currencies } from '../constants/constants';

export default function PortfolioCreate() {
    // useNavigate returns a function that lets you navigate programatically
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    const axios = useAxios();

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
                    currency_id: Currencies[formData.get("currency")].id,
                },
                url: "/api/portfolios"
            });
        } catch (error) {
            setError(error);
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
                <TextField placeholder="Your portfolios name" /><br />
                <CurrencyMenu selectedCurrency="USD" /><br />
                <SubmitButton name="Create"/>
                <CancelButton />
            </form>
            { error && <span>{error.data.detail}</span> }
        </div>
    );
}
