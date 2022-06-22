import { useState, useRef } from 'react';
import { DownArrowIcon } from '../svg/Icons';
interface DateRangeInputProps {
  label: string;
}
const DateRangeInput = ({ label }: DateRangeInputProps) => {
  const [showYears, setShowYears] = useState(false);
  const [value, setValue] = useState('');
  const inputRef = useRef(null);
  const years = [
    2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021,
    2022,
  ];
  const toggleYears = () => {
    setShowYears(!showYears);
  };
  const selectInputValue = (e) => {
    const value = e.target.innerText;
    setValue(value);
    setShowYears(false);
  };
  const setInputValue = (e) => {
    const value = e.target.value;
    setValue(value);
    setShowYears(false);
  };
  return (
    <div>
      <label>{label}</label>
      <div className="relative">
        <input
          ref={inputRef}
          value={value}
          onChange={setInputValue}
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
