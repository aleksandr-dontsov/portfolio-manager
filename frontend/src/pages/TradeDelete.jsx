import { redirect } from 'react-router-dom';
import { deleteTrade } from '../api/api';

export async function action({ params }) {
    if (!window.confirm(`Please confirm you want to delete the trade.`)) {
        return;
    }

    const errors = {};
    try {
        await deleteTrade(params.portfolioId, params.tradeId);
    } catch (error) {
        errors.response = error.data.detail;
    }

    if (Object.keys(errors).length) {
        return errors;
    }

    return redirect(`/portfolios/${params.portfolioId}`);
}
