import { useEffect} from "react";
import { StatusCodes } from 'http-status-codes';
import { useAuth } from "./useAuth";
import { api } from '../api/api';

const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

export const useAxios = () => {
    const { setIsLoggedIn } = useAuth();

    useEffect(() => {
        const requestIntercept = api.interceptors.request.use(
            (request) => {
                // Before sending each request, get the CSRF token from the cookie and
                // add it to the headers
                const csrfToken = getCookie("csrf_access_token");
                if (csrfToken) {
                    request.headers["X-CSRF-TOKEN"] = csrfToken;
                }
                return request;
            },
            (error) => {
                return Promise.reject(error);
            }
        );

        const responseIntercept = api.interceptors.response.use(
            (response) => {
                return response;
            },
            (error) => {
                if (error.response.status === StatusCodes.UNAUTHORIZED) {
                    setIsLoggedIn(false);
                }
                return Promise.reject(error);
            }
        );

        return () => {
            api.interceptors.request.eject(requestIntercept);
            api.interceptors.response.eject(responseIntercept);
        };
    }, []);

    return api;
}
