import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export function DeleteForm(formName, deleteRequest, confirmationText) {
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!window.confirm(confirmationText)) {
            return;
        }
        try {
            await axios.request(deleteRequest);
        } catch (error) {
            setError(error);
            return;
        }
        navigate(-1);
    }

    return (
        <div>
            <h2>{ formName }</h2>
            <form
                method="delete"
                onSubmit={handleSubmit}
            >
                <SubmitButton name="Delete" />
            </form>
            { error && <span>{error.response.data.detail}</span> }
        </div>
    );
}
