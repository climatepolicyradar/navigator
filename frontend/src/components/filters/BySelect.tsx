const BySelect = ({ onChange, list, title, type, defaultValue }) => {
  return (
    <div>
      <div>{title}</div>
      <select
        className="border border-indigo-200 mt-2 small"
        defaultValue={defaultValue}
        onChange={(e) => {
          onChange(type, e.currentTarget.value);
        }}
      >
        {list.map((item, index) => (
          <option key={`${type}${index}`} value={item === 'All' ? '' : item}>
            {item}
          </option>
        ))}
      </select>
    </div>
  );
};
export default BySelect;
