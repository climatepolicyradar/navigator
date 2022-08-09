import { useEffect, useRef, useState } from 'react';
import { sortData } from '@utils/sorting';

type TProps = {
  onChange(type: string, value: string, action?: string): void;
  list: any[];
  title: string;
  keyField: string;
  keyFieldDisplay?: string;
  filterType: string;
  defaultValue?: string;
  defaultText?: string;
};

function BySelect({
  onChange,
  list,
  title,
  keyField,
  keyFieldDisplay = null,
  filterType,
  defaultValue,
  defaultText = 'All',
}: TProps) {
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
        onChange={(e) => {
          onChange(filterType, e.currentTarget.value);
        }}
        value={defaultValue}
      >
        <option value="">{defaultText}</option>
        {sortedList.map((item, index) => (
          <option key={`${keyField}${index}`} value={item[keyField]}>
            {keyFieldDisplay ? item[keyFieldDisplay] : item[keyField]}
          </option>
        ))}
      </select>
    </div>
  );
}
export default BySelect;
