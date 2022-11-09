import useConfig from "@hooks/useConfig";
import FilterTag from "../buttons/FilterTag";
import { getCountryName } from "@helpers/getCountryFields";

const MultiList = ({ list, removeFilter, type }) => {
  const configQuery: any = useConfig("config");
  const { data: { countries = [] } = {} } = configQuery;

  const handleClick = (item) => {
    removeFilter(type, item, "delete");
  };
  return (
    <div className="flex flex-wrap mt-1">
      {list.length > 0
        ? list.map((item, index) => (
            <div key={`tag${index}`} className="mr-2 mt-1">
              <FilterTag onClick={() => handleClick(item)} item={type === "countries" ? getCountryName(item, countries) : item} />
            </div>
          ))
        : null}
    </div>
  );
};
export default MultiList;
