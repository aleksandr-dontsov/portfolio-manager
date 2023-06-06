import React from 'react';
import { Link } from 'react-router-dom';
import chartImage from '../assets/chart.svg';

export default function MainPage() {
    return (
        <main className="main">
            <h1>The Simplest Financial Portfolio Manager</h1>
            <ul>
                <li>Create multiple portfolios in different currencies</li>
                <li>Add your favorite stocks, ETFs and other assets</li>
                <li>Track the performance of portfolios and positions</li>
            </ul>
            <Link to="/signup">Get started for free</Link>
            <img src={chartImage} />
        </main>
    )
}
