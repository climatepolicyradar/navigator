const List = ({ list }) => {
  return (
    <ul className="text-indigo-500">
      {list.map((item) => (
        <li>
          {item.name}{' '}
          {item?.children && (
            <ul className="ml-4">
              {item.children.map((child) => (
                <li>{child.name}</li>
              ))}{' '}
            </ul>
          )}
        </li>
      ))}
    </ul>
  );
};
export default List;
