interface DateRangeOptionProps {
  id: string;
  label: string;
  name: string;
  value: string;
}

const DateRangeOption = ({ id, label, name, value }: DateRangeOptionProps) => {
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
        // checked={false}
        // onChange={handleClick}
      />
      <span className="text-xs font-medium pl-2 leading-none">
        {/* TODO: make translatable */}
        {label}
      </span>
    </label>
  );
};

export default DateRangeOption;
