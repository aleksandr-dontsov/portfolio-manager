import React, {
    useState,
} from 'react';
import { useNavigate } from 'react-router-dom';
import { changePassword } from '../api/api';

export default function ChangePassword() {
    const [currentPassword, setCurrentPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState("");
    const { navigate } = useNavigate();

    const handleSubmit = async (event) => {
        // Prevent the browser's default behavior on form submit,
        // which would cause a page reload
        event.preventDefault();
        if (newPassword != confirmPassword) {
            setError("New and confirm passwords are not equal");
            return;
        }
        if (currentPassword === newPassword) {
            setError("New password cannot be the same as old password");
            return;
        }
        try {
            await changePassword(currentPassword, newPassword);
            navigate(-1);
        } catch (error) {
            setError("New password cannot be the same as old password");
        }
        // TODO: clear all states
    };

    return (
        <div>
            <h1>Change Password</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Current Password:
                    <input
                        type="password"
                        name="currentPassword"
                        value={currentPassword}
                        onChange={event => setCurrentPassword(event.target.value)}
                        required>
                    </input>
                </label>
                <label>
                    New Password:
                    <input
                        type="password"
                        name="newPassword"
                        value={newPassword}
                        onChange={event => setNewPassword(event.target.value)}
                        required>
                    </input>
                </label>
                <label>
                    Confirm Password:
                    <input
                        type="password"
                        name="confirmPassword"
                        value={confirmPassword}
                        onChange={event => setConfirmPassword(event.target.value)}
                        required>
                    </input>
                </label>
                <button type="submit">Change Password</button>
            </form>
            { error.length && <span>{error}</span>}
        </div>
    );
}
