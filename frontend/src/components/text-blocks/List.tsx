const List = ({ list }) => {
  return (
    <ul className="text-indigo-500">
      {list.map((item, index) => (
        <li key={`listitem${index}`}>
          {item.name}{' '}
          {item?.children && (
            <ul className="ml-4">
              {item.children.map((child, index) => (
                <li key={`listchilditem${index}`}>{child.name}</li>
              ))}{' '}
            </ul>
          )}
        </li>
      ))}
    </ul>
  );
};
export default List;
