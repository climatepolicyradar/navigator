import FilterTag from '../buttons/FilterTag';

const MultiList = ({ list, removeFilter, type }) => {
  const handleClick = (item) => {
    removeFilter(type, item, 'delete');
  };
  return (
    <div className="flex flex-wrap mt-1">
      {list.length > 0
        ? list.map((item, index) => (
            <div key={`tag${index}`} className="mr-2 mt-1">
              <FilterTag onClick={() => handleClick(item)} item={item} />
            </div>
          ))
        : null}
    </div>
  );
};
export default MultiList;
