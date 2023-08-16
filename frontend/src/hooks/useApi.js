import { useEffect, useState } from "react";
import { useAxios } from "./useAxios";

export const useApi = (url, method, payload) => {
    const axios = useAxios();
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);

    useEffect(() => {
        const sendRequest = async () => {
            try {
                setIsLoaded(false);
                const response = await axios.request({
                    method,
                    data: payload,
                    url,
                });
                setData(response.data);
            } catch (error) {
                setError(error);
            } finally {
                setIsLoaded(true);
            }
        };

        sendRequest();
    }, []);

    return { data, error, isLoaded, axios }
}
