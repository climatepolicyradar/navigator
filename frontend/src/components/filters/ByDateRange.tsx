import React, { useState, useEffect } from "react";
import { currentYear } from "../../constants/timedate";
import DateRangeInput from "./DateRangeInput";
import DateRangeOption from "./DateRangeOption";

interface ByDateRangeProps {
  title: string;
  type: string;
  handleChange(values: number[]): void;
  defaultValues: number[];
  min: number;
  max: number;
  clear: boolean;
}

const ByDateRange = ({ title, handleChange, defaultValues, min, max, clear }: ByDateRangeProps) => {
  const [showDateInput, setShowDateInput] = useState(false);
  const [startYear, endYear] = defaultValues;

  useEffect(() => {
    if (!clear) setShowDateInput(false);
  }, [clear]);

  const isChecked = (range?: number): boolean => {
    return range ? Number(endYear) === currentYear() && Number(startYear) === endYear - range : showDateInput;
  };

  const setDateInputVisible = () => {
    setShowDateInput(true);
    handleChange([startYear, endYear]);
  };

  const selectRange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setShowDateInput(false);
    const thisYear = currentYear();
    const calculatedStart = thisYear - Number(e.target.value);
    handleChange([calculatedStart, thisYear]);
  };

  const inputCustomRange = (updatedDate: number, name: string) => {
    if (name === "From") {
      handleChange([updatedDate, Number(endYear)]);
    } else {
      handleChange([Number(startYear), updatedDate]);
    }
  };

  return (
    <div>
      <div>{title}</div>
      {/* TODO: make labels translatable */}
      <div className="mt-2 grid lg:grid-cols-2 gap-2">
        <DateRangeOption id="last5" label="in last 5 years" name="date_range" value="5" onChange={selectRange} checked={isChecked(5)} />
        <DateRangeOption id="last10" label="in last 10 years" name="date_range" value="10" onChange={selectRange} checked={isChecked(10)} />
        <DateRangeOption id="specify" label="specify range" name="date_range" value="specify" onChange={setDateInputVisible} checked={isChecked()} />
      </div>
      {showDateInput && (
        <div className="block lg:grid lg:grid-cols-2 gap-2 mt-2">
          <DateRangeInput label="Earliest year" name="From" value={startYear} min={min} max={endYear} handleBlur={inputCustomRange} />
          <DateRangeInput label="Latest year" name="To" value={endYear} min={startYear} max={max} handleBlur={inputCustomRange} />
        </div>
      )}
    </div>
  );
};
export default ByDateRange;
