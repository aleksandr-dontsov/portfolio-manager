import { Navigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function ProtectedRoute({children}) {
    const user = useAuth();
    if (!user) {
        // user is not authenticated

        // Navigate element changes the current location when it is rendered.
        // Internally it uses the useNavigate hook
        return <Navigate to="/" />;
    }
    return children;
};
