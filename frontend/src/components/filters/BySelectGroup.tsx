import { useEffect, useRef } from 'react';

function BySelectGroup({
  onChange,
  list,
  title,
  keyField,
  filterType,
  defaultValue,
}) {
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
        {list.map((item) => (
          <optgroup key={`${item[keyField]}`} label={item[keyField]}>
            {item.children.map((item) => (
              <option
                key={`${item[keyField]}|${item.parent}`}
                value={`${item[keyField]}|${item.parent}`}
                disabled={item?.children !== undefined}
              >
                {item[keyField]}
              </option>
            ))}
          </optgroup>
        ))}
      </select>
    </div>
  );
}
export default BySelectGroup;
