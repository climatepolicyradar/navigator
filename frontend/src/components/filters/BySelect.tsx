const BySelect = ({
  onChange,
  list,
  title,
  keyField,
  filterType,
  defaultValue,
}) => {
  return (
    <div>
      <div>{title}</div>
      <select
        className="border border-indigo-200 mt-2 small"
        defaultValue={defaultValue}
        onChange={(e) => {
          onChange(filterType, e.currentTarget.value);
        }}
      >
        <option value="">All</option>
        {list.map((item, index) => (
          <option key={`${keyField}${index}`} value={item[keyField]}>
            {item[keyField]}
          </option>
        ))}
      </select>
    </div>
  );
};
export default BySelect;
