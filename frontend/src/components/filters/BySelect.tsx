import { useEffect, useRef } from 'react';

const BySelect = ({
  onChange,
  list,
  title,
  keyField,
  keyFieldDisplay = null,
  filterType,
  defaultValue,
}) => {
  const selectRef = useRef(null);
  useEffect(() => {
    if (selectRef?.current) {
      selectRef.current.value = defaultValue;
    }
  }, [defaultValue, selectRef]);
  return (
    <div>
      <div>{title}</div>
      <select
        ref={selectRef}
        className="border border-indigo-200 mt-2 small"
        defaultValue={defaultValue}
        onChange={(e) => {
          onChange(filterType, e.currentTarget.value);
        }}
      >
        <option value="">All</option>
        {list.map((item, index) => (
          <option key={`${keyField}${index}`} value={item[keyField]}>
            {keyFieldDisplay ? item[keyFieldDisplay] : item[keyField]}
          </option>
        ))}
      </select>
    </div>
  );
};
export default BySelect;
