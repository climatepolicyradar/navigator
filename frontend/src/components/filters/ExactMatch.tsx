const ExactMatch = ({ id, handleSearchChange, checked }) => {
  const handleClick = (e) => {
    const isChecked = e.currentTarget.checked;
    handleSearchChange('exact_match', isChecked);
  };
  return (
    <div className="text-sm">
      <label className="checkbox-input flex items-center" htmlFor={id}>
        <input
          className="text-white border-blue-500 rounded"
          id={id}
          type="checkbox"
          checked={checked}
          onChange={handleClick}
        />
        <span className="pl-2 leading-none">Exact matches only</span>
      </label>
    </div>
  );
};
export default ExactMatch;
