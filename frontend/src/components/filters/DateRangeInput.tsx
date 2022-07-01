import { useState } from "react";

interface DateRangeInputProps {
  label: string;
  value: string | number;
  max: number;
  min: number;
  handleBlur(e: React.ChangeEvent<HTMLInputElement>): void;
}
const DateRangeInput = ({ label, value, handleBlur }: DateRangeInputProps) => {
  const [inputValue, setInputValue] = useState(value);

  const updateInputValue = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  return (
    <div>
      <label>{label}</label>
      <div className="relative">
        <input
          name={label}
          value={inputValue}
          onChange={updateInputValue}
          onBlur={handleBlur}
          type="text"
          className="border border-indigo-200 mt-2 small outline-none placeholder:text-indigo-300"
        />
      </div>
    </div>
  );
};
export default DateRangeInput;
