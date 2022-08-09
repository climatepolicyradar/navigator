function List({ list, bulleted = false }) {
  const renderChildren = (list: any) => (
    <>:{list.map((item, i) => [i > 0 && ', ', item.name])}</>
  );

  return (
    <ul
      className={`text-indigo-500 ${
        bulleted && 'ml-4 list-disc list-outside mb-4'
      }`}
    >
      {list.map((item, index) => (
        <li key={`listitem${index}`} className={!bulleted && 'inline'}>
          {index > 0 && !bulleted && ', '} {item.name}
          {item?.children && renderChildren(item.children)}
        </li>
      ))}
    </ul>
  );
}
export default List;
