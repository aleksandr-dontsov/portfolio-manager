import { useEffect } from 'react';
import { useTimeout } from './useTimeout';

export const useDebounce = (callback, delay) => {
    const { reset, clear } = useTimeout(callback, delay);

    useEffect(reset, [reset])
    useEffect(clear, [])
}
