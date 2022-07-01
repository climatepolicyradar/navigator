import { SyntheticEvent } from "react";

interface DateRangeOptionProps {
  id: string;
  label: string;
  name: string;
  value: string;
  onChange?(e: SyntheticEvent): void;
  checked?: boolean;
}

const DateRangeOption = ({ id, label, name, value, onChange, checked }: DateRangeOptionProps) => {
  return (
    <label className="checkbox-input flex items-center border p-2 rounded-md cursor-pointer border-indigo-200 bg-white" htmlFor={id}>
      <input
        className="text-white border-blue-500 cursor-pointer"
        id={id}
        type="radio"
        name={name}
        value={value}
        checked={checked}
        onClick={onChange}
      />
      <span className="pl-2 text-base">
        {/* TODO: make translatable */}
        {label}
      </span>
    </label>
  );
};

export default DateRangeOption;
