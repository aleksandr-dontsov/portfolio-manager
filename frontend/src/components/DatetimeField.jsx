import { DateTime } from 'luxon';
import { toInputDatetimeLocal } from '../utils/utils';

export function DatetimeField({ datetime }) {
    return (
        <label>
            Date and time:
            <input
                type="datetime-local"
                name="datetime"
                defaultValue={ datetime }
                max={ toInputDatetimeLocal(DateTime.now()) }
                required />
        </label>
    );
}
