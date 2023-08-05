import React, {
    useState,
} from 'react';
import { useAuth } from '../hooks/useAuth';
import {
    EmailField,
    PasswordField,
    SubmitButton
} from '../components/Common';

export default function Login() {
    const { onLogin } = useAuth();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleSubmit = async (event) => {
        // Prevent the browser's default behavior on form submit,
        // which would cause a page reload
        event.preventDefault();
        try {
            await onLogin(email, password);
        } catch (error) {
            setError(error.response.data.detail);
        }
    };

    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <EmailField
                    email={ email }
                    onEmailChange={ setEmail } /><br/>
                <PasswordField
                    label="Password:"
                    password={ password }
                    onPasswordChange={ setPassword }/><br/>
                <SubmitButton name="Login" />
            </form>
            { error && <span>{error}</span> }
        </div>
    );
}
