export function AmountField({ label, name, min, max, placeholder, step, defaultValue }) {
    return (
        <label>
            {label}
            <input
                type="number"
                name={ name }
                min={ min }
                max={ max }
                placeholder={ placeholder }
                step={ step }
                defaultValue={ defaultValue }
                required />
        </label>
    );
}
