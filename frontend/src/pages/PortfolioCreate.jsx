import { PortfolioForm } from '../components/PortfolioForm';

export default function PortfolioCreate() {
    const createPortfolioRequest = {
        method: "POST",
        url: "/api/v1/portfolios"
    };
    return (
        <PortfolioForm
            formName="Create"
            portfolioRequest={ createPortfolioRequest }/>
    );
}
