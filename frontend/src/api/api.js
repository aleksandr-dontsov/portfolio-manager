import axios from 'axios';

// Create a new instance of axios with the default config
export const api = axios.create({
    baseURL: "http://localhost:3000",
    timeout: 10000,
    withCredentials: true, // to send and receive cookies
})

export function getQuotesUrl(securities) {
    const params = new URLSearchParams({
        'securities': securities.join(',')
    });
    // For SSE the requests will be sent directly to the backend without using proxy
    // Otherwise a client cannot receive any events from the backend
    return new URL(`?${params}`, 'http://localhost:8000/api/v1/securities/quotes/stream');
}

export const changePassword = async (currentPassword, newPassword) => {
    return await api.post("/api/v1/change-password", {
        current_password: currentPassword,
        new_password: newPassword,
    });
}
