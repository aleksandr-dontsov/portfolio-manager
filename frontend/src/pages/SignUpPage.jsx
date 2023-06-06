import React, {
    useState,
} from 'react';
import { useNavigate } from 'react-router-dom';
import { signup } from "../services/auth";

export default function SignUpPage() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    // useNavigate returns a function that allows a user to navigate programatically
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!email || !password || password !== confirmPassword) {
            alert("Please fill out all fields correctly");
            return;
        }
        try {
            const response = await signup(email, password);
            alert(response.message);
            navigate("/portfolios");
        } catch (error) {
            alert(error.response.data.detail);
        }
    }

    return (
        <form onSubmit={handleSubmit}>
            <label>
                Email:
                <input
                    type="email"
                    name="email"
                    value={email}
                    onChange={event => setEmail(event.target.value)}>
                </input>
            </label>
            <label>
                Password:
                <input
                    type="password"
                    name="password"
                    value={password}
                    onChange={event => setPassword(event.target.value)}>
                </input>
            </label>
            <label>
                Confirm Password:
                <input
                    type="password"
                    name="confirmPassword"
                    value={confirmPassword}
                    onChange={event => setConfirmPassword(event.target.value)}>
                </input>
            </label>
            <button type="submit">Sign Up</button>
        </form>
    )
}
