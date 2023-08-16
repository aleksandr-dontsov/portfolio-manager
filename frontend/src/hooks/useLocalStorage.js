import { useState } from "react";

// Each local storage item contains value and updateTimestamp attributes
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
            const item = window.localStorage.getItem(keyName);
            if (item) {
                // JSON is a namespace object contains static methods for parsing values from
                // and converting values to JSON
                const object = JSON.parse(item);
                return {
                    value: object.value,
                    updateTimestamp: object.updateTimestamp,
                }
            } else {
                const item = {
                    value: defaultValue,
                    updateTimestamp: new Date().toISOString(),
                };
                window.localStorage.setItem(keyName, JSON.stringify(item));
                return item;
            }
        } catch (err) {
            return {
                value: defaultValue,
                updateTimestamp: new Date().toISOString(),
            };
        }
    });
    const setValue = (newValue) => {
        const object = {
            value: newValue,
            updateTimestamp: new Date().toISOString(),
        };
        try {
            window.localStorage.setItem(keyName, JSON.stringify(object));
        } catch (err) {}
        setStoredValue(object);
    };
    return [storedValue, setValue];
}
