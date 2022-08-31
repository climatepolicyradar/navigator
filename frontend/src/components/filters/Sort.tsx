import { sortOptions, sortOptionsBrowse } from "@constants/sortOptions";

type TProps = {
  updateSort: (e: any) => void;
  defaultValue: string;
  browse?: boolean;
};

const Sort = ({ updateSort, defaultValue, browse = false }: TProps) => {
  const options = browse ? sortOptionsBrowse : sortOptions;
  return (
    <>
      <div className="flex-shrink-0 font-medium text-indigo-400">Sort by:</div>
      <select className="border border-indigo-200 small ml-2 z-0" onChange={updateSort} defaultValue={defaultValue}>
        {options.map((item) => (
          <option key={item.value} value={item.value}>
            {item.label}
          </option>
        ))}
      </select>
    </>
  );
};
export default Sort;
