import { useState } from 'react';
import {
    useNavigate,
    useParams,
} from 'react-router-dom';
import { useApi } from '../hooks/useApi';
import { SubmitButton } from '../components/Common';
import { PortfolioForm } from '../components/PortfolioForm';

function PortfolioEditForm({ portfolio }) {
    const editPortfolioRequest = {
        method: "PUT",
        url: `/api/portfolios/${portfolio.id}`
    };
    return (
        <PortfolioForm
            formName="Edit"
            portfolio={ portfolio }
            portfolioRequest={ editPortfolioRequest }/>
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
                portfolio={ portfolio } /><br />
            <PortfolioDeleteForm
                axios={ axios }
                portfolio={ portfolio } />
        </div>
    )
}
