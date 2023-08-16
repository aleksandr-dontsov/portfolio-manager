import { useNavigate } from 'react-router-dom';

export function EmailField({ email, onEmailChange }) {
    return (
        <label>
            Email:
            <input
                type="email"
                name="email"
                value={ email }
                onChange={event => onEmailChange(event.target.value)}
                required>
            </input>
        </label>
    );
}

export function PasswordField({ label, password, onPasswordChange }) {
    return (
        <label>
            {label}
            <input
                type="password"
                autoComplete="password"
                value={ password }
                onChange={ event => onPasswordChange(event.target.value) }
                required>
            </input>
        </label>
    );
}

export function TextField({ text, placeholder }) {
    return (
        <label>
            Name:
            <input
                type="plain"
                name="name"
                defaultValue={ text }
                placeholder={ placeholder }
                maxLength="150"
                required />
        </label>
    );
}

export function SubmitButton({ name }) {
    return (
        <button type="submit">{name}</button>
    );
}

export function CancelButton() {
    const navigate = useNavigate();
    const onClick = () => {
        navigate(-1);
    }
    return (
        <button type="button" onClick={onClick}>Cancel</button>
    );
}
