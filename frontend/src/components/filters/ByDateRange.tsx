import { useState } from 'react';
import DateRangeInput from './DateRangeInput';
import DateRangeOption from './DateRangeOption';

interface ByDateRangeProps {
  title: string;
}

const ByDateRange = ({ title }: ByDateRangeProps) => {
  const [showDateInput, setShowDateInput] = useState(false);
  const toggleDateInput = () => {
    setShowDateInput(!showDateInput);
    console.log('hello?');
  };
  const clickOther = () => {};
  return (
    <div>
      {console.log(showDateInput)}
      <div>{title}</div>
      {/* TODO: make labels translatable */}
      <div className="mt-4 grid lg:grid-cols-2 gap-2">
        <DateRangeOption
          id="last5"
          label="in last 5 years"
          name="date_range"
          value="last5"
        />
        <DateRangeOption
          id="last10"
          label="in last 10 years"
          name="date_range"
          value="last10"
        />
        <DateRangeOption
          id="specify"
          label="specify range"
          name="date_range"
          value="specify"
          onChange={toggleDateInput}
        />
      </div>
      {showDateInput}
      <div
        className={`${
          showDateInput ? 'block' : 'hidden'
        } lg:grid lg:grid-cols-2 gap-2 mt-2`}
      >
        <DateRangeInput label="From" />
        <DateRangeInput label="To" />
      </div>
    </div>
  );
};
export default ByDateRange;
