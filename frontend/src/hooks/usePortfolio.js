import { createContext, useContext, useMemo } from "react";
import { useAxio } from '../hooks/useAxio';

export const PortfolioContext = createContext(null);

export const PortfolioProvider = ({ children }) => {
    const [portfolio, setPortfolio] = useState(null);

    // TODO: Provide methods for loading/editing/deleting portfolio

    return (
        <PortfolioContext.Provider value={portfolio}>
            {children}
        </PortfolioContext.Provider>
    );
}

export const usePortfolio = () => {
    return useContext(PortfolioContext);
}
