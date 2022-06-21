import { useState } from 'react';
import { DownArrowIcon } from '../svg/Icons';
interface DateRangeInputProps {
  label: string;
}
const DateRangeInput = ({ label }: DateRangeInputProps) => {
  const [showYears, setShowYears] = useState(false);
  const years = [2020, 2021, 2022];
  const toggleYears = () => {
    setShowYears(!showYears);
  };
  return (
    <div>
      <label>{label}</label>
      <div className="relative">
        <input
          type="text"
          className="border border-indigo-200 mt-2 small outline-none placeholder:text-indigo-300"
        />
        <button
          onClick={toggleYears}
          className="absolute right-0 top-1 h-full flex items-center justify-center px-4"
        >
          <DownArrowIcon />
        </button>

        <ul
          className={`${
            showYears ? 'block' : 'hidden'
          } absolute top-2 right-0 bg-white w-full border border-indigo-200 rounded`}
        >
          {years.map((year) => (
            <li key={year}>
              <button
                onClick={toggleYears}
                className="p-1 w-full hover:bg-lightgray"
              >
                {year}
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};
export default DateRangeInput;
