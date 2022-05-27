import { useEffect, useRef, useState } from 'react';
import { sortData } from '../../utils/sorting';

const BySelect = ({
  onChange,
  list,
  title,
  keyField,
  keyFieldDisplay = null,
  filterType,
  defaultValue,
}) => {
  const [sortedList, setSortedList] = useState(list);
  const selectRef = useRef(null);
  useEffect(() => {
    if (selectRef?.current) {
      selectRef.current.value = defaultValue;
    }
  }, [defaultValue, selectRef]);
  useEffect(() => {
    setSortedList(sortData(list, keyField));
  }, [list]);
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
        {sortedList.map((item, index) => (
          <option key={`${keyField}${index}`} value={item[keyField]}>
            {keyFieldDisplay ? item[keyFieldDisplay] : item[keyField]}
          </option>
        ))}
      </select>
    </div>
  );
};
export default BySelect;
