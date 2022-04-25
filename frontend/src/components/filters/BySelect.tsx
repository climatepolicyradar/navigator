const BySelect = ({ onChange, list, title, type }) => {
  return (
    <div>
      <div>{title}</div>
      <select
        className="border border-indigo-200 mt-2 small"
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
