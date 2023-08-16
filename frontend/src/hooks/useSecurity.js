import { useEffect } from 'react';
import { useLocalStorage } from './useLocalStorage';
import { useAxios } from './useAxios';
import { calculateTimeDiffInHours } from '../utils/utils';

const SECURITY_UPDATE_INTERVAL_HOURS = 12;

export function useSecurity() {
    const [securities, setSecurities] = useLocalStorage("securities", []);
    const axios = useAxios();

    useEffect(() => {
        const loadSecurities = async () => {
            try {
                const response = await axios.request({
                    url: "/api/securities",
                    method: "GET",
                });
                setSecurities(response.data);
            } catch (error) {
                console.error(`Cannot load securities. ${error.response.data.detail}`);
            }
        };
        const diffInHours = calculateTimeDiffInHours(new Date(securities.updateTimestamp), new Date());
        if (securities.value.length === 0 || diffInHours >= SECURITY_UPDATE_INTERVAL_HOURS) {
            loadSecurities();
        }
    }, []);

    return [securities.value, setSecurities];
}
