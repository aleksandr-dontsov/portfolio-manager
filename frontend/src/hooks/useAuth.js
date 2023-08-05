import { createContext, useContext, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { useLocalStorage } from "./useLocalStorage";
import { api } from "../api/api";

// 1. create context
// Context lets the parent component make some information
// available to other components in the tree below without
// passing this information explicitly through props
export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    // TODO: Fix the problem with isLoggedIn stale value
    const [isLoggedIn, setIsLoggedIn] = useLocalStorage("isLoggedIn", false);
    const navigate = useNavigate();

    // call this function when you want to authenticate the user
    const handleLogin = async (email, password) => {
        await api.post("/api/login", {
            email,
            password
        });
        setIsLoggedIn(true);
        navigate("/portfolios");
    }

    // call this function to sign out logged in user
    const handleLogout = () => {
        setIsLoggedIn(false);
        // replace: true will be used by navigation to replace
        // the current entry in the history stack instead of adding a new one
        navigate("/", { replace: true });
    }

    // useMemo is a hook that lets one cache the result of a calculation between re-renders
    const value = useMemo(
        () => ({
            isLoggedIn,
            setIsLoggedIn,
            onLogin: handleLogin,
            onLogout: handleLogout,
        }),
        [isLoggedIn]
    );

    // 3. provide context
    // wraps children components with a context provider
    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};

// this hook allows us to manage  the user's state through
// login and logout methods
export const useAuth = () => {
    // 2. use context
    // it tells React that the component wants to read AuthContext
    return useContext(AuthContext);
}
