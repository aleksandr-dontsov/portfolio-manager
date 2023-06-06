import React from 'react';
import { Link } from 'react-router-dom';

export default function Footer() {
    return (
        <footer className="footer">
            <p>PortMan</p>
            <div>
                <p>Product</p>
                <ul>
                    <li><Link to="/portfolio-management">Portfolio management</Link></li>
                    <li><Link to="/performance-tracking">Performance tracking</Link></li>
                </ul>
            </div>
            <div>
                <p>Legal</p>
                <ul>
                    <li><Link to="/privacy">Privacy Policy</Link></li>
                    <li><Link to="/cookies">Cookie Policy</Link></li>
                    <li><Link to="/terms">Terms of Service</Link></li>
                </ul>
            </div>
        </footer>
    )
}
