import React from 'react';
import { NavLink } from 'react-router-dom';
import logoImage from '../assets/logo.svg';
import { useAuth } from '../hooks/useAuth';

export default function Header() {
    const { token, onLogout } = useAuth();
    return (
        <header className="header">
            <div className="logo">
                <img src={logoImage} alt="Portman logo" />
                <NavLink to="/">PortMan</NavLink>
            </div>
            <nav className="navbar">
                {token ?
                    <button type="button" onClick={onLogout}>Logout</button>
                :
                    <>
                        <NavLink to="/login">Login</NavLink>
                        <NavLink to="/signup">Sign Up</NavLink>
                    </>
                }
            </nav>
        </header>
    )
}
