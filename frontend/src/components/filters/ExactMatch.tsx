const ExactMatch = ({ id, handleSearchChange, checked }) => {
  const handleClick = (e) => {
    const isChecked = e.currentTarget.checked;
    handleSearchChange('exact_match', isChecked);
  };
  return (
    <div className="text-sm flex items-center">
      <label className="checkbox-input" htmlFor={id}>
        <input
          id={id}
          type="checkbox"
          checked={checked}
          onClick={handleClick}
        />
        <span className="pl-2">Exact matches only</span>
      </label>
    </div>
  );
};
export default ExactMatch;
