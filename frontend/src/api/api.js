import axios from 'axios';
import { StatusCodes } from 'http-status-codes';
import { AuthContext, setIsLoggedIn, useAuth } from '../hooks/useAuth';
import { useNavigate } from 'react-router-dom';
import { useContext } from 'react';

// Create a new instance of axios with the default config
export const api = axios.create({
    baseURL: "http://localhost:3000",
    timeout: 10000,
    withCredentials: true, // to send and receive cookies
})

// Axios does throw an error if a REST API endpoint returns an HTTP
// code that falls outside the range of 2xx
export const signup = async (email, password) => {
    return await api.post("/api/signup", {
        email,
        password
    });
}

export const changePassword = async (currentPassword, newPassword) => {
    return await api.post("/api/change-password", {
        current_password: currentPassword,
        new_password: newPassword,
    });
}

///////////////////////////
// Trade api calls
///////////////////////////

export const getTrade = async (portfolioId, tradeId) => {
    return await api.get(`/api/portfolios/${portfolioId}/trades/${tradeId}`);
}

export const createTrade = async (portfolioId, trade) => {
    return await api.post(`/api/portfolios/${portfolioId}/trades`, {
        security_id: trade.securityId,
        currency_id: trade.currencyId,
        trade_type: trade.type,
        trade_datetime: trade.datetime,
        unit_price: trade.unitPrice,
        quantity: trade.quantity,
        brokerage_fee: trade.brokerageFee,
    });
}

export const updateTrade = async (portfolioId, tradeId, trade) => {
    return await api.put(`/api/portfolios/${portfolioId}/trades/${tradeId}`, {
        security_id: trade.securityId,
        currency_id: trade.currencyId,
        trade_type: trade.type,
        trade_datetime: trade.datetime,
        unit_price: trade.unitPrice,
        quantity: trade.quantity,
        brokerage_fee: trade.brokerageFee,
    });
}

export const deleteTrade = async (portfolioId, tradeId) => {
    return await api.delete(`/api/portfolios/${portfolioId}/trades/${tradeId}`, {
        portfolio_id: portfolioId
    });
}
