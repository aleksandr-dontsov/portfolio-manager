import { useEffect, useState } from 'react';

export function useStream(url) {
    const [data, setData] = useState(null);
    useEffect(() => {
        if (!window.EventSource) {
            console.log('Event source is not supported in this browser.');
            return;
        }

        const sse = new EventSource(url, { withCredentials: true });

        sse.onmessage = (event) => {
            setData(event.data);
        };

        sse.onerror = (error) => {
            console.error(`EventSource '${url}' failed:`, error);
            sse.close()
        };

        return () => {
            console.log('connection closed')
            sse.close()
        }
    }, []);

    return { data }
}
