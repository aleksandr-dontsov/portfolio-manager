import { useCallback, useEffect, useRef } from 'react';

export const useTimeout = (callback, delay) => {
    const callbackRef = useRef(callback);
    const timeoutRef = useRef();

    // Ensures that the ref always points out to the latest callback
    useEffect(() => {
        callbackRef.current = callback;
    }, [callback]);

    // Initializes the timer
    const set = useCallback(() => {
        timeoutRef.current = setTimeout(() => callbackRef.current(), delay);
    }, [delay])

    // Clears any existing timer
    const clear = useCallback(() => {
        timeoutRef.current && clearTimeout(timeoutRef.current);
    })

    // Reset the timer
    const reset = useCallback(() => {
        clear();
        set();
    }, [clear, set]);

    return { reset, clear };
}
