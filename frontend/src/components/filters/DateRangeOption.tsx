import { ChangeEvent } from 'react';
interface DateRangeOptionProps {
  id: string;
  label: string;
  name: string;
  value: string;
  onChange?(e: ChangeEvent): void;
  checked?: boolean;
}

const DateRangeOption = ({
  id,
  label,
  name,
  value,
  onChange = () => {},
  checked = false,
}: DateRangeOptionProps) => {
  return (
    <label
      className="checkbox-input flex items-center border border-indigo-200 p-2 rounded cursor-pointer"
      htmlFor={id}
    >
      <input
        className="text-white border-blue-500"
        id={id}
        type="radio"
        name={name}
        value={value}
        checked={checked}
        onChange={onChange}
      />
      <span className="text-xs font-medium pl-2 leading-none">
        {/* TODO: make translatable */}
        {label}
      </span>
    </label>
  );
};

export default DateRangeOption;
