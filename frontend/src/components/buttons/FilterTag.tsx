interface FilterTagProps {
  onClick(): void;
  item: string;
}
const FilterTag = ({ onClick, item }) => {
  return (
    <div className="rounded bg-indigo-600 text-white flex py-1 px-2 font-medium">
      <div className="text-xs">{item}</div>
      <button onClick={onClick} className="ml-2 text-lg leading-none">
        &times;
      </button>
    </div>
  );
};
export default FilterTag;
