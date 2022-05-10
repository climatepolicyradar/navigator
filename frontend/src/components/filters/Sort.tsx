import { sortOptions } from '../../constants/sortOptions';

const Sort = ({ updateSort, defaultValue }) => {
  return (
    <>
      <div className="flex-shrink-0 font-medium text-indigo-400">Sort by:</div>
      <select
        className="border border-indigo-200 small ml-2"
        onChange={updateSort}
        defaultValue={defaultValue}
      >
        {sortOptions.map((item, index) => (
          <option key={item.value} value={item.value}>
            {item.label}
          </option>
        ))}
      </select>
    </>
  );
};
export default Sort;
