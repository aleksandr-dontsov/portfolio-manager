import React from 'react';
import {
    Outlet,
    Navigate,
    createBrowserRouter,
    Link,
    NavLink,
    useNavigation,
} from 'react-router-dom';

import {
    useAuth,
    AuthProvider,
} from '../hooks/useAuth';

// Import pages
import Home from '../pages/Home';
import Login from '../pages/Login';
import Error from '../pages/Error';
import SignUp from '../pages/SignUp';
import ChangePassword from '../pages/ChangePassword';
import Portfolios from '../pages/Portfolios';
import PortfolioCreate from '../pages/PortfolioCreate';
import PortfolioEdit from '../pages/PortfolioEdit';
import PortfolioDashboard from '../pages/PortfolioDashboard';
import TradeCreate from '../pages/TradeCreate';
import TradeEdit from '../pages/TradeEdit';
import {
    action as deleteTrade,
} from '../pages/TradeDelete';

import logoImage from '../assets/logo.svg';

function Header() {
    const { isLoggedIn, onLogout } = useAuth();
    return (
        <header className="header">
            <div className="logo">
                <img src={logoImage} alt="Portman logo" />
                <NavLink to="/">PortMan</NavLink>
            </div>
            <nav className="navbar">
                {isLoggedIn ?
                    <>
                        <NavLink to="/portfolios">Portfolios</NavLink>
                        <NavLink to="/settings">Settings</NavLink>
                        <button type="button" onClick={onLogout}>Logout</button>
                    </>
                :
                    <>
                        <NavLink to="/login">Login</NavLink>
                        <NavLink to="/signup">Sign Up</NavLink>
                    </>
                }
            </nav>
            <hr/>
        </header>
    )
}

function Footer() {
    return (
        <footer className="footer">
            <hr/>
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

function RootLayout() {
    const navigation = useNavigation();
    return (
        <AuthProvider>
            <Header />
            <div
                id="detail"
                className={
                    // navigation returns the current navigation state
                    // which is used for setting a class
                    navigation.state === "loading" ? "loading" : ""
                }
            >
                {/* This element will render different components depending on the URL */}
                <Outlet />
            </div>
            <Footer />
        </AuthProvider>
    );
}

function PublicLayout() {
    const { isLoggedIn } = useAuth();

    if (isLoggedIn) {
        return <Navigate to="/portfolios" />;
    }

    // <>...</> is  shorthand syntax for a React Fragment
    return (
        <>
            <Outlet />
        </>
    )
}

function ProtectedLayout() {
    const { isLoggedIn } = useAuth();

    if (!isLoggedIn) {
        return <Navigate to="/login" />;
    }

    return (
        <>
            <Outlet />
        </>
    );
}

export const router = createBrowserRouter([
    // Whenever the location changes, Router looks through all its
    // child routes to find the best match and renders the branch of the UI
    {
        // This is a "layout route", because it doesn't have a path. It participates in UI
        // nesting, but it does not add any segments to the URL
        element: <RootLayout />,
        // This will render instead of element if an error was thrown
        errorElement: <Error />,
        children: [
            {
                element: <PublicLayout />,
                children: [
                    {
                        path: "/",
                        element: <Home />,
                    },
                    {
                        path: "/login",
                        element: <Login />,
                    },
                    {
                        path: "/signup",
                        element: <SignUp />,
                    },
                ],
            },
            {
                element: <ProtectedLayout />,
                errorElement: <Error />,
                children: [
                    {
                        path: "/portfolios",
                        element: <Portfolios />,
                    },
                    {
                        path: "/portfolios/create",
                        element: <PortfolioCreate />,
                    },
                    {
                        path: "/portfolios/:portfolioId",
                        element: <PortfolioDashboard />,
                    },
                    {
                        path: "/portfolios/:portfolioId/edit",
                        element: <PortfolioEdit />,
                    },
                    {
                        path: "/portfolios/:portfolioId/trades/create",
                        element: <TradeCreate />,
                    },
                    {
                        path: "/portfolios/:portfolioId/trades/:tradeId/edit",
                        element: <TradeEdit />,
                    },
                    {
                        path: "/portfolios/:portfolioId/trades/:tradeId/delete",
                        action: deleteTrade,
                    },
                    {
                        path: "/change-password",
                        element: <ChangePassword />,
                    },
                ],
            },
        ],
    },
]);
