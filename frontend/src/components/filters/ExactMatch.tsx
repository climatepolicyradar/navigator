const ExactMatch = ({ id, handleSearchChange, checked, landing = false }) => {
  const handleClick = (e) => {
    const isChecked = e.currentTarget.checked;
    handleSearchChange('exact_match', isChecked);
  };
  return (
    <div className={`${landing ? 'landing' : ''}`}>
      <label className="checkbox-input flex items-center" htmlFor={id}>
        <input
          className={`${
            landing ? 'text-indigo-600/0' : 'text-white'
          } border-blue-500 rounded`}
          id={id}
          type="checkbox"
          checked={checked}
          onChange={handleClick}
        />
        <span
          className={`${
            landing ? 'text-lg text-white' : 'text-sm'
          } pl-2 leading-none`}
        >
          {/* TODO: make translatable */}
          Show only exact matches
        </span>
      </label>
    </div>
  );
};
export default ExactMatch;
