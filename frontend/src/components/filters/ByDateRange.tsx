import { useState, useEffect } from 'react';
import { currentYear, minYear } from '../../constants/timedate';
import DateRangeInput from './DateRangeInput';
import DateRangeOption from './DateRangeOption';

interface ByDateRangeProps {
  title: string;
  type: string;
  handleChange(values: number[]): void;
  defaultValues: number[];
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
  const [selected, setSelected] = useState('');
  const [startYear, endYear] = defaultValues;

  const setDefaultSelected = () => {
    const current = currentYear();
    const start = Number(startYear);
    const end = Number(endYear);
    if (start === end - 5 && end === current) {
      setSelected('5');
    } else if (start === end - 10 && end === current) {
      setSelected('10');
    } else if (start !== minYear && end !== current) {
      setSelected('custom');
    }
  };
  const setDateInputVisible = () => {
    setShowDateInput(true);
    setSelected('custom');
    handleChange([minYear, currentYear()]);
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
  const inputCustomRange = (e) => {
    if (e.target.name === 'From') {
      handleChange([Number(e.target.value), Number(endYear)]);
    } else {
      handleChange([Number(startYear), Number(e.target.value)]);
    }
  };

  useEffect(() => {
    setDefaultSelected();
  }, [defaultValues]);
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
          checked={selected === '5'}
        />
        <DateRangeOption
          id="last10"
          label="in last 10 years"
          name="date_range"
          value="10"
          onChange={selectRange}
          checked={selected === '10'}
        />
        <DateRangeOption
          id="specify"
          label="specify range"
          name="date_range"
          value="specify"
          onChange={setDateInputVisible}
          checked={selected === 'custom'}
        />
      </div>
      <div
        className={`${
          showDateInput ? 'block lg:grid' : 'hidden'
        } lg:grid-cols-2 gap-2 mt-2`}
      >
        <DateRangeInput
          label="From"
          value={Number(startYear)}
          min={Number(minYear)}
          max={Number(endYear)}
          handleBlur={inputCustomRange}
        />
        <DateRangeInput
          label="To"
          value={Number(endYear)}
          min={Number(startYear)}
          max={currentYear()}
          handleBlur={inputCustomRange}
        />
      </div>
    </div>
  );
};
export default ByDateRange;
