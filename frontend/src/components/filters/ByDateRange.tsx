import { useState, useEffect } from 'react';
import { currentYear } from '../../constants/timedate';
import DateRangeInput from './DateRangeInput';
import DateRangeOption from './DateRangeOption';

// type="year_range"
// handleChange={handleYearChange}
// defaultValues={searchCriteria.year_range}
// min={minYear}
// max={currentYear}
interface ByDateRangeProps {
  title: string;
  type: string;
  handleChange(values: number[]): void;
  defaultValues: string[] | number[];
  min: number;
  max: number;
}

const ByDateRange = ({
  title,
  type,
  handleChange,
  defaultValues,
  min,
  max,
}: ByDateRangeProps) => {
  const [showDateInput, setShowDateInput] = useState(false);
  const dateInputVisible = () => {
    setShowDateInput(true);
  };
  const hideDateInput = () => {
    setShowDateInput(false);
  };
  const selectRange = (e: any) => {
    hideDateInput();
    const type = (e.target as HTMLInputElement).value;
    const thisYear = currentYear();
    const offset = Number(type);
    handleChange([thisYear - offset, thisYear]);
  };
  return (
    <div>
      <div>{title}</div>
      {/* TODO: make labels translatable */}
      <div className="mt-4 grid lg:grid-cols-2 gap-2">
        <DateRangeOption
          id="last5"
          label="in last 5 years"
          name="date_range"
          value="5"
          onChange={selectRange}
        />
        <DateRangeOption
          id="last10"
          label="in last 10 years"
          name="date_range"
          value="10"
          onChange={selectRange}
        />
        <DateRangeOption
          id="specify"
          label="specify range"
          name="date_range"
          value="specify"
          onChange={dateInputVisible}
        />
      </div>
      <div
        className={`${
          showDateInput ? 'block lg:grid' : 'hidden'
        } lg:grid-cols-2 gap-2 mt-2`}
      >
        <DateRangeInput label="From" />
        <DateRangeInput label="To" />
      </div>
    </div>
  );
};
export default ByDateRange;
