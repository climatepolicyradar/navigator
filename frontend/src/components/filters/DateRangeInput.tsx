import { useState } from "react";
import Error from "../blocks/Error";

interface DateRangeInputProps {
  label: string;
  value: string | number;
  max: number;
  min: number;
  handleBlur(updatedDate: number, name: string): void;
}
const DateRangeInput = ({ label, value, handleBlur, min, max }: DateRangeInputProps) => {
  const [inputValue, setInputValue] = useState(value);
  const [error, setError] = useState("");

  const updateInputValue = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const onBlurHandler = () => {
    handleDateUpdate(Number(inputValue), label);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleDateUpdate(Number(inputValue), label);
    }
  };

  const handleDateUpdate = (updatedDate: number, name: string) => {
    setError("");
    if (updatedDate > max || updatedDate < min) {
      setError("Please enter a valid date");
      return;
    }
    handleBlur(updatedDate, name);
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
          onKeyDown={handleKeyDown}
          type="text"
          className="border border-indigo-200 mt-2 small outline-none placeholder:text-indigo-300"
        />
        {error && <Error message={error} />}
      </div>
    </div>
  );
};
export default DateRangeInput;
