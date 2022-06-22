import { useState, useRef, useEffect } from 'react';
import { DownArrowIcon } from '../svg/Icons';
import { currentYear, minYear } from '../../constants/timedate';

interface DateRangeInputProps {
  label: string;
  value: string | number;
  max: number;
  min: number;
  handleBlur(e): void;
}
const DateRangeInput = ({
  label,
  value,
  max,
  min,
  handleBlur,
}: DateRangeInputProps) => {
  const [showYears, setShowYears] = useState(false);
  const [inputValue, setInputValue] = useState(value);
  const [years, setYears] = useState([]);
  const inputRef = useRef(null);

  const toggleYears = () => {
    setShowYears(!showYears);
  };
  const selectInputValue = (e) => {
    const value = e.target.innerText;

    setInputValue(value);
    setShowYears(false);
    handleBlur(e);
  };
  const updateInputValue = (e) => {
    const value = e.target.value;
    setInputValue(value);
    setShowYears(false);
  };
  useEffect(() => {
    setYears(Array.from({ length: max - min }, (_, i) => i + min));
  }, [min, max]);
  return (
    <div>
      <label>{label}</label>
      <div className="relative">
        <input
          ref={inputRef}
          name={label}
          value={inputValue}
          onChange={updateInputValue}
          onBlur={handleBlur}
          type="text"
          className="border border-indigo-200 mt-2 small outline-none placeholder:text-indigo-300"
        />
        <button
          onClick={toggleYears}
          className="absolute right-0 top-1 h-full flex items-center justify-center px-4"
        >
          <DownArrowIcon />
        </button>
        <div
          className={`${
            showYears ? 'block' : 'hidden'
          } absolute top-2 right-0 bg-white w-full border border-indigo-200 rounded h-48 overflow-auto z-10`}
        >
          <ul>
            {years.map((year) => (
              <li key={year}>
                <button
                  onClick={selectInputValue}
                  className="p-1 w-full hover:bg-lightgray"
                  value={year}
                >
                  {year}
                </button>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};
export default DateRangeInput;
