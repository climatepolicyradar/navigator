import { useState } from "react";
import Error from "../blocks/Error";

interface DateRangeInputProps {
  label: string;
  name: string;
  value: string | number;
  max: number;
  min: number;
  handleBlur(updatedDate: number, name: string): void;
}
const DateRangeInput = ({ label, name, value, handleBlur, min, max }: DateRangeInputProps) => {
  const [inputValue, setInputValue] = useState(value);
  const [error, setError] = useState("");

  const updateInputValue = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const onBlurHandler = () => {
    handleDateUpdate(Number(inputValue), name);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleDateUpdate(Number(inputValue), name);
    }
  };

  const handleDateUpdate = (updatedDate: number, name: string) => {
    setError("");
    if (typeof updatedDate !== "number") {
      setError("Please enter a valid year");
      return;
    }
    if (updatedDate > max) {
      setError("Please enter a year on or before " + max);
      return;
    }
    if (updatedDate < min) {
      setError("Please enter a year on or after " + min);
      return;
    }
    handleBlur(updatedDate, name);
  };

  return (
    <div>
      <label>{label}</label>
      <div className="relative">
        <input
          name={name}
          value={inputValue}
          onChange={updateInputValue}
          onBlur={onBlurHandler}
          onKeyDown={handleKeyDown}
          type="number"
          className="border border-indigo-200 mt-2 small outline-none placeholder:text-indigo-300"
        />
        {error && <Error message={error} />}
      </div>
    </div>
  );
};
export default DateRangeInput;
