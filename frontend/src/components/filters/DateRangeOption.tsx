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
    <label className="checkbox-input flex items-center border py-2 px-1 rounded-md cursor-pointer border-indigo-200 bg-white" htmlFor={id}>
      <input
        className="text-white border-indigo-400 cursor-pointer"
        id={id}
        type="radio"
        name={name}
        value={value}
        checked={checked}
        onClick={onChange}
        onChange={onChange}
      />
      <span className="pl-2 text-sm">
        {/* TODO: make translatable */}
        {label}
      </span>
    </label>
  );
};

export default DateRangeOption;
