import { useState } from "react";

export const useLocalStorage = (keyName, defaultValue) => {
    // here we pass an initializer function. React will call this function
    // when initializing the component and store a return value as the initial state
    const [storedValue, setStoredValue] = useState(() => {
        try {
            // Web Storage API provides mechanisms by which browsers can store
            // key/value pairs, in a much more intuitive fashion than using cookies

            // window is the global object in the browser. It represents the browser window
            // localStorage is used to store data across browser sessions. The stored data
            // persist even if the page is refreshed or the browser is closed and reopened
            const value = window.localStorage.getItem(keyName);
            if (value) {
                // JSON is a namespace object contains static methods for parsing values from
                // and converting values to JSON
                return JSON.parse(value);
            } else {
                window.localStorage.setItem(keyName, JSON.stringify(defaultValue));
                return defaultValue;
            }
        } catch (err) {
            return defaultValue;
        }
    });
    const setValue = (newValue) => {
        try {
            window.localStorage.setItem(keyName, JSON.stringify(newValue));
        } catch (err) {}
        setStoredValue(newValue);
    };
    return [storedValue, setValue];
}
