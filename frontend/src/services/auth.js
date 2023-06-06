import axios from 'axios';

export const signup = async (email, password) => {
    const response = await axios.post("/api/signup", {
        email,
        password
    });
    return response.data;
}

export const login = () =>
    new Promise((resolve) => {
        setTimeout(() => resolve('2342f2f1d131rf12'), 250);
    });
