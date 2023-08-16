import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAxios } from '../hooks/useAxios';
import {
    EmailField,
    PasswordField,
    SubmitButton
} from '../components/Common';

export default function SignUp() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState("");
    // useNavigate returns a function that allows a user to navigate programatically
    const navigate = useNavigate();
    const axios = useAxios();

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (password != confirmPassword) {
            setError("Password and confirmation password are not equal");
            return;
        }
        try {
            await axios.request({
                method: "POST",
                data: {
                    email,
                    password,
                },
                url: "api/signup"
            })
        } catch (error) {
            console.log(error);
            setError(error.data.detail);
            return;
        }
        navigate("/login");
    };

    return (
        <div>
            <h2>Sign Up</h2>
            <form onSubmit={handleSubmit}>
                <EmailField
                    email={ email }
                    onEmailChange={ setEmail } /><br/>
                <PasswordField
                    label="Password:"
                    password={ password }
                    onPasswordChange={ setPassword }/><br/>
                <PasswordField
                    label="Confirm Password:"
                    password={ confirmPassword }
                    onPasswordChange={ setConfirmPassword }/><br/>
                <SubmitButton name="Sign Up" />
            </form>
            { error && <span>{error}</span> }
        </div>
    );
}
