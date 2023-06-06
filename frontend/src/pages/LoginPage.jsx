import React from 'react';
import { useAuth } from '../hooks/useAuth';

export default function LoginPage() {
    const { onLogin } = useAuth();
    return (
        <>
            <p>This is a Login page</p>
            <button type="button" onClick={onLogin}>
                Log In
            </button>
        </>
    )
}
