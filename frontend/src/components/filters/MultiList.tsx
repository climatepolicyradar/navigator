const MultiList = ({ list }) => {
  return (
    <div>{list.length > 0 ? list.map((item) => <div>{item}</div>) : null}</div>
  );
};
export default MultiList;
