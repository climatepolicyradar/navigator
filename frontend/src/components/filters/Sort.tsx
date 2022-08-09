import { sortOptions } from '../../constants/sortOptions';

function Sort({ updateSort, defaultValue }) {
  return (
    <>
      <div className="flex-shrink-0 font-medium text-indigo-400">Sort by:</div>
      <select
        className="border border-indigo-200 small ml-2 z-0"
        onChange={updateSort}
        defaultValue={defaultValue}
      >
        {sortOptions.map((item) => (
          <option key={item.value} value={item.value}>
            {item.label}
          </option>
        ))}
      </select>
    </>
  );
}
export default Sort;
