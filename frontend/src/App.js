import {
    Routes,
    Route,
    Outlet,
    Navigate,
} from 'react-router-dom';

import Header from './components/Header';
import Footer from './components/Footer';

import {
    useAuth,
    AuthProvider,
} from './hooks/useAuth';

import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import ErrorPage from './pages/ErrorPage';
import SignUpPage from './pages/SignUpPage';
import PortfoliosPage from './pages/PortfoliosPage';
import PortfolioPage from './pages/PortfolioPage';

export default function App() {
    return (
        <div className="App">
            {/* Whenever the location changes, <Routes> looks through all its
                child routes to find the best match and renders the branch of the UI */}
            <Routes>
                {/* This is a "layout route", because it doesn't have a path. It participates in UI
                    nesting, but it does not add any segments to the URL*/}
                <Route
                    element={ <AuthLayout /> }
                    // This will render instead of element if an error was thrown
                    errorElement={ <ErrorPage /> }
                >
                    <Route element={ <HomeLayout /> } >
                        <Route path="/" element={ <HomePage /> } />
                        <Route path="/login" element={ <LoginPage /> } />
                        <Route path="/signup" element={ <SignUpPage /> } />
                    </Route>
                    <Route element={ <ProtectedLayout /> } >
                        <Route path="/portfolios" element={ <PortfoliosPage /> } />
                        <Route path="/portfolios/:portfolioId" element={ <PortfolioPage /> } />
                    </Route>
                </Route>
            </Routes>
        </div>
    );
}

function AuthLayout() {
    return (
        <AuthProvider>
            <Header />
            {/* This element will render different components depending on the URL */}
            <Outlet />
            <Footer />
        </AuthProvider>
    );
}

function HomeLayout() {
    const { token } = useAuth();

    if (token) {
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
    const { token } = useAuth();

    if (!token) {
        return <Navigate to="/" />;
    }

    return (
        <>
            <Outlet />
        </>
    );
}
