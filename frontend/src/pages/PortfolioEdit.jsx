import { useState } from 'react';
import {
    useNavigate,
    useParams,
} from 'react-router-dom';
import { useApi } from '../hooks/useApi';
import {
    CurrencyMenu,
    TextField,
    SubmitButton,
    CancelButton
} from '../components/Common';
import { Currencies } from '../constants/constants';

function PortfolioEditForm({ axios, portfolio }) {
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        try {
            await axios.request({
                method: "PUT",
                data: {
                    name: formData.get("name"),
                    currency_id: Currencies[formData.get("currency")].id,
                },
                url: `/api/portfolios/${portfolio.id}`
            });
        } catch (error) {
            setError(error);
            return;
        }
        navigate(-1);
    }

    return (
        <div>
            <h2>Edit Portfolio</h2>
            <form
                method="put"
                onSubmit={handleSubmit}
            >
                <TextField text={ portfolio.name } /><br />
                <CurrencyMenu selectedCurrency={ portfolio.currency.code } /><br />
                <SubmitButton name="Save" />
                <CancelButton />
            </form>
            { error && <span>{error.data.detail}</span> }
        </div>
    );
}

function PortfolioDeleteForm({ axios, portfolio }) {
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!window.confirm(`Please confirm you want to delete '${portfolio.name}' portfolio.`)) {
            return;
        }
        try {
            await axios.request({
                method: "DELETE",
                url: `/api/portfolios/${portfolio.id}`
            });
        } catch (error) {
            setError(error);
            return;
        }
        navigate("/portfolios");
    }

    return (
        <div>
            <h2>Delete Portfolio</h2>
            <form
                method="delete"
                onSubmit={handleSubmit}
            >
                <SubmitButton name="Delete" />
            </form>
            { error && <span>{error.data.detail}</span> }
        </div>
    );
}

export default function PortfolioEdit() {
    const params = useParams();
    const { data: portfolio, error, isLoaded, axios } =
        useApi(`/api/portfolios/${params.portfolioId}`, "GET");

    if (!isLoaded) {
        return (
            <span>Loading portfolio...</span>
        );
    }

    if (error) {
        throw error;
    }

    return (
        <div>
            <PortfolioEditForm
                axios={ axios }
                portfolio={ portfolio } /><br />
            <PortfolioDeleteForm
                axios={ axios }
                portfolio={ portfolio } />
        </div>
    )
}
