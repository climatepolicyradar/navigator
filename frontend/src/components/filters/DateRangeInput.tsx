import { useState } from "react";
import Error from "../blocks/Error";

interface DateRangeInputProps {
  label: string;
  value: string | number;
  max: number;
  min: number;
  handleBlur(e: React.ChangeEvent<HTMLInputElement>): void;
}
const DateRangeInput = ({ label, value, handleBlur, min, max }: DateRangeInputProps) => {
  const [inputValue, setInputValue] = useState(value);
  const [error, setError] = useState("");

  const updateInputValue = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const onBlurHandler = (e: React.ChangeEvent<HTMLInputElement>) => {
    setError("");
    const val = Number(e.target.value);
    if (val > max || val < min) {
      setError("Please enter a valid date");
      return;
    }
    handleBlur(e);
  };

  return (
    <div>
      <label>{label}</label>
      <div className="relative">
        <input
          name={label}
          value={inputValue}
          onChange={updateInputValue}
          onBlur={onBlurHandler}
          type="text"
          className="border border-indigo-200 mt-2 small outline-none placeholder:text-indigo-300"
        />
        {error && <Error message={error} />}
      </div>
    </div>
  );
};
export default DateRangeInput;
