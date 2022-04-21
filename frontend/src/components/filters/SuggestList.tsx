const SuggestList = ({ list, keyField, type, onClick }) => {
  // const arr = Array.apply(null, { length: 10 });

  return (
    <ul className="bg-indigo-100 -mt-2 relative z-10 rounded-b-lg">
      {list.map((item, index) => (
        <li
          key={index}
          onClick={() => {
            onClick(type, item[keyField]);
          }}
          className="hover:bg-blue-200 cursor-pointer my-1 p-2"
        >
          {item[keyField]}
        </li>
      ))}
    </ul>
  );
};

export default SuggestList;
