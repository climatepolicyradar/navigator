import { useEffect, useState } from "react";
import { sortOptions, sortOptionsBrowse } from "@constants/sortOptions";

type TProps = {
  updateSort: (e: any) => void;
  defaultValue: string;
  browse?: boolean;
};

const Sort = ({ updateSort, defaultValue, browse = false }: TProps) => {
  const [options, setOptions] = useState(sortOptions);
  const [defaultV, setDefault] = useState("");

  useEffect(() => {
    setOptions(browse ? sortOptionsBrowse : sortOptions);
  }, [browse]);

  useEffect(() => {
    setDefault(defaultValue);
  }, [defaultValue]);

  return (
    <>
      <div className="flex-shrink-0 font-medium text-indigo-400">Sort by:</div>
      <select className="border border-indigo-200 small ml-2 z-0" onChange={updateSort} defaultValue={defaultV} key={defaultV}>
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
